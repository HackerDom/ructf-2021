import * as React from "react";
import styles from "./TrackBattleLayout.less";
import {Line} from "./Line";
import {Button} from "./Button";
import {useHistory} from "react-router-dom";
import {CookiesStorage} from "../../Utilities/CookiesStorage";
import {player} from "../../App";

export const TrackBattleLayout: React.FC = (props) => {
    const history = useHistory();
    const isAuthorized = !!CookiesStorage.getAuth();

    player.stopPlaying();

    const handleLatest = () => {
        history.push("/");
    }

    const handleLogin = () => {
        history.push("/user/login");
    }

    const handleSignup = () => {
        history.push("/user/create")
    }

    const handleProfile = () => {
        history.push("/user")
    }

    const handleLogout = () => {
        CookiesStorage.removeAuth();
        history.push("/logout")
    }

    return (
        <div className={styles.container}>
            <header className={styles.header}>Track Battle</header>
            <main className={styles.main}>
                {props.children}
            </main>
            <footer>
                <Line>
                    {isAuthorized ? (
                        <>
                            <Button color={"green"} text={"Latest posts"} onClick={handleLatest} />
                            <Button color={"green"} text={"Go to user profile"} onClick={handleProfile} />
                            <Button color={"green"} text={"Logout"} onClick={handleLogout} />
                        </>
                    ) : (
                        <>
                            <Button color={"green"} text={"Login"} onClick={handleLogin} />
                            <Button color={"green"} text={"Create user"} onClick={handleSignup} />
                        </>
                    )}
                </Line>
            </footer>
        </div>
    );
};