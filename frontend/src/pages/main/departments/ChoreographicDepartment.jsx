import articles from '@/data/departments/choreographic';
import DepartmentPage from '@/components/departments/DepartmentPage/DepartmentPage';

const ChoreographicDepartment = () => {
  return (
    <DepartmentPage
      id={'3'}
      showSelect={true}
      title={'Хореографічне відділення'}
      articles={articles}
    />
  );
};

export default ChoreographicDepartment;
