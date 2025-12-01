import express from 'express';
import bodyParser from 'body-parser';
import userRoutes from './routes/userRoutes';
import { logger } from './utils/logger';
import { config } from './config';

const app = express();

// Middleware
app.use(bodyParser.json());
app.use(logger);

// Routes
app.use('/api/users', userRoutes());

// Start the server
const PORT = config.port || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});