type Props = {
    severity: string;
};

export default function IncidentBadge({
    severity
}: Props) {

    const getColor = () => {

        switch (
            severity?.toLowerCase()
        ) {

            case "critical":
                return "#dc2626";

            case "high":
                return "#ea580c";

            case "medium":
                return "#ca8a04";

            default:
                return "#2563eb";
        }
    };

    return (

        <span
            style={{
                backgroundColor:
                    getColor(),

                color: "white",

                padding: "4px 8px",

                borderRadius: "6px",

                fontWeight: "bold"
            }}
        >
            {severity}
        </span>
    );
}