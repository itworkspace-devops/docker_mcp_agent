import { Zap, Server, Activity, Pause, AlertCircle, CheckCircle2, AlertTriangle, TrendingDown } from "lucide-react";

type Props = {
    title: string;
    value: string | number;
    gradientClass?: string;
    icon?: React.ReactNode;
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
    icon
}: Props) {
    const defaultIcon = getIconForTitle(title);
    
    return (
        <div className={`stat-card ${gradientClass || ''}`}>
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