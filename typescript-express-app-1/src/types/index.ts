export type User = {
    id: string;
    name: string;
    email: string;
    password: string;
};

export type CreateUserDto = {
    name: string;
    email: string;
    password: string;
};

export type UpdateUserDto = {
    name?: string;
    email?: string;
    password?: string;
};