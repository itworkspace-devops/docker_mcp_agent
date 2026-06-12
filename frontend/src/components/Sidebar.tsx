import { Link } from "react-router-dom";

export default function Sidebar() {
    return (
        <div className="sidebar">

            <h2>Docker AI</h2>

            <Link to="/">Dashboard</Link>

            <Link to="/fleet">Fleet</Link>

            <Link to="/findings">Findings</Link>

            <Link to="/compliance">Compliance</Link>

            <Link to="/incidents">Incidents</Link>

            <Link to="/drift">Drift</Link>

            <Link to="/agent">AI Agent</Link>

        </div>
    );
}