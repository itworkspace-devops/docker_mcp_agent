import { Link } from "react-router-dom";
import { useContext } from "react";
import { Menu } from "lucide-react";

import NotificationBell from "./NotificationBell";
import { AuthContext } from "../context/AuthContext";

interface HeaderProps {
    onToggleSidebar: () => void;
    isSidebarOpen: boolean;
}

export default function Header({ onToggleSidebar, isSidebarOpen }: HeaderProps) {
    const authContext = useContext(AuthContext);
    const auth = authContext?.auth;

    return (
        <div className="header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                {!isSidebarOpen && (
                    <button 
                        className="desktop-toggle-btn" 
                        onClick={onToggleSidebar}
                        style={{
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid var(--card-border)',
                            color: 'var(--text)',
                            padding: '8px',
                            borderRadius: '10px',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            transition: 'all 0.3s ease'
                        }}
                    >
                        <Menu size={20} />
                    </button>
                )}
                <div>
                    <h1 style={{
                        margin: 0,
                        fontSize: '22px',
                        fontWeight: '800',
                        color: 'var(--text)',
                        letterSpacing: '-0.5px'
                    }}>
                        Docker AI Platform
                    </h1>
                    <p style={{
                        color: 'var(--text-secondary)',
                        margin: '2px 0 0 0',
                        fontSize: '13px',
                        fontWeight: '500'
                    }}>
                        Intelligent infrastructure monitoring & management
                    </p>
                </div>
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
                        gap: '2px',
                        color: 'var(--text-secondary)',
                        fontSize: '13px'
                    }}>
                        <span>Signed in as <strong style={{ color: 'var(--text)' }}>{auth.username}</strong></span>
                        <span style={{ 
                            fontSize: '11px',
                            fontWeight: 700,
                            color: 'var(--primary)',
                            background: 'rgba(99, 102, 241, 0.1)',
                            padding: '2px 8px',
                            borderRadius: '6px',
                            textTransform: 'uppercase'
                        }}>
                            {auth.role}
                        </span>
                    </div>
                )}

                <div style={{
                    width: '1px',
                    height: '24px',
                    background: 'var(--card-border)',
                    margin: '0 4px'
                }} />

                <Link
                    to="/notifications"
                    style={{
                        textDecoration: "none",
                        color: "inherit",
                        display: 'flex',
                        alignItems: 'center',
                        padding: '8px',
                        borderRadius: '10px',
                        transition: 'all 0.3s ease',
                        cursor: 'pointer',
                        background: 'rgba(255, 255, 255, 0.03)'
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)';
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)';
                    }}
                >
                    <NotificationBell />
                </Link>
            </div>
        </div>
    );
}
