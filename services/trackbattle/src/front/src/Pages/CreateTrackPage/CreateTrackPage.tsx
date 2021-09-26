import React from "react";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Button} from "../Components/Button";
import {AudioPlayer, Note} from "../../Utilities/AudioPlayer";
import styles from "./CreateTrackPage.less";
import {TrackLine} from "./TrackLine";
import {useHistory, useRouteMatch} from "react-router-dom";
import {api} from "../../api/api";
import {Line} from "../Components/Line";
import {createObject} from "../../Utilities/ObjectCreator";
import {Track} from "../../api/types/Track";
import { Input } from "../Components/Input";
import {CommentResponse} from "../../api/types/Comment";

const maxTrackLength = 124;
const player: AudioPlayer = new AudioPlayer();

export const CreateTrackPage: React.FC = () => {
    const history = useHistory();
    const routeMatch = useRouteMatch<{inReplyTo?: string}>();

    const [track, setTrack] = React.useState<Note[]>([]);
    const [title, setTitle] = React.useState<string>("");
    const [description, setDescription] = React.useState<string>("");
    const [titleStage, setTitleStage] = React.useState<boolean>(false);

    const inReplyTo = routeMatch.params.inReplyTo

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
        if (!titleStage) {
            setTitleStage(true);
            return;
        }

        if ((title || !!inReplyTo) && description) {
            if (!!inReplyTo) {
                const request = createObject<CommentResponse>(CommentResponse, {track: track.join(""), description: description, post_id: inReplyTo});
                await api.addComment(request);
            } else {
                const request = createObject<Track>(Track, {notes: track.join(""), title: title, description: description});
                await api.postTrack(request);
            }
            history.goBack();
        }
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
            {!titleStage ? (
                <>
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
                </>
            ) : (
                <>
                    {!inReplyTo && <Input value={title} onChange={setTitle} placeholder={"Track title"} />}
                    <Input value={description} onChange={setDescription} placeholder={"Track description"} />
                </>
            )}
        </TrackBattleLayout>
    );
}

