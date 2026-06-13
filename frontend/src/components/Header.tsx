import { Link } from "react-router-dom";
import { Settings } from "lucide-react";

import NotificationBell from "./NotificationBell";

export default function Header() {

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
                >
                    <Settings size={18} />
                    Settings
                </button>
            </div>

        </div>
    );
}