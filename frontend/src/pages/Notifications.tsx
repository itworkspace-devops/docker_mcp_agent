import {
    useEffect,
    useState
} from "react";

import { api } from "../services/api";

export default function Notifications() {

    const [
        notifications,
        setNotifications
    ] = useState<any[]>([]);

    const load = async () => {

        try {

            const res =
                await api.get(
                    "/notifications"
                );

            setNotifications(
                res.data
            );

        } catch (err) {

            console.error(err);
        }
    };

    useEffect(() => {

        load();

    }, []);

    return (

        <div>

            <h2>
                Notifications
            </h2>

            <table>

                <thead>

                    <tr>

                        <th>ID</th>
                        <th>Type</th>
                        <th>Title</th>
                        <th>Message</th>
                        <th>Read</th>

                    </tr>

                </thead>

                <tbody>

                    {
                        notifications.map(
                            (n) => (

                                <tr
                                    key={n.id}
                                >

                                    <td>
                                        {n.id}
                                    </td>

                                    <td>
                                        {n.event_type}
                                    </td>

                                    <td>
                                        {n.title}
                                    </td>

                                    <td>
                                        {n.message}
                                    </td>

                                    <td>
                                        {
                                            n.read
                                                ? "Yes"
                                                : "No"
                                        }
                                    </td>

                                </tr>
                            )
                        )
                    }

                </tbody>

            </table>

        </div>
    );
}