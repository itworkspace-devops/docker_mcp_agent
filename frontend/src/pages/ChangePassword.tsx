import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { changePassword } from "../services/auth";

export default function ChangePassword() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();

    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    if (!authContext) {
        return null;
    }

    const auth = authContext.auth;

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);
        setSuccess(null);

        if (!auth) {
            setError("Authentication required.");
            return;
        }

        if (!newPassword || newPassword !== confirmPassword) {
            setError("Passwords must match and cannot be empty.");
            return;
        }

        setLoading(true);

        try {
            await changePassword(auth.token, newPassword);
            authContext.updateAuth({ password_changed: true });
            setSuccess("Password updated successfully. Redirecting to dashboard...");
            setTimeout(() => navigate("/"), 1200);
        } catch (err: any) {
            setError(err?.response?.data?.detail || "Unable to update password.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-shell">
            <div className="login-card">
                <h1>Change password</h1>
                <p>Set a new secure password for your account.</p>

                <form onSubmit={handleSubmit}>
                    <label>
                        New password
                        <input
                            type={showNewPassword ? "text" : "password"}
                            value={newPassword}
                            onChange={(event) => setNewPassword(event.target.value)}
                            autoComplete="new-password"
                        />
                    </label>

                    <div className="password-toggle">
                        <label>
                            <input
                                type="checkbox"
                                checked={showNewPassword}
                                onChange={() => setShowNewPassword(!showNewPassword)}
                            />
                            Show new password
                        </label>
                    </div>

                    <label>
                        Confirm password
                        <input
                            type={showConfirmPassword ? "text" : "password"}
                            value={confirmPassword}
                            onChange={(event) => setConfirmPassword(event.target.value)}
                            autoComplete="new-password"
                        />
                    </label>

                    <div className="password-toggle">
                        <label>
                            <input
                                type="checkbox"
                                checked={showConfirmPassword}
                                onChange={() => setShowConfirmPassword(!showConfirmPassword)}
                            />
                            Show confirm password
                        </label>
                    </div>

                    {error && <div className="form-error">{error}</div>}
                    {success && <div className="form-success">{success}</div>}

                    <button type="submit" disabled={loading}>
                        {loading ? "Saving..." : "Save password"}
                    </button>
                </form>
            </div>
        </div>
    );
}
