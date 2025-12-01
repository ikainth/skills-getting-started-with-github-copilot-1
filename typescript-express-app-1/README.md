# TypeScript Express App

This is a TypeScript-based Express application that provides a RESTful API for user management.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [License](#license)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd typescript-express-app
   ```
3. Install the dependencies:
   ```
   npm install
   ```

## Usage

To start the application, run the following command:
```
npm start
```
The server will start on the specified port (default is 3000).

## API Endpoints

### User Management

- **POST /users**: Create a new user
- **GET /users/:id**: Retrieve a user by ID
- **PUT /users/:id**: Update a user by ID
- **DELETE /users/:id**: Delete a user by ID

## Testing

To run the tests, use the following command:
```
npm test
```

## License

This project is licensed under the MIT License.