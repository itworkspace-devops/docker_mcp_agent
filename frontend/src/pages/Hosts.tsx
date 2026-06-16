import { useEffect, useState, useContext } from "react";
import { Server, Plus, Trash2, Edit2, ShieldCheck, ShieldAlert, Loader2, X, Check } from "lucide-react";
import { api } from "../services/api";
import { AuthContext } from "../context/AuthContext";

interface Host {
    id: number;
    name: string;
    host: string;
    port: number;
    enabled: boolean;
    created_at: string;
}

interface TestResult {
    success: boolean;
    message: string;
    loading: boolean;
}

export default function Hosts() {
    const authContext = useContext(AuthContext);
    const auth = authContext?.auth;
    const isAdmin = auth?.role === "admin";

    const [hosts, setHosts] = useState<Host[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showAddForm, setShowAddForm] = useState(false);
    
    // Form state for adding/editing
    const [editingId, setEditingId] = useState<number | null>(null);
    const [newName, setNewName] = useState("");
    const [newHost, setNewHost] = useState("");
    const [newPort, setNewPort] = useState(2375);
    const [newEnabled, setNewEnabled] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    
    // Test results state
    const [testResults, setTestResults] = useState<{[key: number]: TestResult}>({});

    const loadHosts = async () => {
        try {
            setLoading(true);
            const res = await api.get("/hosts");
            setHosts(res.data);
            setError(null);
        } catch (err: any) {
            console.error("Failed to load hosts", err);
            setError("Failed to fetch hosts list");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadHosts();
    }, []);

    const resetForm = () => {
        setNewName("");
        setNewHost("");
        setNewPort(2375);
        setNewEnabled(true);
        setEditingId(null);
        setShowAddForm(false);
    };

    const handleAddHost = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError(null);

        try {
            if (editingId) {
                await api.put(`/hosts/${editingId}`, {
                    name: newName,
                    host: newHost,
                    port: newPort,
                    enabled: newEnabled
                });
            } else {
                await api.post("/hosts", {
                    name: newName,
                    host: newHost,
                    port: newPort
                });
            }
            
            resetForm();
            loadHosts();
        } catch (err: any) {
            console.error("Failed to save host", err);
            setError(err.response?.data?.detail || "Failed to save host. Make sure the name is unique.");
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleEditClick = (host: Host) => {
        setEditingId(host.id);
        setNewName(host.name);
        setNewHost(host.host);
        setNewPort(host.port);
        setNewEnabled(host.enabled);
        setShowAddForm(true);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleDeleteHost = async (hostId: number) => {
        if (!window.confirm("Are you sure you want to remove this host? This will stop monitoring for all containers on this node.")) {
            return;
        }

        try {
            await api.delete(`/hosts/${hostId}`);
            loadHosts();
        } catch (err: any) {
            console.error("Failed to delete host", err);
            setError("Failed to delete host");
        }
    };

    const handleTestConnectivity = async (host: Host) => {
        setTestResults(prev => ({
            ...prev,
            [host.id]: { success: false, message: "", loading: true }
        }));

        try {
            const res = await api.post("/hosts/test", {
                host: host.host,
                port: host.port
            });
            
            setTestResults(prev => ({
                ...prev,
                [host.id]: { 
                    success: res.data.success, 
                    message: res.data.message, 
                    loading: false 
                }
            }));

            // Clear result after 10 seconds
            setTimeout(() => {
                setTestResults(prev => {
                    const next = { ...prev };
                    delete next[host.id];
                    return next;
                });
            }, 10000);

        } catch (err: any) {
            setTestResults(prev => ({
                ...prev,
                [host.id]: { 
                    success: false, 
                    message: "Connection failed: Backend unreachable", 
                    loading: false 
                }
            }));
        }
    };

    const handleToggleStatus = async (host: Host) => {
        try {
            await api.put(`/hosts/${host.id}`, {
                name: host.name,
                host: host.host,
                port: host.port,
                enabled: !host.enabled
            });
            loadHosts();
        } catch (err: any) {
            console.error("Failed to toggle host status", err);
            setError("Failed to update host status");
        }
    };

    if (loading && hosts.length === 0) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
                <Loader2 className="spin" size={32} />
            </div>
        );
    }

    return (
        <div className="page-shell">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <div>
                    <h1 style={{ margin: 0 }}>Docker Hosts</h1>
                    <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
                        Manage your Docker infrastructure nodes
                    </p>
                </div>
                {isAdmin && (
                    <button 
                        onClick={() => {
                            if (showAddForm && editingId) {
                                resetForm();
                            } else {
                                setShowAddForm(!showAddForm);
                            }
                        }}
                        style={{
                            padding: '10px 20px',
                            background: showAddForm && editingId ? 'rgba(255,255,255,0.1)' : 'var(--primary-gradient)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '12px',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            fontWeight: '600',
                            boxShadow: 'var(--shadow-md)'
                        }}
                    >
                        {showAddForm && editingId ? <X size={18} /> : <Plus size={18} />}
                        {showAddForm && editingId ? "Cancel Edit" : "Add Host"}
                    </button>
                )}
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

            {isAdmin && showAddForm && (
                <div style={{ 
                    background: 'var(--card)', 
                    border: '1px solid var(--card-border)', 
                    borderRadius: '16px', 
                    padding: '24px', 
                    marginBottom: '32px',
                    animation: 'slideDown 0.3s ease',
                    boxShadow: 'var(--shadow-lg)',
                    borderLeft: '4px solid var(--primary)'
                }}>
                    <h3 style={{ marginTop: 0, marginBottom: '20px' }}>
                        {editingId ? `Edit Host: ${newName}` : "Register New Docker Host"}
                    </h3>
                    <form onSubmit={handleAddHost} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
                        <div className="form-group">
                            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: 'var(--text-secondary)' }}>Display Name</label>
                            <input 
                                type="text" 
                                value={newName}
                                onChange={(e) => setNewName(e.target.value)}
                                placeholder="e.g. Production Node 1"
                                required
                                style={{ width: '100%', padding: '12px', borderRadius: '8px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--card-border)', color: 'white' }}
                            />
                        </div>
                        <div className="form-group">
                            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: 'var(--text-secondary)' }}>Host IP / FQDN</label>
                            <input 
                                type="text" 
                                value={newHost}
                                onChange={(e) => setNewHost(e.target.value)}
                                placeholder="e.g. 192.168.1.10"
                                required
                                style={{ width: '100%', padding: '12px', borderRadius: '8px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--card-border)', color: 'white' }}
                            />
                        </div>
                        <div className="form-group">
                            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: 'var(--text-secondary)' }}>Docker API Port</label>
                            <input 
                                type="number" 
                                value={newPort}
                                onChange={(e) => setNewPort(parseInt(e.target.value))}
                                placeholder="2375"
                                required
                                style={{ width: '100%', padding: '12px', borderRadius: '8px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--card-border)', color: 'white' }}
                            />
                        </div>
                        {editingId && (
                            <div className="form-group">
                                <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: 'var(--text-secondary)' }}>Status</label>
                                <select 
                                    value={newEnabled ? "true" : "false"}
                                    onChange={(e) => setNewEnabled(e.target.value === "true")}
                                    style={{ width: '100%', padding: '12px', borderRadius: '8px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--card-border)', color: 'white' }}
                                >
                                    <option value="true">Enabled</option>
                                    <option value="false">Disabled</option>
                                </select>
                            </div>
                        )}
                        <div style={{ display: 'flex', alignItems: 'flex-end', gap: '12px' }}>
                            <button 
                                type="submit" 
                                disabled={isSubmitting}
                                style={{
                                    flex: 1,
                                    padding: '12px',
                                    background: 'var(--primary)',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '8px',
                                    cursor: isSubmitting ? 'not-allowed' : 'pointer',
                                    fontWeight: '600',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: '8px'
                                }}
                            >
                                {isSubmitting ? <Loader2 size={16} className="spin" /> : editingId ? <Check size={16} /> : <Plus size={16} />}
                                {isSubmitting ? 'Saving...' : editingId ? 'Update Host' : 'Register Host'}
                            </button>
                            <button 
                                type="button" 
                                onClick={resetForm}
                                style={{
                                    padding: '12px',
                                    background: 'rgba(255,255,255,0.05)',
                                    color: 'white',
                                    border: '1px solid var(--card-border)',
                                    borderRadius: '8px',
                                    cursor: 'pointer'
                                }}
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            )}

            <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
                {hosts.map((host) => (
                    <div key={host.id} className="host-card" style={{
                        background: 'var(--card)',
                        border: editingId === host.id ? '2px solid var(--primary)' : '1px solid var(--card-border)',
                        borderRadius: '16px',
                        padding: '20px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '16px',
                        transition: 'all 0.3s ease',
                        position: 'relative',
                        opacity: editingId && editingId !== host.id ? 0.6 : 1
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <div style={{ 
                                    width: '40px', 
                                    height: '40px', 
                                    borderRadius: '10px', 
                                    background: 'rgba(99, 102, 241, 0.1)', 
                                    display: 'flex', 
                                    alignItems: 'center', 
                                    justifyContent: 'center',
                                    color: 'var(--primary)'
                                }}>
                                    <Server size={24} />
                                </div>
                                <div>
                                    <h3 style={{ margin: 0, fontSize: '16px' }}>{host.name}</h3>
                                    <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>ID: {host.id}</span>
                                </div>
                            </div>
                            <div style={{
                                padding: '4px 8px',
                                borderRadius: '6px',
                                fontSize: '10px',
                                fontWeight: '700',
                                background: host.enabled ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                color: host.enabled ? 'var(--success)' : '#ef4444',
                                border: host.enabled ? '1px solid rgba(16, 185, 129, 0.2)' : '1px solid rgba(239, 68, 68, 0.2)'
                            }}>
                                {host.enabled ? 'ENABLED' : 'DISABLED'}
                            </div>
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                                <span style={{ color: 'var(--text-secondary)' }}>Host</span>
                                <span style={{ fontWeight: '500' }}>{host.host}</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                                <span style={{ color: 'var(--text-secondary)' }}>Port</span>
                                <span style={{ fontWeight: '500' }}>{host.port}</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                                <span style={{ color: 'var(--text-secondary)' }}>Created</span>
                                <span style={{ fontWeight: '500' }}>{new Date(host.created_at).toLocaleDateString()}</span>
                            </div>
                        </div>

                        <div style={{ 
                            marginTop: '8px', 
                            paddingTop: '16px', 
                            borderTop: '1px solid var(--card-border)',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '12px'
                        }}>
                            {testResults[host.id] && (
                                <div style={{
                                    padding: '8px 12px',
                                    borderRadius: '8px',
                                    fontSize: '12px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '8px',
                                    background: testResults[host.id].loading ? 'rgba(255,255,255,0.05)' : 
                                               testResults[host.id].success ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                    color: testResults[host.id].loading ? 'var(--text-secondary)' : 
                                           testResults[host.id].success ? 'var(--success)' : '#ef4444',
                                    border: `1px solid ${testResults[host.id].loading ? 'var(--card-border)' : 
                                           testResults[host.id].success ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'}`,
                                    animation: 'fadeIn 0.3s ease'
                                }}>
                                    {testResults[host.id].loading ? <Loader2 size={14} className="spin" /> : 
                                     testResults[host.id].success ? <Check size={14} /> : <X size={14} />}
                                    <span style={{ flex: 1 }}>{testResults[host.id].loading ? "Testing..." : testResults[host.id].message}</span>
                                </div>
                            )}

                            <div style={{ display: 'flex', gap: '8px' }}>
                                <button 
                                    onClick={() => handleTestConnectivity(host)}
                                    disabled={testResults[host.id]?.loading}
                                    style={{
                                        flex: 1,
                                        padding: '8px',
                                        background: 'rgba(255, 255, 255, 0.05)',
                                        border: '1px solid var(--card-border)',
                                        borderRadius: '8px',
                                        color: 'var(--text)',
                                        fontSize: '13px',
                                        cursor: testResults[host.id]?.loading ? 'not-allowed' : 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '6px'
                                    }}>
                                    <ShieldCheck size={14} />
                                    Test Connectivity
                                </button>

                                {isAdmin && (
                                    <button 
                                        onClick={() => handleToggleStatus(host)}
                                        style={{
                                            padding: '8px 12px',
                                            background: host.enabled ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)',
                                            border: `1px solid ${host.enabled ? '#ef4444' : 'var(--success)'}`,
                                            borderRadius: '8px',
                                            color: host.enabled ? '#ef4444' : 'var(--success)',
                                            fontSize: '12px',
                                            fontWeight: '600',
                                            cursor: 'pointer',
                                            minWidth: '80px'
                                        }}
                                    >
                                        {host.enabled ? 'Disable' : 'Enable'}
                                    </button>
                                )}
                            </div>
                            
                            {isAdmin && (
                                <div style={{ display: 'flex', gap: '8px' }}>
                                    <button 
                                        onClick={() => handleEditClick(host)}
                                        style={{
                                            flex: 1,
                                            padding: '8px 12px',
                                            background: 'rgba(99, 102, 241, 0.1)',
                                            border: '1px solid var(--primary)',
                                            borderRadius: '8px',
                                            color: 'var(--primary)',
                                            fontSize: '13px',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            gap: '6px'
                                        }}
                                    >
                                        <Edit2 size={14} />
                                        Edit Details
                                    </button>
                                    <button 
                                        onClick={() => handleDeleteHost(host.id)}
                                        style={{
                                            padding: '8px 12px',
                                            background: 'rgba(239, 68, 68, 0.1)',
                                            border: '1px solid #ef4444',
                                            borderRadius: '8px',
                                            color: '#ef4444',
                                            fontSize: '13px',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '6px'
                                        }}
                                    >
                                        <Trash2 size={14} />
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {hosts.length === 0 && (
                    <div style={{ 
                        gridColumn: '1 / -1', 
                        padding: '48px', 
                        textAlign: 'center', 
                        background: 'rgba(0,0,0,0.1)', 
                        borderRadius: '24px',
                        border: '2px dashed var(--card-border)',
                        color: 'var(--text-secondary)'
                    }}>
                        <Server size={48} style={{ opacity: 0.2, marginBottom: '16px' }} />
                        <h3>No Hosts Registered</h3>
                        <p>Get started by adding your first Docker host node.</p>
                    </div>
                )}
            </div>

            <style>{`
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                @keyframes slideDown {
                    from { opacity: 0; transform: translateY(-10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .host-card:hover {
                    transform: translateY(-4px);
                    box-shadow: var(--shadow-lg);
                }
                .spin {
                    animation: spin 1s linear infinite;
                }
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    );
}