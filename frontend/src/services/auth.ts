import { api } from "./api";

export interface LoginPayload {
    username: string;
    password: string;
}

export interface AuthState {
    token: string;
    username: string;
    role: string;
    password_changed: boolean;
    change_required: boolean;
}

export interface CreateUserPayload {
    username: string;
    password: string;
    role: string;
}

export interface UserItem {
    username: string;
    role: string;
    password_changed: boolean;
}

export async function login(payload: LoginPayload) {
    const response = await api.post("/auth/login", payload);
    return response.data as AuthState;
}

export async function changePassword(token: string, newPassword: string) {
    const response = await api.post(
        "/auth/change-password",
        { new_password: newPassword },
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;
}

export async function fetchUsers(token: string) {
    const response = await api.get("/auth/users", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data as UserItem[];
}

export async function createUser(payload: CreateUserPayload, token: string) {
    const response = await api.post("/auth/users", payload, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data as UserItem;
}

export async function fetchMe(token: string) {
    const response = await api.get("/auth/me", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data as UserItem;
}
