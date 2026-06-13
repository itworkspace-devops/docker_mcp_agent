import {
    LayoutDashboard,
    Server,
    Shield,
    Bell,
    Bot,
    CheckCircle2,
    AlertCircle,
    Settings,
    LogOut
} from "lucide-react";

import {
    Link
} from "react-router-dom";

export default function Sidebar() {

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

    return (

        <div
            className="sidebar"
        >

            <div>
                <h2 style={{ marginBottom: '8px' }}>
                    🤖 Docker AI
                </h2>
                <p style={{
                    margin: 0,
                    fontSize: '12px',
                    color: 'var(--text-secondary)',
                    fontWeight: '500',
                    letterSpacing: '0.3px'
                }}>
                    Infrastructure Management
                </p>
            </div>

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
                            gap: '12px',
                            color: 'var(--text-secondary)',
                            textDecoration: 'none',
                            padding: '12px 16px',
                            borderRadius: '12px',
                            transition: 'all 0.3s ease',
                            fontSize: '15px',
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
                            gap: '12px',
                            color: 'var(--text-secondary)',
                            textDecoration: 'none',
                            padding: '12px 16px',
                            borderRadius: '12px',
                            transition: 'all 0.3s ease',
                            fontSize: '15px',
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

            <div style={{ flex: 1 }} />

            <div style={{
                height: '1px',
                background: 'var(--card-border)',
                marginBottom: '8px'
            }} />

            <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '4px'
            }}>
                <button style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    color: 'var(--text-secondary)',
                    background: 'transparent',
                    border: 'none',
                    padding: '12px 16px',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    fontSize: '15px',
                    fontWeight: '500',
                    transition: 'all 0.3s ease',
                    textAlign: 'left',
                    fontFamily: 'inherit'
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.color = 'var(--text)';
                    e.currentTarget.style.background = 'rgba(99, 102, 241, 0.1)';
                    e.currentTarget.style.transform = 'translateX(4px)';
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.color = 'var(--text-secondary)';
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.transform = 'translateX(0)';
                }}
                >
                    <Settings size={20} />
                    <span>Settings</span>
                </button>
                <button style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    color: '#ef4444',
                    background: 'transparent',
                    border: 'none',
                    padding: '12px 16px',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    fontSize: '15px',
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
                >
                    <LogOut size={20} />
                    <span>Logout</span>
                </button>
            </div>

        </div>
    );
}