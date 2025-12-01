export class UserService {
    private users: Map<number, { id: number; name: string; email: string; password: string }> = new Map();
    private currentId: number = 1;

    registerUser(name: string, email: string, password: string) {
        const user = { id: this.currentId, name, email, password };
        this.users.set(this.currentId, user);
        this.currentId++;
        return user;
    }

    findUserById(id: number) {
        return this.users.get(id);
    }

    deleteUser(id: number) {
        return this.users.delete(id);
    }
}