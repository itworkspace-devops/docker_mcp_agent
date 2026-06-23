import { useEffect, useState } from "react";
import { Activity } from "lucide-react";
import { useNavigate } from "react-router-dom";

import StatCard from "../components/StatCard";
import { api } from "../services/api";
import { createWebSocket } from "../services/ws";

import ActivityFeed from "../components/ActivityFeed";

interface DashboardSummary {
    hosts: number;
    containers: number;
    running: number;
    stopped: number;
    findings: number;
    remediations: number;
    incidents: number;
    drift_findings: number;
}

export default function Dashboard() {
    const navigate = useNavigate();
    const [summary, setSummary] =
        useState<DashboardSummary | null>(
            null
        );

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState<string | null>(null);

    const loadSummary = async () => {

        try {

            setError(null);

            const res =
                await api.get(
                    "/dashboard/summary"
                );

            console.log("Dashboard summary response:", res.data);

            setSummary(
                res.data
            );

        } catch (err: any) {

            console.error(
                "Failed to load dashboard summary",
                err
            );
            setError(err?.message || "Unable to load dashboard summary");

        } finally {

            setLoading(false);
        }
    };

    useEffect(() => {

        loadSummary();

        const ws =
            createWebSocket();

        ws.onopen = () => {

            console.log(
                "Dashboard WebSocket connected"
            );
        };

        ws.onmessage = (
            event
        ) => {

            try {

                const message =
                    JSON.parse(
                        event.data
                    );

                console.log(
                    "Realtime Event:",
                    message
                );

                loadSummary();

            } catch (err) {

                console.error(
                    "Failed to parse websocket message",
                    err
                );
            }
        };

        ws.onerror = (
            error
        ) => {

            console.error(
                "WebSocket error:",
                error
            );
        };

        ws.onclose = () => {

            console.log(
                "Dashboard WebSocket disconnected"
            );
        };

        return () => {

            ws.close();
        };

    }, []);

    if (loading) {

        return (
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: '400px',
                color: 'var(--text-secondary)'
            }}>
                <div style={{ textAlign: 'center' }}>
                    <Activity size={40} style={{ marginBottom: '16px', opacity: 0.6 }} />
                    <p style={{ fontSize: '16px' }}>Loading dashboard...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div style={{
                padding: '32px',
                color: 'var(--text)',
                maxWidth: '720px'
            }}>
                <h1 style={{ marginBottom: '12px' }}>Dashboard Load Error</h1>
                <p style={{ marginBottom: '16px', color: 'var(--text-secondary)' }}>
                    There was a problem fetching dashboard data.
                </p>
                <pre style={{
                    background: 'rgba(255,255,255,0.06)',
                    border: '1px solid rgba(255,255,255,0.08)',
                    borderRadius: '14px',
                    padding: '18px',
                    overflowX: 'auto',
                    color: 'var(--text)'
                }}>
                    {error}
                </pre>
            </div>
        );
    }

    return (

        <div className="page-shell">

            <h1 style={{ marginBottom: '8px' }}>
                Dashboard Overview
            </h1>
            
            <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
                Real-time monitoring of your Docker infrastructure
            </p>

            <div className="section-title">
                Infrastructure Status
            </div>

            <div className="grid">

                <StatCard
                    title="Hosts"
                    value={summary?.hosts ?? 0}
                    gradientClass="gradient-1"
                    onClick={() => navigate("/hosts")}
                />

                <StatCard
                    title="Containers"
                    value={
                        summary?.containers ?? 0
                    }
                    gradientClass="gradient-3"
                    onClick={() => navigate("/containers", { state: { filter: "all" } })}
                />

                <StatCard
                    title="Running"
                    value={summary?.running ?? 0}
                    gradientClass="gradient-4"
                    onClick={() => navigate("/containers", { state: { filter: "running" } })}
                />

                <StatCard
                    title="Stopped"
                    value={summary?.stopped ?? 0}
                    gradientClass="gradient-2"
                    onClick={() => navigate("/containers", { state: { filter: "stopped" } })}
                />

            </div>

            <div className="section-title">
                Security & Compliance
            </div>

            <div className="grid">

                <StatCard
                    title="Findings"
                    value={
                        summary?.findings ?? 0
                    }
                    gradientClass="gradient-5"
                    onClick={() => navigate("/findings")}
                />

                <StatCard
                    title="Remediations"
                    value={
                        summary?.remediations ?? 0
                    }
                    gradientClass="gradient-6"
                    onClick={() => navigate("/approvals")}
                />

                <StatCard
                    title="Incidents"
                    value={
                        summary?.incidents ?? 0
                    }
                    gradientClass="gradient-2"
                    onClick={() => navigate("/incidents")}
                />

                <StatCard
                    title="Drift Findings"
                    value={
                        summary?.drift_findings ?? 0
                    }
                    gradientClass="gradient-8"
                    onClick={() => navigate("/drift")}
                />

            </div>

            <div className="section-title">
                Recent Activity
            </div>

            <ActivityFeed />

        </div>
    );
}