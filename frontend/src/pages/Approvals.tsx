import {
    useEffect,
    useState
} from "react";

import { api } from "../services/api";

export default function Approvals() {

    const [
        approvals,
        setApprovals
    ] = useState<any[]>([]);

    const [
        loading,
        setLoading
    ] = useState(true);

    const load = async () => {

        try {

            const res =
                await api.get(
                    "/approval/pending"
                );

            setApprovals(
                res.data
            );

        } catch (err) {

            console.error(
                "Failed to load approvals",
                err
            );

        } finally {

            setLoading(false);
        }
    };

    const approve = async (
        executionId: string
    ) => {

        try {

            await api.post(
                `/approval/${executionId}/approve`
            );

            await load();

        } catch (err) {

            console.error(
                "Approval failed",
                err
            );
        }
    };

    const reject = async (
        executionId: string
    ) => {

        try {

            await api.post(
                `/approval/${executionId}/reject`
            );

            await load();

        } catch (err) {

            console.error(
                "Reject failed",
                err
            );
        }
    };

    useEffect(() => {

        load();

    }, []);

    if (loading) {

        return (
            <div>
                Loading approvals...
            </div>
        );
    }

    return (

        <div>

            <h2>
                Pending Approvals
            </h2>

            {
                approvals.length === 0 && (

                    <p>
                        No pending approvals.
                    </p>
                )
            }

            {
                approvals.length > 0 && (

                    <table>

                        <thead>

                            <tr>

                                <th>
                                    Tool
                                </th>

                                <th>
                                    Arguments
                                </th>

                                <th>
                                    Execution ID
                                </th>

                                <th>
                                    Actions
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {
                                approvals.map(
                                    (item) => (

                                        <tr
                                            key={
                                                item.execution_id
                                            }
                                        >

                                            <td>
                                                {
                                                    item.tool_name
                                                }
                                            </td>

                                            <td>

                                                <pre>

                                                    {
                                                        JSON.stringify(
                                                            item.tool_args,
                                                            null,
                                                            2
                                                        )
                                                    }

                                                </pre>

                                            </td>

                                            <td>

                                                {
                                                    item.execution_id
                                                }

                                            </td>

                                            <td>

                                                <button
                                                    onClick={() =>
                                                        approve(
                                                            item.execution_id
                                                        )
                                                    }
                                                >
                                                    Approve
                                                </button>

                                                <button
                                                    onClick={() =>
                                                        reject(
                                                            item.execution_id
                                                        )
                                                    }
                                                    style={{
                                                        marginLeft:
                                                            "10px"
                                                    }}
                                                >
                                                    Reject
                                                </button>

                                            </td>

                                        </tr>
                                    )
                                )
                            }

                        </tbody>

                    </table>
                )
            }

        </div>
    );
}