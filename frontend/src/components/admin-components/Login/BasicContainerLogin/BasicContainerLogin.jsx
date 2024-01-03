import styles from './BasicContainerLogin.module.scss';

export const BasicContainerLogin = ({ children }) => {
  return <div className={styles.basicContainerLoginWrap}>{children}</div>;
};
export default BasicContainerLogin;
