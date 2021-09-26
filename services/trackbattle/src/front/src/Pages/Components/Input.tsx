import * as React from "react";
import styles from "./Input.less";
import {Line} from "./Line";

interface Props {
    value: string;
    placeholder: string;
    onChange: (value: string) => void;
    type?: "text" | "password";
}

export const Input: React.FC<Props> = (props) => {
    return (
        <Line>
            <input className={styles.input} onChange={e => props.onChange(e.target.value)} placeholder={props.placeholder} type={props.type ?? "text"} />
        </Line>
    );
};