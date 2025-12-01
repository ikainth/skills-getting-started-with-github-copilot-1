import request from 'supertest';
import app from '../src/app'; // Adjust the path if necessary

describe('Example Test Suite', () => {
    it('should respond with a 200 status code on the root endpoint', async () => {
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
    });

    it('should respond with JSON data', async () => {
        const response = await request(app).get('/api/users'); // Adjust the endpoint as necessary
        expect(response.headers['content-type']).toEqual(expect.stringContaining('json'));
    });

    // Add more test cases as needed
});