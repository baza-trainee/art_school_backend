import DepartmentCard from './DepartmentCard/DepartmentCard';
import styles from './DepartmentsLayout.module.scss';

const DepartmentsLayout = ({ data }) => {
  return (
    <div className={styles.contentWrap}>
      {data &&
        Array.isArray(data) &&
        data.map(item => <DepartmentCard key={item.id} department={item} />)}
    </div>
  );
};
export default DepartmentsLayout;
