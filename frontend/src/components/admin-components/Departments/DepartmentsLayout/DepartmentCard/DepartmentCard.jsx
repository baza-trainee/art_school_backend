import { Link } from 'react-router-dom';
import styles from './DepartmentCard.module.scss';

const DepartmentCard = ({ department }) => {
  return (
    <Link
      to={`/admin/departments/${department.id}`}
      state={{ title: department.department_name }}
    >
      <div className={styles.card}>{department.department_name}</div>
    </Link>
  );
};

export default DepartmentCard;
