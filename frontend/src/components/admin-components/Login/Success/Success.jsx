import { Link } from 'react-router-dom';
import styles from './Success.module.scss';

const Success = () => {
  return (
    <div className={styles.successStyle}>
      <p className={styles.headingStyle}>Пароль успішно змінено</p>
      <img src="/icons/icon-success.svg" alt="" />
      <Link to="/login" className={styles.link}>
        Увійти в аккаунт
      </Link>
    </div>
  );
};
export default Success;
