import {
    BrowserRouter,
    Routes,
    Route,
    Navigate,
} from "react-router-dom";
import { useContext, useState, useEffect } from "react";
import { Menu } from "lucide-react";

import { AuthProvider, AuthContext } from "./context/AuthContext";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Dashboard from "./pages/Dashboard";
import Fleet from "./pages/Fleet";
import Findings from "./pages/Findings";
import Compliance from "./pages/Compliance";
import Drift from "./pages/Drift";
import Agent from "./pages/Agent";
import Incidents from "./pages/Incidents";
import Approvals from "./pages/Approvals";
import Notifications from "./pages/Notifications";
import Users from "./pages/Users";
import Login from "./pages/Login";
import ChangePassword from "./pages/ChangePassword";

import "./styles/theme.css";
import "./styles/layout.css";
import "./styles/cards.css";
import "./styles/tables.css";

function AppRoutes() {
    const authContext = useContext(AuthContext);
    const auth = authContext?.auth;
    const [sidebarOpen, setSidebarOpen] = useState(window.innerWidth > 768);

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth > 768) {
                setSidebarOpen(true);
            } else {
                setSidebarOpen(false);
            }
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    if (!auth) {
        return (
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/change-password" element={<Navigate to="/login" replace />} />
                <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
        );
    }

    if (!auth.password_changed) {
        return (
            <Routes>
                <Route path="/change-password" element={<ChangePassword />} />
                <Route path="*" element={<Navigate to="/change-password" replace />} />
            </Routes>
        );
    }

    return (
        <div className="layout">
            <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
            
            {window.innerWidth <= 768 && sidebarOpen && (
                <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
            )}

            <div className="content">
                <Header onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} isSidebarOpen={sidebarOpen} />
                <Routes>

                        <Route
                            path="/"
                            element={<Dashboard />}
                        />

                        <Route
                            path="/fleet"
                            element={<Fleet />}
                        />

                        <Route
                            path="/findings"
                            element={<Findings />}
                        />

                        <Route
                            path="/compliance"
                            element={<Compliance />}
                        />

                        <Route
                            path="/drift"
                            element={<Drift />}
                        />

                        <Route
                            path="/incidents"
                            element={<Incidents />}
                        />

                        <Route
                            path="/notifications"
                            element={
                                <Notifications />
                            }
                        />

                        <Route
                            path="/approvals"
                            element={<Approvals />}
                        />

                        <Route
                            path="/agent"
                            element={<Agent />}
                        />
                    <Route
                        path="/users"
                        element={auth?.role === "admin" ? <Users /> : <Navigate to="/" replace />}
                    />
                    <Route
                        path="*"
                        element={<Navigate to="/" replace />}
                    />
                </Routes>
            </div>
        </div>
    );
}

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <AppRoutes />
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;