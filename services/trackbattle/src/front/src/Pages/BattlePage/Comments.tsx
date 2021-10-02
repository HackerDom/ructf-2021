import React from "react";
import {api} from "../../api/api";
import {Cell} from "../Components/Cell";
import {Line} from "../Components/Line";
import {Button} from "../Components/Button";
import {createObject} from "../../Utilities/ObjectCreator";
import {useHistory} from "react-router-dom";
import {Comment} from "../../api/types/Comment";
import {toBase64} from "../../Utilities/HashConverter";

interface Props {
    commentsIds: string[];
}

export const Comments: React.FC<Props> = (props) => {
    const history = useHistory();
    const [comments, setComments] = React.useState<Comment[] | null>(null);

    React.useEffect(() => {
        const loadCommentsInfo = async (commentsIds: string[]) => {
            const commentsInfos = await Promise.all(
                commentsIds.map(p => api.getComment(p))
            );

            if (commentsInfos.every(x => x.data)) {
                setComments(commentsInfos.map((x, i) => createObject(Comment, {...x.data, id: commentsIds[i]})));
            }
        }

        if (props.commentsIds && props.commentsIds?.length) {
            void loadCommentsInfo(props.commentsIds);
        }

    }, [props.commentsIds])

    if (!comments || !comments.length) {
        return null;
    }

    const handleListen = (comment: Comment) => {
        const search = toBase64(`description=${comment.description}&track=${comment.track}`)
        history.push(`/track?${search}`);
    }

    const handleLike = async (commentId: string) => {
        const response = await api.likeComment(commentId);
        if (response.data) {
            const commentIndex = comments.findIndex(x => x.id === commentId);
            const newComment = createObject(Comment, {
                id: comments[commentIndex].id,
                postId: comments[commentIndex].postId,
                author: comments[commentIndex].author,
                publishingDate: comments[commentIndex].publishingDate,
                description: comments[commentIndex].description,
                track: comments[commentIndex].track,
                likes_amount: comments[commentIndex].likes_amount + 1
            } );
            const newComments = [...comments.slice(0, commentIndex), newComment, ...comments.slice(commentIndex + 1)]
            setComments(newComments);
        }
    }

    return (
        <>
            {comments.map((p) => (
                <Line key={p.id}>
                    <Cell center>{new Date(p.publishingDate).toLocaleString("en-US")}</Cell>
                    <Cell center>Author: {p.author}</Cell>
                    <Cell center>Liked {p.likes_amount} times</Cell>
                    <Button color={"green"} text={"listen to it"} onClick={() => handleListen(p)} width={250}/>
                    <Button color={"green"} text={"like it"} onClick={() => handleLike(p.id)} width={200}/>
                </Line>
            ))}
        </>
    )
}