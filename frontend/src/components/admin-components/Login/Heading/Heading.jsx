import React from "react";
import styles from "./Heading.module.scss";

const Heading = ({ title }) => {
  return (
    <div className={styles.headingWrap}>
      <p className={styles.headingText}>{title}</p>
    </div>
  );
};

export default Heading;

