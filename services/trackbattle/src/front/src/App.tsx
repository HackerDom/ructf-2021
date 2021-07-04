import React from 'react';
import './App.css';
import {HashRouter, Route, Switch} from "react-router-dom";
import {CreateUserPage} from "./Pages/CreateUserPage/CreateUserPage";
import {UserProfilePage} from "./Pages/UserProfilePage/UserProfilePage";
import {TrackPage} from "./Pages/TrackPage/TrackPage";
import {CreateTrackPage} from "./Pages/CreateTrackPage/CreateTrackPage";
import {BattlePage} from "./Pages/BattlePage/BattlePage";
import {LatestPage} from "./Pages/LatestPage/LatestPage";

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
                    path="/user/:userId"
                    component={UserProfilePage}
                    exact
                />
                <Route
                    path="/track/create"
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
                    path={["/", "/latest"]}
                    component={LatestPage}
                />
            </Switch>
        </HashRouter>
    );
};
