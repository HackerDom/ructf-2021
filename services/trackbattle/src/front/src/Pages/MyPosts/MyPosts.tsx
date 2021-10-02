import * as React from "react";
import {api} from "../../api/api";
import {useHistory} from "react-router-dom";
import {Posts} from "../LatestPage/Posts";
import {Button} from "../Components/Button";
import {Cell} from "../Components/Cell";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";

export const MyPosts: React.FC = () => {
    const history = useHistory();
    const [posts, setPosts] = React.useState<string[] | null>(null);

    React.useEffect(() => {
        const loadPosts = async () => {
            const response = await api.getMyPosts();
            setPosts(response.data?.post_ids || null);
        }

        void loadPosts();
    }, [])

    const handleCreate = () => {
        history.push("/track/create");
    }

    return (
        <TrackBattleLayout>
            {posts?.length ? (
                <>
                    <Posts postIds={posts}/>
                </>
            ) : (
                <>
                    <Cell center>There are no tracks yet</Cell>
                    <Button color={"green"} text={"Create your first battle"} onClick={handleCreate} />
                </>
            )}
        </TrackBattleLayout>
    );
};