import { Link } from 'react-router-dom';
import sprite from '../../../../assets/icons/sprite-admin.svg';
import styles from './LogoutButton.module.scss';
import { useAuthorized } from '@/store/IsAuthorizedStore';

const LogoutButton = () => {
  const { setUnAuthorized } = useAuthorized();
  // Define a function to check and remove the key
  const checkAndRemoveKey = key => {
    // Get the value of the key from local storage
    const value = localStorage.getItem(key);
    // Check if the value is not null
    const exists = value !== null;
    // If the key exists, remove it
    if (exists) {
      localStorage.removeItem(key);
    }
  };
  return (
    <Link
      className={styles.logoutButtonLink}
      onClick={() => {
        setUnAuthorized();
        // Call the function with the key 'access_token'
        checkAndRemoveKey('access_token');
      }}
    >
      <p>Вихід</p>
      <svg width="16" height="16">
        <use href={`${sprite}#logout`} className={styles.icon} />
      </svg>
    </Link>
  );
};

export default LogoutButton;
