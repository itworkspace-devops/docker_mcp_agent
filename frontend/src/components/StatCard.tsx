type Props = {
    title: string;
    value: number | string;
};

export default function StatCard({
    title,
    value,
}: Props) {
    return (
        <div className="card">
            <h3>{title}</h3>
            <h1>{value}</h1>
        </div>
    );
}