import * as React from "react";
import {Line} from "../Components/Line";
import {Cell} from "../Components/Cell";

interface Props {
    lineNumber: number;
    note: string;
}

export const TrackLine: React.FC<Props> = (props) => {
    return (
        <Line>
            <Cell>
                {props.lineNumber.toString().padStart(4, "0")}
            </Cell>
            <Cell>
                {props.note}
            </Cell>
        </Line>
    )
}