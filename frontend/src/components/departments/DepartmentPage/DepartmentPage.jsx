import { useState, useEffect } from 'react';
import Container from '@/components/Container/Container';
import Achievements from '@/components/main/Achievements/Achievements';
import GalleryDepartments from '@/components/departments/GalleryDepartments/GalleryDepartments';
import DropDownsList from '@/components/ui/DropDownsList/DropDownsList';
import useServicesStore from '@/store/serviseStore';
import Articles from '../DepartmentArticles/Articles';
import styles from './DepartmentPage.module.scss';
import Spinner from '@/components/ui/Spinner/Spinner';

const DepartmentPage = ({ id, title, showSelect, articles }) => {
  const subDepartments = useServicesStore(state => state.subDepartments);
  const { getSubDepartments } = useServicesStore();
  const [departmentId, setDepartmentId] = useState();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const changeDepartment = url => {
    console.log('url: ', url);

    setDepartmentId(url);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getSubDepartments(id);
      } catch (error) {
        console.error('Error:', error);
      }
    };
    fetchData();
  }, [id, getSubDepartments]);

  useEffect(() => {
    setDepartmentId(subDepartments?.[0]?.id);
  }, [subDepartments]);

  useEffect(() => {
    changeDepartment(departmentId);
  }, [departmentId]);

  return (
    <Container>
      <div className={styles.contentWrapper}>
        <h2 className="department_title ">{title}</h2>
        {subDepartments?.length > 0 ? (
          <div className={styles.wrapper}>
            <Articles articles={articles} title={title} />
            <DropDownsList departmentId={id} />
            <GalleryDepartments
              showSelect={showSelect}
              selectOptions={subDepartments}
              url={'gallery'}
              departmentId={departmentId}
              changeDepartment={changeDepartment}
            />
            <Achievements
              title={'Досягнення відділу'}
              showSelect={showSelect}
              selectOptions={subDepartments}
              url={'achievement'}
              departmentId={departmentId}
              changeDepartment={changeDepartment}
            />
          </div>
        ) : (
          <Spinner />
        )}
      </div>
    </Container>
  );
};

export default DepartmentPage;
