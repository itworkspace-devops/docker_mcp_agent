import {
    useState
} from "react";

import { api }
from "../services/api";

import StatCard
from "../components/StatCard";

import DriftBadge
from "../components/DriftBadge";

export default function Drift() {

    const [results, setResults] =
        useState<any[]>([]);

    const [loading, setLoading] =
        useState(false);

    const runScan =
        async () => {

        try {

            setLoading(true);

            const res =
                await api.post(
                    "/drift/scan"
                );

            const findings =
                res.data.findings || [];

            setResults(
                findings
            );

        } catch (err) {

            console.error(err);

        } finally {

            setLoading(false);
        }
    };

    const criticalCount =
        results.filter(
            x =>
                x.severity ===
                "critical"
        ).length;

    return (

        <div>

            <h2>
                Drift Detection
            </h2>

            <button
                onClick={runScan}
            >
                Run Drift Scan
            </button>

            {
                loading &&
                <p>
                    Scanning...
                </p>
            }

            <div
                className="grid"
                style={{
                    marginTop: "20px",
                    marginBottom: "20px"
                }}
            >

                <StatCard
                    title="Total Drift Findings"
                    value={
                        results.length
                    }
                />

                <StatCard
                    title="Critical Drift"
                    value={
                        criticalCount
                    }
                />

            </div>

            <table>

                <thead>

                    <tr>

                        <th>
                            Severity
                        </th>

                        <th>
                            Category
                        </th>

                        <th>
                            Message
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {
                        results.map(
                            (
                                finding,
                                index
                            ) => (

                                <tr
                                    key={index}
                                    style={{
                                        backgroundColor:

                                            finding.severity === "critical"

                                                ? "#fee2e2"

                                                : "transparent"
                                    }}
                                >

                                    <td>

                                        <DriftBadge
                                            severity={
                                                finding.severity
                                            }
                                        />

                                    </td>

                                    <td>
                                        {
                                            finding.category
                                        }
                                    </td>

                                    <td>
                                        {
                                            finding.message
                                        }
                                    </td>

                                </tr>
                            )
                        )
                    }

                </tbody>

            </table>

        </div>
    );
}