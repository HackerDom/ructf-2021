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


    const pp = React.useMemo(() => {
        return getParams(Track);
    }, [history.location])

    if (pp === null)
        return <div></div>;

    pp.play();

    return (
        <>
            <div>Тут у нас будет проигрывание трека</div>
            <div>{pp.notes}</div>
        </>
    );
}