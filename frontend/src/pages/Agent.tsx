import { useState } from "react";
import { api } from "../services/api";

export default function Agent() {

    const [query, setQuery] =
        useState("");

    const [response, setResponse] =
        useState<any>();

    const execute = async () => {

        const res = await api.post(

            "/docker-agent/query",

            {
                query
            }
        );

        setResponse(
            res.data
        );
    };

    return (

        <div>

            <textarea

                rows={5}

                value={query}

                onChange={(e) =>
                    setQuery(
                        e.target.value
                    )
                }

            />

            <br />

            <button
                onClick={execute}
            >
                Execute
            </button>

            <pre>

                {
                    JSON.stringify(
                        response,
                        null,
                        2
                    )
                }

            </pre>

        </div>
    );
}