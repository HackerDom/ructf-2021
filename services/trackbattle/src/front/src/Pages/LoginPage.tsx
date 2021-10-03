import React from "react";
import {useHistory} from "react-router-dom";
import {User} from "../api/types/User";
import {TrackBattleLayout} from "./Components/TrackBattleLayout";
import {Line} from "./Components/Line";
import {Button} from "./Components/Button";
import {Input} from "./Components/Input";
import {Cell} from "./Components/Cell";
import {api} from "../api/api";
import {CookiesStorage} from "../Utilities/CookiesStorage";
import {createObject} from "../Utilities/ObjectCreator";
import {sha256} from "../Utilities/HashConverter";

export const LoginPage: React.FC = () => {
    const history = useHistory();
    const [error, setError] = React.useState<string | null>(null);
    const [user, setUser] = React.useState<User>({nickname: "", password_sha256: ""});

    const handleBack = () => {
        history.push("/latest");
    }

    const handleLogin = async () => {
        if (!user.nickname || !user.password_sha256) {
            setError("Fill username and password");
            return;
        }

        const request = createObject(User, {nickname: user.nickname, password_sha256: sha256(user.password_sha256)});
        const result = await api.loginUser(request);

        if (!result.data) {
            setError(result.error || "Unknown error");
            return;
        }

        CookiesStorage.setAuth(result.data.auth_token);
        history.push("/");
    }

    const handleSignup = () => {
        history.push("/user/create")
    }

    const handleSetUser = (value: Partial<User>) => {
        setUser({...user, ...value});
        setError(null);
    }

    return (
        <TrackBattleLayout>
            <Line>
                <Button text="back" color="green" onClick={handleBack} />
                <Button text="Create an account" color="green" onClick={handleSignup} />
                <Button text="login" color="green" onClick={handleLogin} />
            </Line>
            <Input value={user.nickname} placeholder={"Enter user name"} onChange={v => handleSetUser({nickname: v})} />
            <Input value={user.password_sha256} placeholder={"Enter password"} onChange={v => handleSetUser({password_sha256: v})} type={"password"}/>
            {error && <Cell>{error}</Cell>}
        </TrackBattleLayout>
    );
}