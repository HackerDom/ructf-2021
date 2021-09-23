import React from "react";
import {Link} from "react-router-dom";

export const LatestPage: React.FC = () => {
    return (<>
        <Link to={"/track/create"}>Create track</Link>
        <br />
        <Link to={"/track?notes=AEAEAGGGEGEGAAAEAEA&title=track&description=this is track for battle!!!"}>Go to track</Link>
        <br />
        <Link to={"/user/create"}>Create User</Link>
        <br />
        <Link to={"/login"}>Login</Link>
    </>);
}