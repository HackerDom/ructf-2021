import React from "react";
import {Link} from "react-router-dom";

export const LatestPage: React.FC = () => {
    return <Link to={"/track?notes=AABBCCDD"}>Погнали сразу в трек</Link>;
}