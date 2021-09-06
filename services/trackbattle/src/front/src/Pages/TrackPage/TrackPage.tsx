import React from "react";
import {useHistory} from "react-router-dom";
import querystring from "querystring";
import {JsonSerializer} from "../../Utilities/JsonSerializer";
import {Track} from "../../api/types/Track";

export const TrackPage: React.FC = () => {
    const history = useHistory();

    const getParams = React.useCallback(<T, >(type: {new (): T;}): T | null => {
        const query = history.location.search[0] === "?" ? history.location.search.substring(1) : history.location.search;
        const json = querystring.parse(query);

        return JsonSerializer.deserialize(json, type);
    }, [history.location]);

    const track = React.useMemo(() => {
        return getParams(Track);
    }, [history.location])

    if (track === null) {
        return <div>loading</div>;
    }


    return (
        <>
            <div>Track for battle!!!</div>
            <div>{track.notes}</div>
            <button onClick={() => track.play()}>resume</button>
        </>
    );
}
