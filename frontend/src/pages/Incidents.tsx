import {
    useEffect,
    useState
} from "react";

import { api }
from "../services/api";

import StatCard
from "../components/StatCard";

import IncidentBadge
from "../components/IncidentBadge";

export default function Incidents() {

    const [incidents, setIncidents] =
        useState<any[]>([]);

    const [loading, setLoading] =
        useState(true);

    const loadIncidents =
        async () => {

        try {

            const res =
                await api.get(
                    "/incidents"
                );

            setIncidents(
                res.data
            );

        } catch (err) {

            console.error(err);

        } finally {

            setLoading(false);
        }
    };

    useEffect(() => {

        loadIncidents();

    }, []);

    const criticalCount =
        incidents.filter(
            i =>
                i.severity ===
                "critical"
        ).length;

    if (loading) {

        return (
            <div>
                Loading incidents...
            </div>
        );
    }

    return (

        <div>

            <h2>
                Incident Investigation
            </h2>

            <div
                className="grid"
                style={{
                    marginBottom: "20px"
                }}
            >

                <StatCard
                    title="Incidents"
                    value={
                        incidents.length
                    }
                />

                <StatCard
                    title="Critical"
                    value={
                        criticalCount
                    }
                />

            </div>

            <table>

                <thead>

                    <tr>

                        <th>
                            Container
                        </th>

                        <th>
                            Severity
                        </th>

                        <th>
                            Root Cause
                        </th>

                        <th>
                            Analysis
                        </th>

                        <th>
                            Recommendation
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {
                        incidents.map(
                            (
                                incident,
                                index
                            ) => (

                                <tr
                                    key={index}
                                >

                                    <td>
                                        {
                                            incident.container
                                        }
                                    </td>

                                    <td>

                                        <IncidentBadge
                                            severity={
                                                incident.severity
                                            }
                                        />

                                    </td>

                                    <td>
                                        {
                                            incident.root_cause
                                        }
                                    </td>

                                    <td>
                                        {
                                            incident.analysis
                                        }
                                    </td>

                                    <td>
                                        {
                                            incident.recommendation
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