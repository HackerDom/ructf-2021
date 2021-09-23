import React from "react";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Button} from "../Components/Button";
import {AudioPlayer, Note} from "../../Utilities/AudioPlayer";
import styles from "./CreateTrackPage.less";
import {TrackLine} from "./TrackLine";
import {useHistory} from "react-router-dom";
import {api} from "../../api/api";
import {Line} from "../Components/Line";

const maxTrackLength = 124;
const player: AudioPlayer = new AudioPlayer();

export const CreateTrackPage: React.FC = () => {
    const history = useHistory();

    const [track, setTrack] = React.useState<Note[]>([]);

    const handleBack = () => {
        history.push("/latest")
    }

    const handleDelete = () => {
        if (track.length > 0) {
            setTrack(track.slice(0, track.length - 1))
        }
    }

    const handlePlay = async () => {
        await player.play(track);
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
            <Line>
                <Button text="back" color="green" onClick={handleBack} />
                <Button text="publish" color="green" onClick={handlePublish} />
            </Line>
            <Line>
                <Button text="clear" color="green" onClick={() => setTrack([])} />
                <Button text="delete" color="green" onClick={handleDelete} />
                <Button text="play" color="green" onClick={handlePlay} />
            </Line>
            <Line>
                {AudioPlayer.Notes.map(x => (
                    <div className={styles.trackButton}>
                        <Button text={x} color="green" onClick={() => handleClick(x)} />
                    </div>
                ))}
            </Line>
            <div>
                {track.map((x, i) => (
                    <TrackLine lineNumber={i} note={x} />
                ))}
            </div>
        </TrackBattleLayout>
    );
}

