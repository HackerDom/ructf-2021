import React from "react";
import {Post} from "../../api/types/Post";
import {api} from "../../api/api";
import {Cell} from "../Components/Cell";
import {Line} from "../Components/Line";
import {Button} from "../Components/Button";
import {createObject} from "../../Utilities/ObjectCreator";
import {useHistory} from "react-router-dom";

interface Props {
    postIds: string[];
}

export const Posts: React.FC<Props> = (props) => {
    const history = useHistory();
    const [posts, setPosts] = React.useState<Post[] | null>(null);

    React.useEffect(() => {
        const loadPostsInfo = async (posts: string[]) => {
            const postsInfos = await Promise.all(
                posts.map(p => api.getPost(p))
            );

            if (postsInfos.every(x => x.data)) {
                setPosts(postsInfos.map((x, i) => createObject(Post, {...x.data, id: posts[i]})));
            }
        }

        if (props.postIds && props.postIds?.length) {
            void loadPostsInfo(props.postIds);
        }

    }, [props.postIds])

    if (!posts || !posts.length) {
        return null;
    }

    const handleBattle = (postId: string) => {
        history.push(`/battle/${postId}`);
    }

    return (
        <>
            {posts.map((p) => (
                <Line key={p.id}>
                    <Cell center>{new Date(p.publishingDate).toLocaleString("en-US")}</Cell>
                    <Cell center>{p.title}</Cell>
                    <Cell center>Author: {p.author}</Cell>
                    <Button color={"green"} text={"View it"} onClick={() => handleBattle(p.id)} width={200}/>
                </Line>
            ))}
        </>
    )
}