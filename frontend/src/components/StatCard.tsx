import { Zap, Server, Activity, Pause, AlertCircle, CheckCircle2, AlertTriangle, TrendingDown } from "lucide-react";

type Props = {
    title: string;
    value: string | number;
    gradientClass?: string;
    icon?: React.ReactNode;
    onClick?: () => void;
};

const getIconForTitle = (title: string) => {
    const icons: { [key: string]: React.ReactNode } = {
        "Hosts": <Server size={20} />,
        "Containers": <Zap size={20} />,
        "Running": <Activity size={20} />,
        "Stopped": <Pause size={20} />,
        "Findings": <AlertCircle size={20} />,
        "Remediations": <CheckCircle2 size={20} />,
        "Incidents": <AlertTriangle size={20} />,
        "Drift Findings": <TrendingDown size={20} />
    };
    return icons[title] || <Zap size={20} />;
};

export default function StatCard({
    title,
    value,
    gradientClass,
    icon,
    onClick
}: Props) {
    const defaultIcon = getIconForTitle(title);
    
    return (
        <div 
            className={`stat-card ${gradientClass || ''}`}
            onClick={onClick}
            style={{ 
                cursor: onClick ? 'pointer' : 'default',
                transition: 'transform 0.2s ease, box-shadow 0.2s ease'
            }}
            onMouseEnter={(e) => {
                if (onClick) {
                    e.currentTarget.style.transform = 'translateY(-4px)';
                    e.currentTarget.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3)';
                }
            }}
            onMouseLeave={(e) => {
                if (onClick) {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                }
            }}
        >
            <div className="stat-card-title">
                {icon || defaultIcon}
                <span>{title}</span>
            </div>
            <div className="stat-value">
                {value}
            </div>
        </div>
    );
}