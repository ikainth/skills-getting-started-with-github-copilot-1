import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from socketserver import ThreadingMixIn

PORT = int(os.environ.get("PORT", 8000))

# Example activities data (in-memory)
ACTIVITIES = {
    "Chess Club": {
        "description": "Strategy and tactics for players of all levels.",
        "schedule": "Tue & Thu 3:30pm - 4:30pm",
        "max_participants": 12,
        "participants": ["alice@mergington.edu", "bob@mergington.edu"],
    },
    "Robotics Team": {
        "description": "Build robots and compete in regional robotics competitions.",
        "schedule": "Mon & Wed 4:00pm - 6:00pm",
        "max_participants": 10,
        "participants": ["carlos@mergington.edu"],
    },
    "Drama Club": {
        "description": "Acting, stagecraft and production.",
        "schedule": "Fri 3:00pm - 5:00pm",
        "max_participants": 20,
        "participants": [],
    },
}


class RequestHandler(SimpleHTTPRequestHandler):
    # Serve static files and JSON API for /activities
    def _send_json(self, data, status=200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        # No cache to see updates immediately
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/activities":
            # Return activities JSON
            self._send_json(ACTIVITIES)
            return

        # Otherwise serve static files (index.html, CSS, JS, etc.)
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # Expect path like /activities/<activity-name>/signup
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 3 and parts[0] == "activities" and parts[-1] == "signup":
            # Activity name may contain slashes encoded; join parts[1:-1]
            activity_name = "/".join(parts[1:-1])
            activity_name = unquote(activity_name)

            # Ensure activity exists
            if activity_name not in ACTIVITIES:
                self._send_json({"detail": "Activity not found"}, status=404)
                return

            # Get email from query string now
            email_list = qs.get("email") or []
            email = email_list[0] if email_list else None
            if not email:
                self._send_json({"detail": "Email is required"}, status=400)
                return

            activity = ACTIVITIES[activity_name]
            if len(activity["participants"]) >= activity["max_participants"]:
                self._send_json({"detail": "Activity is full"}, status=400)
                return

            # Prevent duplicate signups
            if email in activity["participants"]:
                self._send_json({"detail": "Already signed up"}, status=400)
                return

            # Add participant
            activity["participants"].append(email)

            self._send_json({"message": f"Signed up {email} for {activity_name}"})
            return

        # For other POST paths, return 404
        self._send_json({"detail": "Not found"}, status=404)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


if __name__ == "__main__":
    # Serve static files from the "static" directory next to this file
    base_dir = os.path.dirname(__file__)
    static_dir = os.path.join(base_dir, "static")
    if not os.path.isdir(static_dir):
        print("Error: static directory not found:", static_dir)
        raise SystemExit(1)

    os.chdir(static_dir)  # Serve static files from /src/static
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    print(f"Serving on http://localhost:{PORT}. Press Ctrl+C to stop.")

    # Write PID file so external scripts can manage the server
    pid_file = os.path.join(base_dir, "server.pid")
    try:
        with open(pid_file, "w") as f:
            f.write(str(os.getpid()))
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        try:
            httpd.server_close()
        except Exception:
            pass
        # Remove PID file on shutdown
        try:
            os.remove(pid_file)
        except Exception:
            pass
