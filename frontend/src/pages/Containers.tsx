import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Zap, Server, Activity, ShieldAlert, RefreshCcw, ChevronDown, ChevronRight, Search, Filter } from "lucide-react";
import { api } from "../services/api";

interface ContainerInfo {
    id: string;
    name: string;
    status: string;
    image: string[];
}

interface HostContainers {
    host: string;
    containers?: {
        success: boolean;
        data: ContainerInfo[];
        error: string | null;
    };
    error?: string;
}

export default function Containers() {
    const location = useLocation();
    const [data, setData] = useState<HostContainers[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [collapsedHosts, setCollapsedHosts] = useState<Record<string, boolean>>({});
    const [searchQuery, setSearchQuery] = useState("");
    const [statusFilter, setStatusFilter] = useState<string>("all");

    useEffect(() => {
        const state = location.state as { filter?: string };
        if (state?.filter) {
            setStatusFilter(state.filter);
        }
    }, [location]);

    const loadContainers = async () => {
        try {
            setLoading(true);
            setError(null);
            const res = await api.get("/fleet/containers");
            setData(res.data);
        } catch (err: any) {
            console.error("Failed to load containers", err);
            setError(err.message || "Unable to load container data");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadContainers();
    }, []);

    const toggleHost = (hostName: string) => {
        setCollapsedHosts(prev => ({
            ...prev,
            [hostName]: !prev[hostName]
        }));
    };

    const filterContainers = (containers: ContainerInfo[]) => {
        return containers.filter(c => {
            const matchesSearch = c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                                 c.image.some(img => img.toLowerCase().includes(searchQuery.toLowerCase())) ||
                                 c.id.toLowerCase().includes(searchQuery.toLowerCase());
            
            const matchesStatus = statusFilter === "all" || 
                                 (statusFilter === "running" && c.status.toLowerCase().startsWith("running")) ||
                                 (statusFilter === "stopped" && !c.status.toLowerCase().startsWith("running"));
            
            return matchesSearch && matchesStatus;
        });
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '400px' }}>
                <div style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                    <RefreshCcw size={40} className="spin" style={{ marginBottom: '16px', opacity: 0.6 }} />
                    <p>Loading containers across fleet...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="page-shell">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <div>
                    <h1 style={{ margin: 0 }}>Containers Fleet</h1>
                    <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
                        Manage and monitor containers across all hosts
                    </p>
                </div>
                <div style={{ display: 'flex', gap: '12px' }}>
                    <button 
                        onClick={loadContainers}
                        style={{
                            padding: '8px 16px',
                            background: 'rgba(99, 102, 241, 0.1)',
                            border: '1px solid var(--primary)',
                            color: 'var(--primary)',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            fontSize: '14px',
                            fontWeight: '500'
                        }}
                    >
                        <RefreshCcw size={16} />
                        Refresh
                    </button>
                </div>
            </div>

            <div style={{ 
                display: 'flex', 
                gap: '16px', 
                marginBottom: '24px',
                flexWrap: 'wrap'
            }}>
                <div style={{ 
                    flex: 1, 
                    minWidth: '300px',
                    position: 'relative'
                }}>
                    <Search size={18} style={{ 
                        position: 'absolute', 
                        left: '12px', 
                        top: '50%', 
                        transform: 'translateY(-50%)',
                        color: 'var(--text-muted)'
                    }} />
                    <input 
                        type="text"
                        placeholder="Search containers by name, image, or ID..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        style={{
                            width: '100%',
                            padding: '10px 12px 10px 40px',
                            background: 'var(--card)',
                            border: '1px solid var(--card-border)',
                            borderRadius: '10px',
                            color: 'var(--text)',
                            fontSize: '14px'
                        }}
                    />
                </div>
                
                <div style={{ display: 'flex', gap: '8px', background: 'var(--card)', padding: '4px', borderRadius: '10px', border: '1px solid var(--card-border)' }}>
                    <button 
                        onClick={() => setStatusFilter("all")}
                        style={{
                            padding: '6px 16px',
                            borderRadius: '8px',
                            border: 'none',
                            background: statusFilter === "all" ? 'var(--primary)' : 'transparent',
                            color: statusFilter === "all" ? 'white' : 'var(--text-secondary)',
                            cursor: 'pointer',
                            fontSize: '13px',
                            fontWeight: '500'
                        }}
                    >
                        All
                    </button>
                    <button 
                        onClick={() => setStatusFilter("running")}
                        style={{
                            padding: '6px 16px',
                            borderRadius: '8px',
                            border: 'none',
                            background: statusFilter === "running" ? 'var(--success)' : 'transparent',
                            color: statusFilter === "running" ? 'white' : 'var(--text-secondary)',
                            cursor: 'pointer',
                            fontSize: '13px',
                            fontWeight: '500'
                        }}
                    >
                        Running
                    </button>
                    <button 
                        onClick={() => setStatusFilter("stopped")}
                        style={{
                            padding: '6px 16px',
                            borderRadius: '8px',
                            border: 'none',
                            background: statusFilter === "stopped" ? '#ef4444' : 'transparent',
                            color: statusFilter === "stopped" ? 'white' : 'var(--text-secondary)',
                            cursor: 'pointer',
                            fontSize: '13px',
                            fontWeight: '500'
                        }}
                    >
                        Stopped
                    </button>
                </div>
            </div>

            {error && (
                <div style={{ 
                    padding: '16px', 
                    background: 'rgba(239, 68, 68, 0.1)', 
                    border: '1px solid #ef4444', 
                    borderRadius: '12px',
                    color: '#ef4444',
                    marginBottom: '24px',
                    display: 'flex',
                    gap: '12px',
                    alignItems: 'center'
                }}>
                    <ShieldAlert size={20} />
                    <span>{error}</span>
                </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
                {data.map((hostData, idx) => {
                    const isCollapsed = collapsedHosts[hostData.host];
                    const containers = hostData.containers?.data || [];
                    const filteredContainers = filterContainers(containers);
                    
                    if (statusFilter !== "all" && filteredContainers.length === 0 && searchQuery === "") {
                        // Optionally hide hosts with no matching containers when filtering by status
                        // return null;
                    }

                    return (
                        <div key={idx} className="host-section">
                            <div 
                                onClick={() => toggleHost(hostData.host)}
                                style={{ 
                                    display: 'flex', 
                                    alignItems: 'center', 
                                    justifyContent: 'space-between',
                                    cursor: 'pointer',
                                    paddingBottom: isCollapsed ? '0' : '8px',
                                    borderBottom: isCollapsed ? 'none' : '1px solid var(--card-border)',
                                    marginBottom: isCollapsed ? '0' : '16px',
                                }}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                    <Server size={20} style={{ color: 'var(--primary)' }} />
                                    <h2 style={{ margin: 0, fontSize: '18px' }}>
                                        Host: {hostData.host}
                                        <span style={{ 
                                            marginLeft: '12px', 
                                            fontSize: '14px', 
                                            fontWeight: 'normal', 
                                            color: 'var(--text-secondary)',
                                            background: 'rgba(255, 255, 255, 0.05)',
                                            padding: '2px 8px',
                                            borderRadius: '12px'
                                        }}>
                                            {filteredContainers.length} {statusFilter !== "all" ? statusFilter : ""} Containers
                                        </span>
                                    </h2>
                                </div>
                                {isCollapsed ? <ChevronRight size={20} /> : <ChevronDown size={20} />}
                            </div>

                            {!isCollapsed && (
                                <>
                                    {hostData.error || (hostData.containers && !hostData.containers.success) ? (
                                        <div style={{ color: '#ef4444', padding: '12px', background: 'rgba(239, 68, 68, 0.05)', borderRadius: '8px' }}>
                                            Error: {hostData.error || hostData.containers?.error}
                                        </div>
                                    ) : (
                                        <div className="table-container">
                                            <table>
                                                <thead>
                                                    <tr>
                                                        <th>Name</th>
                                                        <th>Status</th>
                                                        <th>Image</th>
                                                        <th>ID</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {filteredContainers.length > 0 ? (
                                                        filteredContainers.map((container) => (
                                                            <tr key={container.id}>
                                                                <td style={{ fontWeight: '600' }}>
                                                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                                                        <Zap size={14} style={{ color: container.status.toLowerCase().startsWith('running') ? 'var(--success)' : 'var(--text-muted)' }} />
                                                                        {container.name}
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <span style={{
                                                                        padding: '4px 8px',
                                                                        borderRadius: '6px',
                                                                        fontSize: '12px',
                                                                        fontWeight: '600',
                                                                        background: container.status.toLowerCase().startsWith('running') ? 'rgba(16, 185, 129, 0.1)' : 'rgba(255, 255, 255, 0.05)',
                                                                        color: container.status.toLowerCase().startsWith('running') ? 'var(--success)' : 'var(--text-secondary)'
                                                                    }}>
                                                                        {container.status.toUpperCase()}
                                                                    </span>
                                                                </td>
                                                                <td style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
                                                                    {container.image && container.image.length > 0 ? container.image[0] : 'N/A'}
                                                                </td>
                                                                <td style={{ fontFamily: 'monospace', fontSize: '12px', opacity: 0.7 }}>
                                                                    {container.id}
                                                                </td>
                                                            </tr>
                                                        ))
                                                    ) : (
                                                        <tr>
                                                            <td colSpan={4} style={{ textAlign: 'center', padding: '24px', color: 'var(--text-secondary)' }}>
                                                                No containers found matching your filters
                                                            </td>
                                                        </tr>
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    )}
                                </>
                            )}
                        </div>
                    );
                })}
            </div>


            <style>{`
                .spin {
                    animation: spin 2s linear infinite;
                }
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
                .host-section {
                    background: var(--card);
                    border: 1px solid var(--card-border);
                    border-radius: 16px;
                    padding: 20px;
                    box-shadow: var(--shadow-sm);
                }
                .table-container {
                    overflow-x: auto;
                }
            `}</style>
        </div>
    );
}
