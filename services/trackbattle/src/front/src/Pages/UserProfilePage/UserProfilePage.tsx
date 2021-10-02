import React from "react";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {UserData} from "../../api/types/User";
import {api} from "../../api/api";
import {createObject} from "../../Utilities/ObjectCreator";
import {Cell} from "../Components/Cell";
import {Button} from "../Components/Button";
import {useHistory} from "react-router-dom";

export const UserProfilePage: React.FC = () => {
    const history = useHistory();
    const [user, setUser] = React.useState<UserData | null>(null);

    React.useEffect(() => {
        const loadUser = async () => {
            const response = await api.getUser();

            setUser(createObject(UserData, {nickname: response.data?.nickname, payment_info: response.data?.payment_info, posts: response.data?.posts}));
        }

        void loadUser();
    }, [])

    const handlePosts = () => {
        history.push("/user/tracks");
    }

    return (
        <TrackBattleLayout>
            {user &&
                <>
                    <Cell center>User name: {user?.nickname}</Cell>
                    <Cell center>User payment info: {user?.payment_info}</Cell>
                    {user.posts.length ? (
                        <Button text={`Published ${user.posts.length} posts`} color={"green"} onClick={handlePosts}/>
                    ) : (
                        <Cell center>Published {user.posts.length} posts</Cell>
                    )}
                </>
            }
        </TrackBattleLayout>
    )
}