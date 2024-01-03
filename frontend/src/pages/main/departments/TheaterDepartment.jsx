import articles from '@/data/departments/theater';
import DepartmentPage from '@/components/departments/DepartmentPage/DepartmentPage';

const TheaterDepartment = () => {
  return (
    <DepartmentPage
      id={'4'}
      showSelect={false}
      title={'Театральне відділення'}
      articles={articles}
    />
  );
};

export default TheaterDepartment;
