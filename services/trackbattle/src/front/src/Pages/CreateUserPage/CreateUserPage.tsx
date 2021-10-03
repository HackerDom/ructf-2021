import React from "react";
import {TrackBattleLayout} from "../Components/TrackBattleLayout";
import {Line} from "../Components/Line";
import {Button} from "../Components/Button";
import {useHistory} from "react-router-dom";
import {User} from "../../api/types/User";
import {Input} from "../Components/Input";
import {Cell} from "../Components/Cell";
import {api} from "../../api/api";
import {CookiesStorage} from "../../Utilities/CookiesStorage";
import {sha256} from "../../Utilities/HashConverter";
import {createObject} from "../../Utilities/ObjectCreator";

export const CreateUserPage: React.FC = () => {
    const history = useHistory();
    const [error, setError] = React.useState<string | null>(null);
    const [user, setUser] = React.useState<User>({nickname: "", password_sha256: "", payment_info: ""});

    const handleBack = () => {
        history.push("/latest");
    }

    const handleCreate = async () => {
        if (!user.nickname || !user.password_sha256 || !user.payment_info) {
            setError("Fill username and password");
            return;
        }

        const request = createObject(User, {nickname: user.nickname, password_sha256: sha256(user.password_sha256), payment_info: user.payment_info});
        const result = await api.createUser(request);

        if (!result.data) {
            setError(result.error || "Unknown error");
            return;
        }

        CookiesStorage.setAuth(result.data.auth_token);
        history.push("/");
    }

    const handleLogin = () => {
        history.push("/user/login");
    }

    const handleSetUser = (value: Partial<User>) => {
        setUser({...user, ...value});
        setError(null);
    }

    return (
        <TrackBattleLayout>
            <Line>
                <Button text="back" color="green" onClick={handleBack} />
                <Button text="I have an account" color="green" onClick={handleLogin} />
                <Button text="create" color="green" onClick={handleCreate} />
            </Line>
            <Input value={user.nickname} placeholder={"Enter user name"} onChange={v => handleSetUser({nickname: v})} />
            <Input value={user.password_sha256} placeholder={"Enter password"} onChange={v => handleSetUser({password_sha256: v})} type={"password"}/>
            <Input value={user.payment_info || ""} placeholder={"Enter payment info in case of victory in the battle"} onChange={v => handleSetUser({payment_info: v})}/>
            {error && <Cell>{error}</Cell>}
        </TrackBattleLayout>
    );
}