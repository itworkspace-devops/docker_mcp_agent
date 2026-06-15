import {
    LayoutDashboard,
    Server,
    Shield,
    Bell,
    Bot,
    CheckCircle2,
    AlertCircle,
    Settings,
    LogOut,
    Menu,
    X,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";

import { AuthContext } from "../context/AuthContext";

interface SidebarProps {
    isOpen: boolean;
    onToggle: () => void;
}

export default function Sidebar({ isOpen, onToggle }: SidebarProps) {
    const authContext = useContext(AuthContext);
    const auth = authContext?.auth;
    const navigate = useNavigate();

    const mainLinks = [
        { path: "/", icon: LayoutDashboard, label: "Dashboard" },
        { path: "/fleet", icon: Server, label: "Fleet" },
        { path: "/findings", icon: Shield, label: "Findings" },
        { path: "/compliance", icon: CheckCircle2, label: "Compliance" },
        { path: "/drift", icon: AlertCircle, label: "Drift" },
        { path: "/incidents", icon: AlertCircle, label: "Incidents" },
    ];

    const secondaryLinks = [
        { path: "/notifications", icon: Bell, label: "Notifications" },
        { path: "/agent", icon: Bot, label: "Agent" },
    ];

    const handleLogout = () => {
        authContext?.logout();
        navigate("/login");
    };

    return (
        <div className={`sidebar ${!isOpen ? 'sidebar-collapsed' : ''}`}>
            <div className="sidebar-header">
                <div>
                    <h2 style={{ 
                        margin: 0,
                        fontSize: '20px',
                        fontWeight: '800',
                        background: 'var(--primary-gradient)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text',
                    }}>
                        🤖 Docker AI
                    </h2>
                </div>
                <button className="sidebar-toggle-btn" onClick={onToggle}>
                    {isOpen ? <X size={20} /> : <Menu size={20} />}
                </button>
            </div>

            <div className="sidebar-scroll-area">
                <nav style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {mainLinks.map(({ path, icon: Icon, label }) => (
                        <Link
                            key={path}
                            to={path}
                            style={{ textDecoration: 'none', color: 'inherit' }}
                        >
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '10px',
                                color: 'var(--text-secondary)',
                                textDecoration: 'none',
                                padding: '10px 14px',
                                borderRadius: '12px',
                                transition: 'all 0.3s ease',
                                fontSize: '14px',
                                fontWeight: '500',
                                borderLeft: '3px solid transparent',
                                cursor: 'pointer'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.color = 'var(--text)';
                                e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)';
                                e.currentTarget.style.borderLeftColor = 'var(--primary)';
                                e.currentTarget.style.transform = 'translateX(4px)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.color = 'var(--text-secondary)';
                                e.currentTarget.style.background = 'transparent';
                                e.currentTarget.style.borderLeftColor = 'transparent';
                                e.currentTarget.style.transform = 'translateX(0)';
                            }}
                            >
                                <Icon size={20} />
                                <span>{label}</span>
                            </div>
                        </Link>
                    ))}
                    {auth?.role === "admin" && (
                        <Link
                            to="/users"
                            style={{ textDecoration: 'none', color: 'inherit' }}
                        >
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '10px',
                                color: 'var(--text-secondary)',
                                textDecoration: 'none',
                                padding: '10px 14px',
                                borderRadius: '12px',
                                transition: 'all 0.3s ease',
                                fontSize: '14px',
                                fontWeight: '500',
                                borderLeft: '3px solid transparent',
                                cursor: 'pointer'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.color = 'var(--text)';
                                e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)';
                                e.currentTarget.style.borderLeftColor = 'var(--primary)';
                                e.currentTarget.style.transform = 'translateX(4px)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.color = 'var(--text-secondary)';
                                e.currentTarget.style.background = 'transparent';
                                e.currentTarget.style.borderLeftColor = 'transparent';
                                e.currentTarget.style.transform = 'translateX(0)';
                            }}
                            >
                                <Settings size={20} />
                                <span>Users</span>
                            </div>
                        </Link>
                    )}
                </nav>

                <div style={{
                    height: '1px',
                    background: 'var(--card-border)',
                    margin: '8px 0'
                }} />

                <nav style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {secondaryLinks.map(({ path, icon: Icon, label }) => (
                        <Link
                            key={path}
                            to={path}
                            style={{ textDecoration: 'none', color: 'inherit' }}
                        >
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '10px',
                                color: 'var(--text-secondary)',
                                textDecoration: 'none',
                                padding: '10px 14px',
                                borderRadius: '12px',
                                transition: 'all 0.3s ease',
                                fontSize: '14px',
                                fontWeight: '500',
                                borderLeft: '3px solid transparent',
                                cursor: 'pointer'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.color = 'var(--text)';
                                e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)';
                                e.currentTarget.style.borderLeftColor = 'var(--primary)';
                                e.currentTarget.style.transform = 'translateX(4px)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.color = 'var(--text-secondary)';
                                e.currentTarget.style.background = 'transparent';
                                e.currentTarget.style.borderLeftColor = 'transparent';
                                e.currentTarget.style.transform = 'translateX(0)';
                            }}
                            >
                                <Icon size={20} />
                                <span>{label}</span>
                            </div>
                        </Link>
                    ))}
                </nav>
            </div>

            <div className="sidebar-footer">
                <button style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    color: 'var(--text-secondary)',
                    background: 'transparent',
                    border: 'none',
                    padding: '8px 12px',
                    borderRadius: '10px',
                    cursor: 'pointer',
                    fontSize: '13px',
                    fontWeight: '500',
                    transition: 'all 0.3s ease',
                    textAlign: 'left',
                    fontFamily: 'inherit'
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.color = 'var(--text)';
                    e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)';
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.color = 'var(--text-secondary)';
                    e.currentTarget.style.background = 'transparent';
                }}
                >
                    <Settings size={18} />
                    <span>Settings</span>
                </button>
                <button style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    color: '#ef4444',
                    background: 'transparent',
                    border: 'none',
                    padding: '8px 12px',
                    borderRadius: '10px',
                    cursor: 'pointer',
                    fontSize: '13px',
                    fontWeight: '500',
                    transition: 'all 0.3s ease',
                    textAlign: 'left',
                    fontFamily: 'inherit'
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)';
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'transparent';
                }}
                onClick={handleLogout}
                >
                    <LogOut size={18} />
                    <span>Logout</span>
                </button>
            </div>
        </div>
    );
}
