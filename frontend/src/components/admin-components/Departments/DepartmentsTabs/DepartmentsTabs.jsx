import { Link, useParams } from 'react-router-dom';
import styles from './DepartmentsTabs.module.scss';

const DepartmentsTabs = ({ departments }) => {
  const { id } = useParams();

  return (
    <div className={styles.wrapper}>
      {departments &&
        Array.isArray(departments) &&
        departments.map(item => (
          <div
            key={item.id}
            className={item.id == id ? styles.item_active : styles.item}
          >
            <Link
              to={`/admin/departments/${item.id}`}
              state={{ title: item.department_name }}
            >
              {item.department_name}
            </Link>
          </div>
        ))}
    </div>
  );
};

export default DepartmentsTabs;
