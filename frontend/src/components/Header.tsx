import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { LogOut } from "lucide-react";

import NotificationBell from "./NotificationBell";
import { AuthContext } from "../context/AuthContext";

export default function Header() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const auth = authContext?.auth;

    const handleLogout = () => {
        authContext?.logout();
        navigate("/login");
    };

    return (
        <div className="header">
            <div>
                <h1>Docker AI Platform</h1>
                <p style={{
                    color: 'var(--text-secondary)',
                    margin: '4px 0 0 0',
                    fontSize: '14px'
                }}>
                    Intelligent infrastructure monitoring & management
                </p>
            </div>

            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '16px'
            }}>
                {auth && (
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'flex-end',
                        gap: '4px',
                        color: 'var(--text-secondary)',
                        fontSize: '14px'
                    }}>
                        <span>Signed in as {auth.username}</span>
                        <span style={{ fontWeight: 600 }}>{auth.role.toUpperCase()}</span>
                    </div>
                )}

                <Link
                    to="/notifications"
                    style={{
                        textDecoration: "none",
                        color: "inherit",
                        display: 'flex',
                        alignItems: 'center',
                        padding: '8px 12px',
                        borderRadius: '10px',
                        transition: 'all 0.3s ease',
                        cursor: 'pointer'
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)';
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'transparent';
                    }}
                >
                    <NotificationBell />
                </Link>

                <button style={{
                    background: 'rgba(99, 102, 241, 0.1)',
                    border: '1px solid rgba(99, 102, 241, 0.3)',
                    color: 'var(--primary)',
                    padding: '8px 12px',
                    borderRadius: '10px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    transition: 'all 0.3s ease',
                    fontSize: '14px',
                    fontWeight: '500'
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'rgba(99, 102, 241, 0.2)';
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)';
                }}
                onClick={handleLogout}
                >
                    <LogOut size={18} />
                    Logout
                </button>
            </div>
        </div>
    );
}
