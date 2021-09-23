import * as React from "react";
import styles from "./TrackLine.less";

interface Props {
    lineNumber: number;
    note: string;
}

export const TrackLine: React.FC<Props> = (props) => {
    return (
        <div className={styles.line}>
            <div>
                {props.lineNumber.toString().padStart(4, "0")}
            </div>
            <div>
                {props.note}
            </div>
        </div>
    )
}