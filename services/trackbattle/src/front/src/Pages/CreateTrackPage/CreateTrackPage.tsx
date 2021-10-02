import React from "react";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Button} from "../Components/Button";
import {AudioPlayer, Note, Waveform} from "../../Utilities/AudioPlayer";
import styles from "./CreateTrackPage.less";
import {TrackLine} from "./TrackLine";
import {useHistory, useRouteMatch} from "react-router-dom";
import {api} from "../../api/api";
import {Line} from "../Components/Line";
import {createObject} from "../../Utilities/ObjectCreator";
import {Notes, Track} from "../../api/types/Track";
import { Input } from "../Components/Input";
import {CommentResponse} from "../../api/types/Comment";
import {player} from "../../App";
import {Cell} from "../Components/Cell";
import {toBase64} from "../../Utilities/HashConverter";
import {JsonSerializer} from "../../Utilities/JsonSerializer";

const maxTrackLength = 124;

export const CreateTrackPage: React.FC = () => {
    const history = useHistory();
    const routeMatch = useRouteMatch<{inReplyTo?: string}>();

    const [track, setTrack] = React.useState<Note[]>([]);
    const [waveform, setWaveform] = React.useState<Waveform>("triangle");
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
        player.stopPlaying();
        await player.play(track, waveform);
    }

    const handlePublish = async () => {
        if (!titleStage) {
            setTitleStage(true);
            return;
        }

        if ((title || !!inReplyTo) && description) {
            const notes = JSON.stringify(JsonSerializer.serialize<Notes>(createObject<Notes>(Notes, {notes: track.join(""), waveform: waveform}), Notes));
            if (!!inReplyTo) {
                const request = createObject<CommentResponse>(CommentResponse, {track: toBase64(notes), description: description, post_id: inReplyTo});
                await api.addComment(request);
            } else {
                const request = createObject<Track>(Track, {track: toBase64(notes), title: title, description: description});
                await api.postTrack(request);
            }
            history.goBack();
        }
    }

    const handleWaveform = async (form: Waveform) => {
        setWaveform(form);
    }

    const handleClick = async (note: Note) => {
        player.stopPlaying();
        if (track.length < maxTrackLength) {
            setTrack([...track, note])
            await player.playNote(note, waveform);
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
                    <Cell center>Wave form:</Cell>
                    <Line>
                        <Button text="triangle" color="green" checked={waveform === "triangle"} onClick={() => handleWaveform("triangle")} />
                        <Button text="sine" color="green" checked={waveform === "sine"} onClick={() => handleWaveform("sine")} />
                        <Button text="square" color="green" checked={waveform === "square"} onClick={() => handleWaveform("square")} />
                        <Button text="sawtooth" color="green" checked={waveform === "sawtooth"} onClick={() => handleWaveform("sawtooth")} />
                    </Line>
                    <Line>
                        <Button text="clear" color="green" onClick={() => setTrack([])} />
                        <Button text="delete" color="green" onClick={handleDelete} />
                        <Button text="play" color="green" onClick={handlePlay} />
                    </Line>
                    <Line>
                        {AudioPlayer.Notes.map((x, i) => (
                            <div className={styles.trackButton}>
                                <Button key={i} text={x} color="green" onClick={() => handleClick(x)} />
                            </div>
                        ))}
                    </Line>
                    <div>
                        {track.map((x, i) => (
                            <TrackLine key={i} lineNumber={i} note={x} />
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

