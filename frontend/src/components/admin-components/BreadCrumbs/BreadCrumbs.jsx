import { Link } from 'react-router-dom';
import AdminHome from '@/components/Icons/AdminHome';
import AdminArrow from '@/components/Icons/AdminArrow';
import styles from './BreadCrumbs.module.scss';

const BreadCrumbs = ({ breadcrumbs }) => {
  return (
    <div className={styles.wrapper}>
      <div className={styles.icon}>
        <Link to={'/admin/sliders'}>
          <AdminHome />
        </Link>
      </div>

      {breadcrumbs.map((item, index) => (
        <div key={index} className={styles.crumb}>
          <AdminArrow />
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
};

export default BreadCrumbs;
