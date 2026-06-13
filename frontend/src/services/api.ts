import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8090";
const STORAGE_KEY = "docker-ai-auth";

console.log("API baseURL:", baseURL);

export const api = axios.create({
    baseURL,
});

api.interceptors.request.use((config) => {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
            const auth = JSON.parse(raw);
            if (auth?.token) {
                if (config.headers) {
                    (config.headers as Record<string, string>).Authorization = `Bearer ${auth.token}`;
                } else {
                    config.headers = {
                        Authorization: `Bearer ${auth.token}`,
                    } as any;
                }
            }
        }
    } catch {
        // ignore invalid localStorage state
    }

    return config;
});