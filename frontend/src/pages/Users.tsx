import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { createUser, fetchUsers } from "../services/auth";
import type { UserItem } from "../services/auth";

const availableRoles = ["viewer", "operator", "admin"];

export default function Users() {
    const authContext = useContext(AuthContext);
    const [users, setUsers] = useState<UserItem[]>([]);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("viewer");
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    if (!authContext) {
        return null;
    }

    const auth = authContext.auth;

    useEffect(() => {
        if (!auth) {
            return;
        }

        fetchUsers(auth.token)
            .then(setUsers)
            .catch((err) => {
                setError(err?.response?.data?.detail || "Could not load users.");
            });
    }, [auth]);

    const handleCreateUser = async (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);
        setSuccess(null);

        if (!auth) {
            setError("Authentication required.");
            return;
        }

        if (!username || !password) {
            setError("Username and password are required.");
            return;
        }

        try {
            const created = await createUser(
                { username, password, role },
                auth.token,
            );

            setUsers((current) => [...current, created]);
            setSuccess(`Created user ${created.username} with role ${created.role}.`);
            setUsername("");
            setPassword("");
            setRole("viewer");
        } catch (err: any) {
            setError(err?.response?.data?.detail || "Failed to create user.");
        }
    };

    return (
        <div className="page-shell">
            <div className="page-heading" style={{ marginBottom: '20px' }}>
                <div>
                    <h1 style={{ marginBottom: '8px' }}>User management</h1>
                    <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
                        Admins can create users with roles and manage access in one place.
                    </p>
                </div>
            </div>

            <div className="card user-form-card" style={{ marginBottom: '24px' }}>
                <div className="card-title">Create user</div>
                <form onSubmit={handleCreateUser} className="form-grid">
                    <label className="form-row">
                        <span>Username</span>
                        <input
                            type="text"
                            value={username}
                            onChange={(event) => setUsername(event.target.value)}
                            placeholder="Enter username"
                        />
                    </label>

                    <label className="form-row">
                        <span>Password</span>
                        <input
                            type="password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            placeholder="Enter temporary password"
                        />
                    </label>

                    <label className="form-row">
                        <span>Role</span>
                        <select value={role} onChange={(event) => setRole(event.target.value)}>
                            {availableRoles.map((item) => (
                                <option key={item} value={item}>
                                    {item}
                                </option>
                            ))}
                        </select>
                    </label>

                    <div className="form-feedback">
                        {error && <div className="form-error">{error}</div>}
                        {success && <div className="form-success">{success}</div>}
                    </div>

                    <button type="submit">Create user</button>
                </form>
            </div>

            <div className="section-title">Existing users</div>
            <div className="card">
                <table className="table">
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Role</th>
                            <th>Password changed</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map((user) => (
                            <tr key={user.username}>
                                <td>{user.username}</td>
                                <td>{user.role}</td>
                                <td>{user.password_changed ? "Yes" : "No"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
