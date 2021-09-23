import * as React from "react";

import styles from "./Button.less";

interface Props {
    color: "green";
    text: string;
    onClick: () => void;
    width?: number;
}

export const Button: React.FC<Props> = (props) => {
    return (
        <button className={styles.button} style={{width: props.width ?? "100%" }} onClick={props.onClick}>
            {props.text}
        </button>
    );
};