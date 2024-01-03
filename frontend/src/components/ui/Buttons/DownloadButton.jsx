import { Link } from 'react-router-dom';
import styles from './NavLinkButton.module.scss';

function DownloadButton({ title, to }) {
  return (
    <Link to={to} className={styles.NavLinkButton}>
      {title}
    </Link>
  );
}

export default DownloadButton;
