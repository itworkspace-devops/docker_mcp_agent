import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";
import { api } from "../services/api";

export default function Dashboard() {

    const [summary, setSummary] =
        useState<any>();

    useEffect(() => {

        api.get("/dashboard/summary")
            .then(res => {

                setSummary(
                    res.data
                );
            });

    }, []);

    if (!summary)
        return <div>Loading...</div>;

    return (

        <div className="grid">

            <StatCard
                title="Hosts"
                value={summary.hosts}
            />

            <StatCard
                title="Containers"
                value={summary.containers}
            />

            <StatCard
                title="Running"
                value={summary.running}
            />

            <StatCard
                title="Stopped"
                value={summary.stopped}
            />

            <StatCard
                title="Findings"
                value={summary.findings}
            />

            <StatCard
                title="Remediations"
                value={summary.remediations}
            />

        </div>
    );
}