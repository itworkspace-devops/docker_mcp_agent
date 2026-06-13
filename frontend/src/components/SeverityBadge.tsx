type Props = {
    severity: string;
};

export default function SeverityBadge(
    {
        severity
    }: Props
) {

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

            case "low":
                return "#16a34a";

            default:
                return "#6b7280";
        }
    };

    return (

        <span
            style={{
                backgroundColor:
                    getColor(),

                color: "white",

                padding:
                    "4px 8px",

                borderRadius:
                    "6px",

                fontSize:
                    "12px",

                fontWeight:
                    "bold"
            }}
        >
            {severity}
        </span>
    );
}