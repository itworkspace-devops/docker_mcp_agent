import {
    useState
} from "react";

import { api }
from "../services/api";

import ComplianceBadge
from "../components/ComplianceBadge";

export default function Compliance() {

    const [results, setResults] =
        useState<any[]>([]);

    const [loading, setLoading] =
        useState(false);

    const scan =
        async () => {

        try {

            setLoading(
                true
            );

            const res =
                await api.post(
                    "/compliance/scan"
                );

            setResults(
                res.data.results || []
            );

        } catch (err) {

            console.error(
                err
            );

        } finally {

            setLoading(
                false
            );
        }
    };

    return (

        <div>

            <h2>
                Compliance Scanner
            </h2>

            <button
                onClick={scan}
            >
                Run Compliance Scan
            </button>

            {
                loading &&
                <p>
                    Scanning...
                </p>
            }

            <table
                style={{
                    marginTop:
                        "20px"
                }}
            >

                <thead>

                    <tr>

                        <th>
                            Container
                        </th>

                        <th>
                            Status
                        </th>

                        <th>
                            Violations
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {
                        results.map(
                            (
                                item,
                                index
                            ) => (

                                <tr
                                    key={index}
                                >

                                    <td>
                                        {
                                            item.container
                                        }
                                    </td>

                                    <td>

                                        <ComplianceBadge
                                            count={
                                                item.violations.length
                                            }
                                        />

                                    </td>

                                    <td>

                                        {
                                            item.violations.join(
                                                ", "
                                            )
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