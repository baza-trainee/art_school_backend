import articles from '@/data/departments/vocal';
import DepartmentPage from '@/components/departments/DepartmentPage/DepartmentPage';

const VocalDepartment = () => {
  return (
    <DepartmentPage
      id={'2'}
      showSelect={true}
      title={'Вокально-хорове відділення'}
      articles={articles}
    />
  );
};

export default VocalDepartment;
