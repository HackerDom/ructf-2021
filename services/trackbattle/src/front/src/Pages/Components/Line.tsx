import * as React from "react";

import styles from "./Line.less";

export const Line: React.FC = (props) => {
    return (
        <div className={styles.line}>
            {props.children}
        </div>
    );
};