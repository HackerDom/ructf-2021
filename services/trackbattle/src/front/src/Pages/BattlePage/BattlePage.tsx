import React from "react";
import {Cell} from "../Components/Cell";
import {useHistory, useRouteMatch} from "react-router-dom";
import {Post} from "../../api/types/Post";
import {api} from "../../api/api";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Line} from "../Components/Line";
import {Button} from "../Components/Button";
import {Comments} from "./Comments";
import {toBase64} from "../../Utilities/HashConverter";

export const BattlePage: React.FC = () => {
    const routeMatch = useRouteMatch<{battleId: string}>();
    const history = useHistory();
    const [post, setPost] = React.useState<Post | null>(null);

    React.useEffect(() => {
        const loadPostInfo = async (postId: string) => {
            const p = await api.getPost(postId)

            if (p.data) {
                setPost(p.data)
            }
        }

        if (routeMatch.params.battleId) {
            void loadPostInfo(routeMatch.params.battleId);
        }

    }, [routeMatch.params.battleId])

    if (!post) {
        return null;
    }

    const handleBack = () => {
        history.push("/latest");
    }


    const handleListen = () => {
        const search = toBase64(`title=${post.title}&description=${post.description}&track=${post.track}`)
        history.push(`/track?${search}`);
    }

    const handleLike = async () => {
        const response = await api.likePost(routeMatch.params.battleId);
        if (response.data) {
            setPost({...post, likes_amount: post.likes_amount + 1})
        }
    }

    const handleBattle = () => {
        history.push(`/track/create/${routeMatch.params.battleId}`);
    }

    return (
        <TrackBattleLayout>
            <Line>
                <Button color={"green"} text={"back"} onClick={handleBack} />
                <Button color={"green"} text={"listen to it"} onClick={handleListen} />
                <Button color={"green"} text={"like it"} onClick={handleLike} />
                <Button color={"green"} text={"battle it"} onClick={handleBattle} />
            </Line>
            <Line><Cell center>{post.title}</Cell></Line>
            <Line><Cell center>{post.description}</Cell></Line>
            <Line>
                <Cell center>Posted at {new Date(post.publishingDate).toLocaleString("en-US")}</Cell>
                <Cell center>Author: {post.author}</Cell>
                <Cell center>Liked {post.likes_amount} times</Cell>
            </Line>
            <Cell center>------------------</Cell>
            <Cell center>Others battled with:</Cell>
            <Comments commentsIds={post.comments} />
        </TrackBattleLayout>
    )
}