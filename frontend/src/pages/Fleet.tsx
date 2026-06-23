import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { api } from "../services/api";

import StatCard from "../components/StatCard";

export default function Fleet() {
    const navigate = useNavigate();
    const [hosts, setHosts] =
        useState<any[]>([]);
    console.log("Fleet hosts:", hosts);
    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");

    useEffect(() => {

        loadFleet();

    }, []);

    const loadFleet = async () => {

        try {

            setLoading(true);

            const res = await api.get(
                "/fleet/health"
            );

            setHosts(
                res.data
            );

        } catch (err: any) {

            setError(
                err.message
            );

        } finally {

            setLoading(false);
        }
    };

    const totalHosts =
        hosts.length;

    const totalContainers =
        hosts.reduce(
            (sum, host) =>
                sum + (host.containers || 0),
            0
        );

    const totalRunning =
        hosts.reduce(
            (sum, host) =>
                sum + (host.running || 0),
            0
        );

    const totalStopped =
        hosts.reduce(
            (sum, host) =>
                sum + (host.stopped || 0),
            0
        );

    const healthyHosts =
        hosts.filter(
            h => h.healthy
        ).length;

    if (loading) {

        return (
            <div>
                Loading fleet data...
            </div>
        );
    }

    if (error) {

        return (
            <div>

                <h2>
                    Fleet Health
                </h2>

                <p>
                    Error: {error}
                </p>

            </div>
        );
    }

    return (

        <div className="page-shell">

            <h2>
                Fleet Health Dashboard
            </h2>

            <div
                className="grid"
                style={{
                    marginBottom: "20px"
                }}
            >

                <StatCard
                    title="Hosts"
                    value={totalHosts}
                    onClick={() => navigate("/hosts")}
                />

                <StatCard
                    title="Healthy Hosts"
                    value={healthyHosts}
                />

                <StatCard
                    title="Containers"
                    value={totalContainers}
                    onClick={() => navigate("/containers")}
                />

                <StatCard
                    title="Running"
                    value={totalRunning}
                    onClick={() => navigate("/containers")}
                />

                <StatCard
                    title="Stopped"
                    value={totalStopped}
                    onClick={() => navigate("/containers")}
                />

            </div>

            <table>

                <thead>

                    <tr>

                        <th>
                            Host
                        </th>

                        <th>
                            Status
                        </th>

                        <th>
                            Containers
                        </th>

                        <th>
                            Running
                        </th>

                        <th>
                            Stopped
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {hosts.map(
                        (host, index) => (

                            <tr key={index}>

                                <td>
                                    {host.host}
                                </td>

                                <td>

                                    {
                                        host.healthy
                                            ? "🟢 Healthy"
                                            : "🔴 Offline"
                                    }

                                </td>

                                <td>
                                    {host.containers}
                                </td>

                                <td>
                                    {host.running}
                                </td>

                                <td>
                                    {host.stopped}
                                </td>

                            </tr>
                        )
                    )}

                </tbody>

            </table>

        </div>
    );
}