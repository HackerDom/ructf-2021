import React from "react";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Line} from "../Components/Line";
import {Button} from "../Components/Button";
import {useHistory} from "react-router-dom";
import {User} from "../../api/types/User";
import {Input} from "../Components/Input";
import {Cell} from "../Components/Cell";
import {api} from "../../api/api";
import {LocalStorage} from "../../Utilities/LocalStorage";
import {sha256} from "../../Utilities/HashConverter";
import {createObject} from "../../Utilities/ObjectCreator";

export const CreateUserPage: React.FC = () => {
    const history = useHistory();
    const [error, setError] = React.useState<string | null>(null);
    const [user, setUser] = React.useState<User>({nickname: "", password_sha256: "", flag: ""});

    const handleBack = () => {
        history.push("/latest");
    }

    const handleCreate = async () => {
        if (!user.nickname || !user.password_sha256 || !user.flag) {
            setError("Fill username and password");
            return;
        }

        const request = createObject(User, {nickname: user.nickname, password_sha256: await sha256(user.password_sha256), flag: user.flag});
        const result = await api.createUser(request);

        if (!result.data) {
            setError(result.error || "Unknown error");
            return;
        }

        LocalStorage.setAuth(result.data.auth_token);
        history.push("/");
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
            <Input value={user.nickname} placeholder={"Enter user name"} onChange={v => handleSetUser({nickname: v})} />
            <Input value={user.password_sha256} placeholder={"Enter password"} onChange={v => handleSetUser({password_sha256: v})} type={"password"}/>
            <Input value={user.flag || ""} placeholder={"Enter flag"} onChange={v => handleSetUser({flag: v})}/>
            {error && <Cell>{error}</Cell>}
        </TrackBattleLayout>
    );
}