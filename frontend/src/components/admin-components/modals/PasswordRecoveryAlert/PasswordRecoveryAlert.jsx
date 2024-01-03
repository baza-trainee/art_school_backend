import styles from './PasswordRecoveryAlert.module.scss';

const PasswordRecoveryAlert = ({ setIsAlertOpen, message }) => {
  return (
    <div className={styles.wrapper}>
      <div className={styles.modalStyle} onClick={() => setIsAlertOpen(false)}>
        <p className={styles.headingStyle}>Відновлення паролю</p>
        <div className={styles.popUpStyle}>
          <img src="/icons/icon-success.svg" alt="" width="60" />
          <p className={styles.textStyle}>{message}</p>
        </div>
      </div>
    </div>
  );
};

export default PasswordRecoveryAlert;
