import React from "react";
import {useHistory} from "react-router-dom";
import {Cell} from "../Components/Cell";
import {Button} from "../Components/Button";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {api} from "../../api/api";
import {CookiesStorage} from "../../Utilities/CookiesStorage";
import {Posts} from "./Posts";

export const LatestPage: React.FC = () => {
    const history = useHistory();
    const [posts, setPosts] = React.useState<string[] | null>(null);

    React.useEffect(() => {
        const loadPosts = async () => {
            const response = await api.getLatest();
            setPosts(response.data?.posts || null);
        }

        void loadPosts();
    }, [])

    const handleCreate = () => {
        history.push("/track/create");
    }

    if (!posts) {
        return (
            <TrackBattleLayout>
                {!CookiesStorage.getAuth() ? (
                    <Cell center>You have to create user to battle with other users</Cell>
                ) : null}
            </TrackBattleLayout>
        )
    }

    return (
        <TrackBattleLayout>
            <Button color={"green"} text={"Start new battle"} onClick={handleCreate} />
            {posts.length ? (
                <>
                    <Posts postIds={posts}/>
                </>
            ) : (
                <Cell center>There are no battles yet</Cell>
            )}
        </TrackBattleLayout>
    )
}