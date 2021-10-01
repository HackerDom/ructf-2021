import * as React from "react";

import styles from "./Button.less";

interface Props {
    color: "green";
    text: string;
    onClick: () => void;
    width?: number;
    checked?: boolean;
}

export const Button: React.FC<Props> = (props) => {
    return (
        <button className={styles.button} style={{width: props.width ?? "100%", textShadow: props.checked ? "0 0 7px" : undefined, border: props.checked ? "#8a2be2 solid 2px" : undefined, boxShadow: props.checked ? "0 0 7px #8a2be2" : undefined }} onClick={props.onClick}>
            {props.text}
        </button>
    );
};