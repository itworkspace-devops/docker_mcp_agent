import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { login as loginRequest } from "../services/auth";

export default function Login() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();

    const [username, setUsername] = useState("admin");
    const [password, setPassword] = useState("admin");
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    if (!authContext) {
        return null;
    }

    const { login } = authContext;

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const result = await loginRequest({ username, password });
            login(result);

            if (result.change_required) {
                navigate("/change-password");
            } else {
                navigate("/");
            }
        } catch (err: any) {
            setError(err?.response?.data?.detail || "Login failed. Please check your credentials.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-shell">
            <div className="login-card">
                <h1>Welcome back</h1>
                <p>Sign in with your Docker AI account to continue.</p>

                <form onSubmit={handleSubmit}>
                    <label>
                        Username
                        <input
                            type="text"
                            value={username}
                            onChange={(event) => setUsername(event.target.value)}
                            autoComplete="username"
                        />
                    </label>

                    <label>
                        Password
                        <input
                            type={showPassword ? "text" : "password"}
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            autoComplete="current-password"
                        />
                    </label>

                    <div className="password-toggle">
                        <label>
                            <input
                                type="checkbox"
                                checked={showPassword}
                                onChange={() => setShowPassword(!showPassword)}
                            />
                            Show password
                        </label>
                    </div>

                    {error && <div className="form-error">{error}</div>}

                    <button type="submit" disabled={loading}>
                        {loading ? "Signing in..." : "Sign in"}
                    </button>
                </form>

                <div className="login-note">
                    Use default admin credentials: <strong>admin / admin</strong>
                </div>
            </div>
        </div>
    );
}
