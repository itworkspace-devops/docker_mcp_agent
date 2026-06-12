import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Dashboard from "./pages/Dashboard";
import Fleet from "./pages/Fleet";
import Findings from "./pages/Findings";
import Compliance from "./pages/Compliance";
import Drift from "./pages/Drift";
import Agent from "./pages/Agent";

import Incidents
from "./pages/Incidents";

<Route
    path="/incidents"
    element={<Incidents />}
/>

function App() {

    return (

        <BrowserRouter>

            <div className="layout">

                <Sidebar />

                <div className="content">

                    <Header />

                    <Routes>

                        <Route
                            path="/"
                            element={<Dashboard />}
                        />

                        <Route
                            path="/fleet"
                            element={<Fleet />}
                        />

                        <Route
                            path="/findings"
                            element={<Findings />}
                        />

                        <Route
                            path="/compliance"
                            element={<Compliance />}
                        />

                        <Route
                            path="/drift"
                            element={<Drift />}
                        />

                        <Route
                            path="/agent"
                            element={<Agent />}
                        />

                    </Routes>

                </div>

            </div>

        </BrowserRouter>
    );
}

export default App;