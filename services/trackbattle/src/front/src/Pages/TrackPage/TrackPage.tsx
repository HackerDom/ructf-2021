import React from "react";
import {useHistory} from "react-router-dom";
import querystring from "querystring";
import {JsonSerializer} from "../../Utilities/JsonSerializer";
import {Notes, Track} from "../../api/types/Track";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Button} from "../Components/Button";
import styles from "./TrackPage.less";
import {Cell} from "../Components/Cell";
import {Line} from "../Components/Line";
import {fromBase64} from "../../Utilities/HashConverter";
import {player} from "../../App";

export const TrackPage: React.FC = () => {
    const history = useHistory();

    const getParams = React.useCallback(<T, >(type: {new (): T;}): T | null => {
        const query = history.location.search[0] === "?" ? history.location.search.substring(1) : history.location.search;
        const json = querystring.parse(fromBase64(query));

        return JsonSerializer.deserialize(json, type);
    }, [history.location]);

    const track = React.useMemo(() => {
        return getParams(Track);
    }, [history.location])

    if (track === null) {
        return <div>loading</div>;
    }

    const handleBack = () => {
        history.goBack();
    }

    const handlePlay = () => {
        const notes = JsonSerializer.deserialize(JSON.parse(fromBase64(track.track)), Notes)
        notes?.play(player);
    }

    return (
        <TrackBattleLayout>
            <Line>
                <Button text="back" color="green" onClick={handleBack} />
                <Button text="play" color="green" onClick={handlePlay} />
            </Line>
            {track.title ? <Cell><div className={styles.title}>{track.title}</div></Cell> : null}
            {track.description ? <Cell center>{track.description}</Cell> : null}
        </TrackBattleLayout>
    );
}
