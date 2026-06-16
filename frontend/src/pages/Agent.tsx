import { useEffect, useState } from "react";
import { Send, Loader, MessageCircle, AlertCircle, CheckCircle2, ShieldAlert, XCircle, Plus, History } from "lucide-react";
import { api } from "../services/api";

interface Message {
    id: string;
    query: string;
    response: any;
    timestamp: string;
    loading?: boolean;
}

interface Session {
    id: string;
    title: string;
    created_at: string;
}

export default function Agent() {
    const [query, setQuery] = useState("");
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);
    const [sessions, setSessions] = useState<Session[]>([]);
    const [currentSessionId, setCurrentSessionId] = useState<string>(() => {
        return localStorage.getItem("chat_session_id") || `session_${Date.now()}`;
    });

    const loadSessions = async () => {
        try {
            const res = await api.get("/chat/sessions");
            setSessions(res.data);
        } catch (err) {
            console.error("Failed to load sessions", err);
        }
    };

    const loadMessages = async (sessionId: string) => {
        try {
            const res = await api.get(`/chat/sessions/${sessionId}/messages`);
            const history = res.data.map((m: any, idx: number) => {
                if (m.role === 'user') {
                    // Find next agent message
                    const nextMsg = res.data[idx+1];
                    if (nextMsg && nextMsg.role === 'agent') {
                        return {
                            id: m.id.toString(),
                            query: m.content,
                            response: JSON.parse(nextMsg.content.startsWith('{') ? nextMsg.content : JSON.stringify(nextMsg.content)),
                            timestamp: new Date(m.created_at).toLocaleTimeString(),
                            loading: false
                        };
                    } else {
                         return {
                            id: m.id.toString(),
                            query: m.content,
                            response: null,
                            timestamp: new Date(m.created_at).toLocaleTimeString(),
                            loading: false
                        };
                    }
                }
                return null;
            }).filter((m: any) => m !== null);
            
            setMessages(history);
        } catch (err) {
            console.error("Failed to load messages", err);
        }
    };

    useEffect(() => {
        loadSessions();
        loadMessages(currentSessionId);
    }, []);

    useEffect(() => {
        localStorage.setItem("chat_session_id", currentSessionId);
    }, [currentSessionId]);

    const createNewSession = () => {
        const newId = `session_${Date.now()}`;
        setCurrentSessionId(newId);
        setMessages([]);
    };

    const selectSession = (sessionId: string) => {
        setCurrentSessionId(sessionId);
        loadMessages(sessionId);
    };

    const execute = async () => {
        if (!query.trim()) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            query,
            response: null,
            timestamp: new Date().toLocaleTimeString(),
            loading: true
        };

        setMessages([...messages, userMessage]);
        setQuery("");
        setLoading(true);

        try {
            const res = await api.post("/docker-agent/query", { 
                query,
                session_id: currentSessionId
            });
            
            setMessages(prev =>
                prev.map(msg =>
                    msg.id === userMessage.id
                        ? { ...msg, response: res.data.response, loading: false }
                        : msg
                )
            );
            loadSessions(); // Refresh sessions to update titles/list
        } catch (err: any) {
            const errorMessage = err?.response?.data?.detail || err?.message || "Failed to get response from agent";
            setMessages(prev =>
                prev.map(msg =>
                    msg.id === userMessage.id
                        ? { 
                            ...msg, 
                            response: { error: errorMessage }, 
                            loading: false 
                          }
                        : msg
                )
            );
        } finally {
            setLoading(false);
        }
    };

    const handleApproval = async (messageId: string, executionId: string, approved: boolean) => {
        try {
            const endpoint = approved 
                ? `/approval/approve/${executionId}` 
                : `/approval/${executionId}/reject`;
            
            const res = await api.post(endpoint);
            
            setMessages(prev =>
                prev.map(msg =>
                    msg.id === messageId
                        ? { 
                            ...msg, 
                            response: approved ? (res.data.result || res.data) : { error: "Action rejected by user" }
                          }
                        : msg
                )
            );
        } catch (err: any) {
            console.error("Failed to process approval", err);
            alert("Failed to process approval: " + (err.message || "Unknown error"));
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            execute();
        }
    };

    return (
        <div className="page-shell" style={{
            display: 'flex',
            height: 'calc(100vh - 160px)',
            gap: '20px',
            paddingBottom: '24px',
            overflow: 'hidden'
        }}>
            {/* Sidebar */}
            <div style={{
                width: '260px',
                background: 'var(--card)',
                border: '1px solid var(--card-border)',
                borderRadius: '16px',
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden'
            }}>
                <div style={{ padding: '16px', borderBottom: '1px solid var(--card-border)' }}>
                    <button 
                        onClick={createNewSession}
                        style={{
                            width: '100%',
                            padding: '10px',
                            background: 'var(--primary)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '8px',
                            fontWeight: '600'
                        }}
                    >
                        <Plus size={18} />
                        New Chat
                    </button>
                </div>
                <div style={{ flex: 1, overflowY: 'auto', padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', fontSize: '12px', marginBottom: '8px', padding: '0 4px' }}>
                        <History size={14} />
                        Recent History (15d)
                    </div>
                    {sessions.map(s => (
                        <div 
                            key={s.id}
                            onClick={() => selectSession(s.id)}
                            style={{
                                padding: '10px 12px',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                background: currentSessionId === s.id ? 'rgba(99, 102, 241, 0.1)' : 'transparent',
                                border: currentSessionId === s.id ? '1px solid var(--primary)' : '1px solid transparent',
                                transition: 'all 0.2s ease',
                                fontSize: '13px',
                                color: currentSessionId === s.id ? 'var(--text)' : 'var(--text-secondary)',
                                whiteSpace: 'nowrap',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis'
                            }}
                            onMouseEnter={e => {
                                if (currentSessionId !== s.id) e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
                            }}
                            onMouseLeave={e => {
                                if (currentSessionId !== s.id) e.currentTarget.style.background = 'transparent';
                            }}
                        >
                            {s.title}
                        </div>
                    ))}
                    {sessions.length === 0 && (
                        <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-muted)', fontSize: '12px' }}>
                            No history found
                        </div>
                    )}
                </div>
            </div>

            {/* Chat Area */}
            <div style={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                gap: '20px',
                height: '100%'
            }}>
                {/* Header */}
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px'
                }}>
                    <div style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '12px',
                        background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white'
                    }}>
                        🤖
                    </div>
                    <div>
                        <h1 style={{ margin: 0, fontSize: '24px', fontWeight: '700' }}>Docker AI Agent</h1>
                        <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '13px' }}>
                            Ask questions about your Docker infrastructure
                        </p>
                    </div>
                </div>

                {/* Chat Messages Area */}
                <div style={{
                    flex: 1,
                    overflowY: 'auto',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '16px',
                    paddingBottom: '16px',
                    borderRadius: '16px',
                    background: 'rgba(20, 24, 41, 0.5)',
                    border: '1px solid var(--card-border)',
                    padding: '20px'
                }}>
                    {messages.length === 0 ? (
                        <div style={{
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            height: '100%',
                            color: 'var(--text-secondary)',
                            textAlign: 'center'
                        }}>
                            <MessageCircle size={48} style={{ opacity: 0.4, marginBottom: '16px' }} />
                            <p style={{ fontSize: '16px', fontWeight: '500' }}>No messages yet</p>
                            <p style={{ fontSize: '14px', opacity: 0.7 }}>Start by asking the agent a question</p>
                        </div>
                    ) : (
                        messages.map((msg) => (
                            <div key={msg.id} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                {/* User Message */}
                                <div style={{
                                    display: 'flex',
                                    justifyContent: 'flex-end',
                                    animation: 'slideIn 0.3s ease'
                                }}>
                                    <div style={{
                                        maxWidth: '70%',
                                        background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                        color: 'white',
                                        padding: '14px 18px',
                                        borderRadius: '16px',
                                        borderBottomRightRadius: '4px',
                                        wordWrap: 'break-word',
                                        boxShadow: 'var(--shadow-md)'
                                    }}>
                                        <p style={{ margin: 0, fontSize: '14px', lineHeight: '1.5' }}>{msg.query}</p>
                                        <p style={{
                                            margin: '6px 0 0 0',
                                            fontSize: '11px',
                                            opacity: 0.8
                                        }}>{msg.timestamp}</p>
                                    </div>
                                </div>

                                {/* Agent Response */}
                                {msg.loading ? (
                                    <div style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '10px',
                                        padding: '14px 18px',
                                        background: 'var(--card)',
                                        borderRadius: '16px',
                                        borderBottomLeftRadius: '4px',
                                        border: '1px solid var(--card-border)',
                                        maxWidth: '70%'
                                    }}>
                                        <Loader size={18} style={{ animation: 'spin 1s linear infinite' }} />
                                        <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                                            Agent is thinking...
                                        </span>
                                    </div>
                                ) : msg.response ? (
                                    <div style={{
                                        display: 'flex',
                                        justifyContent: 'flex-start',
                                        maxWidth: '85%'
                                    }}>
                                        <div style={{
                                            width: '100%',
                                            background: 'var(--card)',
                                            border: '1px solid var(--card-border)',
                                            borderRadius: '16px',
                                            borderBottomLeftRadius: '4px',
                                            padding: '16px',
                                            boxShadow: 'var(--shadow-md)'
                                        }}>
                                            {msg.response.error ? (
                                                <div style={{
                                                    display: 'flex',
                                                    gap: '10px',
                                                    alignItems: 'flex-start'
                                                }}>
                                                    <AlertCircle size={18} style={{ color: '#ef4444', marginTop: '2px', flexShrink: 0 }} />
                                                    <div>
                                                        <p style={{
                                                            margin: 0,
                                                            fontSize: '14px',
                                                            color: '#ef4444',
                                                            fontWeight: '500'
                                                        }}>Error</p>
                                                        <p style={{
                                                            margin: '4px 0 0 0',
                                                            fontSize: '13px',
                                                            color: 'var(--text-secondary)'
                                                        }}>{msg.response.error}</p>
                                                    </div>
                                                </div>
                                            ) : msg.response.action === 'approval_required' ? (
                                                <div style={{
                                                    display: 'flex',
                                                    flexDirection: 'column',
                                                    gap: '12px'
                                                }}>
                                                    <div style={{
                                                        display: 'flex',
                                                        gap: '10px',
                                                        alignItems: 'center',
                                                        color: '#f59e0b'
                                                    }}>
                                                        <ShieldAlert size={20} />
                                                        <span style={{ fontWeight: '600', fontSize: '15px' }}>Approval Required</span>
                                                    </div>
                                                    <div style={{
                                                        padding: '12px',
                                                        background: 'rgba(245, 158, 11, 0.05)',
                                                        border: '1px solid rgba(245, 158, 11, 0.2)',
                                                        borderRadius: '8px',
                                                        fontSize: '13px'
                                                    }}>
                                                        <p style={{ margin: '0 0 8px 0', fontWeight: '500' }}>
                                                            The agent wants to execute: <code style={{ color: '#f59e0b' }}>{msg.response.tool_name}</code>
                                                        </p>
                                                        <pre style={{
                                                            margin: 0,
                                                            fontSize: '12px',
                                                            opacity: 0.8,
                                                            overflowX: 'auto'
                                                        }}>
                                                            {JSON.stringify(msg.response.tool_args, null, 2)}
                                                        </pre>
                                                    </div>
                                                    <div style={{ display: 'flex', gap: '12px', marginTop: '4px' }}>
                                                        <button 
                                                            onClick={() => handleApproval(msg.id, msg.response.execution_id, true)}
                                                            style={{
                                                                flex: 1,
                                                                padding: '10px',
                                                                background: 'var(--success)',
                                                                color: 'white',
                                                                border: 'none',
                                                                borderRadius: '8px',
                                                                cursor: 'pointer',
                                                                fontWeight: '600',
                                                                display: 'flex',
                                                                alignItems: 'center',
                                                                justifyContent: 'center',
                                                                gap: '8px'
                                                            }}
                                                        >
                                                            <CheckCircle2 size={16} />
                                                            Approve
                                                        </button>
                                                        <button 
                                                            onClick={() => handleApproval(msg.id, msg.response.execution_id, false)}
                                                            style={{
                                                                flex: 1,
                                                                padding: '10px',
                                                                background: '#ef4444',
                                                                color: 'white',
                                                                border: 'none',
                                                                borderRadius: '8px',
                                                                cursor: 'pointer',
                                                                fontWeight: '600',
                                                                display: 'flex',
                                                                alignItems: 'center',
                                                                justifyContent: 'center',
                                                                gap: '8px'
                                                            }}
                                                        >
                                                            <XCircle size={16} />
                                                            Reject
                                                        </button>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div>
                                                    {msg.response.success === true && (
                                                        <div style={{
                                                            display: 'flex',
                                                            gap: '8px',
                                                            marginBottom: '12px',
                                                            padding: '8px 12px',
                                                            background: 'rgba(16, 185, 129, 0.1)',
                                                            borderRadius: '8px',
                                                            alignItems: 'center'
                                                        }}>
                                                            <CheckCircle2 size={16} style={{ color: 'var(--success)' }} />
                                                            <span style={{ fontSize: '12px', color: 'var(--success)' }}>Success</span>
                                                        </div>
                                                    )}
                                                    <div style={{
                                                        background: 'rgba(0, 0, 0, 0.2)',
                                                        padding: '12px',
                                                        borderRadius: '8px',
                                                        fontFamily: 'monospace',
                                                        fontSize: '12px',
                                                        color: 'var(--text)',
                                                        maxHeight: '400px',
                                                        overflowY: 'auto',
                                                        lineHeight: '1.6',
                                                        whiteSpace: 'pre-wrap',
                                                        wordBreak: 'break-word'
                                                    }}>
                                                        {typeof msg.response === 'string'
                                                            ? msg.response
                                                            : JSON.stringify(msg.response, null, 2)
                                                        }
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ) : null}
                            </div>
                        ))
                    )}
                </div>

                {/* Input Area */}
                <div style={{
                    display: 'flex',
                    gap: '12px',
                    padding: '20px',
                    background: 'linear-gradient(135deg, var(--card) 0%, var(--card-hover) 100%)',
                    border: '1px solid var(--card-border)',
                    borderRadius: '16px',
                    boxShadow: 'var(--shadow-md)'
                }}>
                    <textarea
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask me about your Docker infrastructure... (Ctrl+Enter to send)"
                        style={{
                            flex: 1,
                            padding: '14px',
                            borderRadius: '12px',
                            border: '1px solid var(--card-border)',
                            background: 'rgba(10, 14, 39, 0.8)',
                            color: 'var(--text)',
                            fontSize: '14px',
                            fontFamily: 'inherit',
                            resize: 'none',
                            outline: 'none',
                            transition: 'all 0.3s ease',
                            maxHeight: '120px',
                            minHeight: '48px'
                        }}
                    />
                    <button
                        onClick={execute}
                        disabled={loading || !query.trim()}
                        style={{
                            padding: '12px 24px',
                            background: loading ? 'var(--text-muted)' : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '12px',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            fontSize: '14px',
                            fontWeight: '600',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '8px',
                            height: 'fit-content',
                            opacity: loading || !query.trim() ? 0.6 : 1
                        }}
                    >
                        {loading ? <Loader size={18} className="spin" /> : <Send size={18} />}
                        {loading ? 'Thinking...' : 'Send'}
                    </button>
                </div>
            </div>
            
            <style>{`
                @keyframes slideIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
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
