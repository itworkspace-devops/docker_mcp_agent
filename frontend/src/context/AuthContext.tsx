import { createContext, useEffect, useMemo, useState } from "react";

export interface AuthState {
    token: string;
    username: string;
    role: string;
    password_changed: boolean;
}

export interface AuthContextValue {
    auth: AuthState | null;
    login: (authData: AuthState) => void;
    logout: () => void;
    updateAuth: (partial: Partial<AuthState>) => void;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

const STORAGE_KEY = "docker-ai-auth";

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [auth, setAuth] = useState<AuthState | null>(() => {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            return raw ? JSON.parse(raw) as AuthState : null;
        } catch {
            return null;
        }
    });

    useEffect(() => {
        if (auth) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(auth));
        } else {
            localStorage.removeItem(STORAGE_KEY);
        }
    }, [auth]);

    const login = (authData: AuthState) => {
        setAuth(authData);
    };

    const logout = () => {
        setAuth(null);
    };

    const updateAuth = (partial: Partial<AuthState>) => {
        setAuth((current) => current ? { ...current, ...partial } : current);
    };

    const value = useMemo(
        () => ({ auth, login, logout, updateAuth }),
        [auth]
    );

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}
