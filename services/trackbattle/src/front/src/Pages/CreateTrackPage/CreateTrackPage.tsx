import React from "react";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Button} from "../Components/Button";
import {AudioPlayer, Note} from "../TrackPage/AudioPlayer";
import styles from "./CreateTrackPage.less";
import {TrackLine} from "./TrackLine";
import {useHistory} from "react-router-dom";
import {Track} from "../../api/types/Track";
import {api} from "../../api/api";

const maxTrackLength = 124;

export const CreateTrackPage: React.FC = () => {
    const history = useHistory();

    const [track, setTrack] = React.useState<string[]>([]);

    const handleBack = () => {
        history.push("/latest")
    }

    const handleDelete = () => {
        if (track.length > 0) {
            setTrack(track.slice(0, track.length - 1))
        }
    }

    const handlePlay = () => {
        const t = new Track();
        t.notes = track.join("");
        t.play();
    }

    const handlePublish = async () => {
        await api.postTrack({track: track.join(""), title: "", description: ""})
    }

    const handleClick = (note: Note) => {
        if (track.length < maxTrackLength) {
            setTrack([...track, note])
        }
    }

    return (
        <TrackBattleLayout>
            <div className={styles.actionButtons}>
                <Button text="back" color="green" onClick={handleBack} />
                <Button text="publish" color="green" onClick={handlePublish} />
            </div>
            <div className={styles.actionButtons}>
                <Button text="clear" color="green" onClick={() => setTrack([])} />
                <Button text="delete" color="green" onClick={handleDelete} />
                <Button text="play" color="green" onClick={handlePlay} />
            </div>
            <div className={styles.trackButtons}>
                {AudioPlayer.Notes.map(x => (
                    <div className={styles.trackButton}>
                        <Button text={x} color="green" onClick={() => handleClick(x)} />
                    </div>
                ))}
            </div>
            <div>
                {track.map((x, i) => (
                    <TrackLine lineNumber={i} note={x} />
                ))}
            </div>
        </TrackBattleLayout>
    );
}

