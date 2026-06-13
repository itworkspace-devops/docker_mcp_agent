const wsUrl = import.meta.env.VITE_WS_URL || "ws://127.0.0.1:8001";

console.log("WS URL:", wsUrl);

export const createWebSocket = () => {
    return new WebSocket(wsUrl);
};