import { Router } from 'express';
import UserController from '../controllers/userController';

const router = Router();
const userController = new UserController();

export const setUserRoutes = (app) => {
    app.use('/api/users', router);
    
    router.post('/', userController.createUser);
    router.get('/:id', userController.getUser);
    router.put('/:id', userController.updateUser);
    router.delete('/:id', userController.deleteUser);
};