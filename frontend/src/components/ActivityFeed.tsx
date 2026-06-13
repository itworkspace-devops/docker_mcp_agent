import { AlertCircle, Zap, Shield, CheckCircle2, TrendingDown } from "lucide-react";

interface Activity {
    id: string;
    message: string;
    icon: React.ReactNode;
    color: string;
    timestamp: string;
}

export default function ActivityFeed() {

    const activities: Activity[] = [
        {
            id: "1",
            message: "Container nginx restarted",
            icon: <Zap size={18} />,
            color: "#06b6d4",
            timestamp: "2 min ago"
        },
        {
            id: "2",
            message: "New security finding detected",
            icon: <Shield size={18} />,
            color: "#ef4444",
            timestamp: "5 min ago"
        },
        {
            id: "3",
            message: "Drift detected in production",
            icon: <TrendingDown size={18} />,
            color: "#f59e0b",
            timestamp: "12 min ago"
        },
        {
            id: "4",
            message: "Approval policy granted",
            icon: <CheckCircle2 size={18} />,
            color: "#10b981",
            timestamp: "15 min ago"
        },
    ];

    return (

        <div className="stat-card" style={{
            background: 'linear-gradient(135deg, var(--card) 0%, var(--card-hover) 100%)',
            border: '1px solid var(--card-border)',
            borderRadius: '20px'
        }}>

            <h3 style={{
                margin: 0,
                fontSize: '18px',
                fontWeight: '700',
                color: 'var(--text)',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
            }}>
                <AlertCircle size={20} />
                Recent Activity
            </h3>

            <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '0',
                marginTop: '8px'
            }}>
                {activities.map((activity, index) => (
                    <div
                        key={activity.id}
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '12px',
                            padding: '14px 0',
                            borderBottom: index < activities.length - 1 ? '1px solid var(--card-border)' : 'none',
                            transition: 'all 0.2s ease'
                        }}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.background = 'rgba(99, 102, 241, 0.05)';
                            e.currentTarget.style.paddingLeft = '8px';
                            e.currentTarget.style.paddingRight = '8px';
                            e.currentTarget.style.marginLeft = '-8px';
                            e.currentTarget.style.marginRight = '-8px';
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.background = 'transparent';
                            e.currentTarget.style.paddingLeft = '0';
                            e.currentTarget.style.paddingRight = '0';
                            e.currentTarget.style.marginLeft = '0';
                            e.currentTarget.style.marginRight = '0';
                        }}
                    >
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            width: '36px',
                            height: '36px',
                            borderRadius: '10px',
                            background: `${activity.color}15`,
                            color: activity.color,
                            flexShrink: 0
                        }}>
                            {activity.icon}
                        </div>
                        
                        <div style={{
                            flex: 1,
                            minWidth: 0
                        }}>
                            <p style={{
                                margin: '0 0 4px 0',
                                fontSize: '14px',
                                fontWeight: '500',
                                color: 'var(--text)',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                whiteSpace: 'nowrap'
                            }}>
                                {activity.message}
                            </p>
                            <p style={{
                                margin: 0,
                                fontSize: '12px',
                                color: 'var(--text-muted)'
                            }}>
                                {activity.timestamp}
                            </p>
                        </div>
                    </div>
                ))}
            </div>

        </div>
    );
}