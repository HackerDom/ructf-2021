import React from "react";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Line} from "../Components/Line";
import {Button} from "../Components/Button";
import {useHistory} from "react-router-dom";
import {User} from "../../api/types/User";
import {Input} from "../Components/Input";
import {Cell} from "../Components/Cell";

export const CreateUserPage: React.FC = () => {
    const history = useHistory();
    const [error, setError] = React.useState<string | null>(null);
    const [user, setUser] = React.useState<User>({username: "", password_sha256: ""});

    const handleBack = () => {
        history.push("/latest");
    }

    const handleCreate = () => {
        if (!user.username || !user.password_sha256) {
            setError("Fill username and password");
            return;
        }
    }

    const handleSetUser = (value: Partial<User>) => {
        setUser({...user, ...value});
        setError(null);
    }

    return (
        <TrackBattleLayout>
            <Line>
                <Button text="back" color="green" onClick={handleBack} />
                <Button text="create" color="green" onClick={handleCreate} />
            </Line>
            <Input value={user.username} placeholder={"Enter user name"} onChange={v => handleSetUser({username: v})} />
            <Input value={user.password_sha256} placeholder={"Enter password"} onChange={v => handleSetUser({password_sha256: v})} type={"password"}/>
            {error && <Cell>{error}</Cell>}
        </TrackBattleLayout>
    );
}