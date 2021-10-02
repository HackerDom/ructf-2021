import React from 'react';
import './App.less';
import {HashRouter, Redirect, Route, Switch} from "react-router-dom";
import {CreateUserPage} from "./Pages/CreateUserPage/CreateUserPage";
import {UserProfilePage} from "./Pages/UserProfilePage/UserProfilePage";
import {TrackPage} from "./Pages/TrackPage/TrackPage";
import {CreateTrackPage} from "./Pages/CreateTrackPage/CreateTrackPage";
import {BattlePage} from "./Pages/BattlePage/BattlePage";
import {LatestPage} from "./Pages/LatestPage/LatestPage";
import {LoginPage} from "./Pages/LoginPage";
import {MyPosts} from "./Pages/MyPosts/MyPosts";
import {AudioPlayer} from "./Utilities/AudioPlayer";

export const player: AudioPlayer = new AudioPlayer();

export const App: React.FC = () => {
    return (
        <HashRouter>
            <Switch>
                <Route
                    path="/user/create"
                    component={CreateUserPage}
                    exact
                />
                <Route
                    path="/user/login"
                    component={LoginPage}
                    exact
                />
                <Route
                    path="/user"
                    component={UserProfilePage}
                    exact
                />
                <Route
                    path="/track/create"
                    component={CreateTrackPage}
                    exact
                />
                <Route
                    path="/track/create/:inReplyTo"
                    component={CreateTrackPage}
                    exact
                />
                <Route
                    path="/track"
                    component={TrackPage}
                    exact
                />
                <Route
                    path="/battle/:battleId"
                    component={BattlePage}
                    exact
                />
                <Route
                    path="/user/tracks"
                    component={MyPosts}
                    exact
                />
                <Redirect
                    path="/logout"
                    to="/"
                    exact
                />
                <Route
                    path={["/", "/latest"]}
                    component={LatestPage}
                />
            </Switch>
        </HashRouter>
    );
};
