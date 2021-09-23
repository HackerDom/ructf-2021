import React from "react";
import {useHistory} from "react-router-dom";
import querystring from "querystring";
import {JsonSerializer} from "../../Utilities/JsonSerializer";
import {Track} from "../../api/types/Track";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Button} from "../Components/Button";
import styles from "./TrackPage.less";

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

    const handleBack = () => {
        history.push("/latest");
    }

    const handlePlay = () => {
        track.play();
    }

    return (
        <TrackBattleLayout>
            <div className={styles.actionButtons}>
                <Button text="back" color="green" onClick={handleBack} />
                <Button text="play" color="green" onClick={handlePlay} />
            </div>
            <div></div>
            <div className={styles.title}>{track.title}</div>
            {track.description ? <div className={styles.description}>{track.description}</div> : null}
        </TrackBattleLayout>
    );
}
