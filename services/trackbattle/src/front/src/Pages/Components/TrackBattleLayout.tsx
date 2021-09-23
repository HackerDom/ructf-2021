import * as React from "react";

import styles from "./TrackBattleLayout.less";

export const TrackBattleLayout: React.FC = (props) => {
    return (
        <div className={styles.container}>
            <header className={styles.header}>Track Battle</header>
            <main className={styles.main}>
                {props.children}
            </main>
            <footer></footer>
        </div>
    );
};