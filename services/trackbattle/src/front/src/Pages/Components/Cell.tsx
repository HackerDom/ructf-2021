import * as React from "react";

import styles from "./Cell.less";

interface Props {
    center?: boolean;
}

export const Cell: React.FC<Props> = (props) => {
    return (
        <div className={styles.cell} style={{textAlign: props.center ? "center" : undefined}}>
            {props.children}
        </div>
    );
};