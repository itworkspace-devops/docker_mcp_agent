import { useState } from "react";
import { Send, Loader, MessageCircle, AlertCircle, CheckCircle2 } from "lucide-react";
import { api } from "../services/api";

interface Message {
    id: string;
    query: string;
    response: any;
    timestamp: string;
    loading?: boolean;
}

export default function Agent() {
    const [query, setQuery] = useState("");
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);

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
            const res = await api.post("/docker-agent/query", { query });
            
            setMessages(prev =>
                prev.map(msg =>
                    msg.id === userMessage.id
                        ? { ...msg, response: res.data, loading: false }
                        : msg
                )
            );
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

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            execute();
        }
    };

    return (
        <div className="page-shell" style={{
            display: 'flex',
            flexDirection: 'column',
            minHeight: 'calc(100vh - 210px)',
            gap: '20px',
            paddingBottom: '24px'
        }}>
            {/* Header */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '16px'
            }}>
                <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '12px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
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
                                    maxWidth: '70%'
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
                                        ) : (
                                            <div>
                                                {msg.response.status === 'success' && (
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
                                                    maxHeight: '300px',
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
                
                <style>{`
                    @keyframes slideIn {
                        from {
                            opacity: 0;
                            transform: translateY(10px);
                        }
                        to {
                            opacity: 1;
                            transform: translateY(0);
                        }
                    }
                    @keyframes spin {
                        from {
                            transform: rotate(0deg);
                        }
                        to {
                            transform: rotate(360deg);
                        }
                    }
                `}</style>
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
                    onFocus={(e) => {
                        e.currentTarget.style.borderColor = 'var(--primary)';
                        e.currentTarget.style.boxShadow = '0 0 0 3px rgba(99, 102, 241, 0.1)';
                    }}
                    onBlur={(e) => {
                        e.currentTarget.style.borderColor = 'var(--card-border)';
                        e.currentTarget.style.boxShadow = 'none';
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
                        transition: 'all 0.3s ease',
                        height: 'fit-content',
                        opacity: loading || !query.trim() ? 0.6 : 1,
                        transform: loading ? 'scale(0.98)' : 'scale(1)'
                    }}
                    onMouseEnter={(e) => {
                        if (!loading && query.trim()) {
                            e.currentTarget.style.transform = 'scale(1.05)';
                            e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
                        }
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)';
                        e.currentTarget.style.boxShadow = 'none';
                    }}
                >
                    {loading ? (
                        <>
                            <Loader size={18} style={{ animation: 'spin 1s linear infinite' }} />
                            Thinking...
                        </>
                    ) : (
                        <>
                            <Send size={18} />
                            Send
                        </>
                    )}
                </button>
            </div>
        </div>
    );
}