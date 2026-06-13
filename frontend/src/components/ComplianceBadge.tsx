type Props = {
    count: number;
};

export default function ComplianceBadge(
    {
        count
    }: Props
) {

    const compliant =
        count === 0;

    return (

        <span
            style={{
                backgroundColor:
                    compliant
                        ? "#16a34a"
                        : "#dc2626",

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
            {
                compliant
                    ? "COMPLIANT"
                    : "VIOLATIONS"
            }
        </span>
    );
}