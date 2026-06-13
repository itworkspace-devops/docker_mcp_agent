import {
    useEffect,
    useState
} from "react";

import { api }
from "../services/api";

import {
    createWebSocket
} from "../services/ws";

export default function NotificationBell() {

    const [
        notifications,
        setNotifications
    ] = useState<any[]>([]);

    const load =
        async () => {

        const res =
            await api.get(
                "/notifications"
            );

        setNotifications(
            res.data
        );
    };

    useEffect(() => {

        load();

        const ws =
            createWebSocket();

        ws.onmessage =
            (
                event
            ) => {

            const msg =
                JSON.parse(
                    event.data
                );

            if (
                msg.event ===
                "notification"
            ) {

                load();
            }
        };

        return () => {

            ws.close();
        };

    }, []);

    const unread =
        notifications.filter(
            n => !n.read
        ).length;

    return (

        <div
            style={{
                position:
                    "relative"
            }}
        >

            🔔

            {
                unread > 0 && (

                    <span
                        style={{

                            position:
                                "absolute",

                            top:
                                "-10px",

                            right:
                                "-10px",

                            background:
                                "red",

                            color:
                                "white",

                            borderRadius:
                                "50%",

                            width:
                                "20px",

                            height:
                                "20px",

                            display:
                                "flex",

                            alignItems:
                                "center",

                            justifyContent:
                                "center",

                            fontSize:
                                "12px",
                        }}
                    >

                        {unread}

                    </span>
                )
            }

        </div>
    );
}