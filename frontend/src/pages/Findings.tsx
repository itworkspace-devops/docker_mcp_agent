import {
    useEffect,
    useState
} from "react";

import { api }
from "../services/api";

import SeverityBadge
from "../components/SeverityBadge";

export default function Findings() {

    const [findings, setFindings] =
        useState<any[]>([]);

    const [loading, setLoading] =
        useState(true);

    const loadFindings =
        async () => {

        try {

            const res =
                await api.get(
                    "/findings"
                );

            setFindings(
                res.data
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

    useEffect(() => {

        loadFindings();

        const timer =
            setInterval(
                loadFindings,
                30000
            );

        return () =>
            clearInterval(
                timer
            );

    }, []);

    if (loading) {

        return (
            <div>
                Loading...
            </div>
        );
    }

    return (

        <div>

            <h2>
                Findings
            </h2>

            <table>

                <thead>

                    <tr>

                        <th>ID</th>

                        <th>Time</th>

                        <th>Severity</th>

                        <th>Category</th>

                        <th>Message</th>

                        <th>Status</th>

                    </tr>

                </thead>

                <tbody>

                    {
                        findings.map(
                            (
                                finding
                            ) => (

                                <tr
                                    key={
                                        finding.id
                                    }
                                >

                                    <td>
                                        {
                                            finding.id
                                        }
                                    </td>

                                    <td>
                                        {
                                            finding.timestamp
                                        }
                                    </td>

                                    <td>

                                        <SeverityBadge
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

                                    <td>
                                        {
                                            finding.status
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