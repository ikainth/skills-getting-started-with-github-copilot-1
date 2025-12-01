import express from 'express';
import { json } from 'body-parser';
import { setUserRoutes } from './routes/userRoutes';
import { logger } from './utils/logger';
import { config } from './config';

const app = express();
const PORT = config.port || 3000;

app.use(json());
app.use(logger);

setUserRoutes(app);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});