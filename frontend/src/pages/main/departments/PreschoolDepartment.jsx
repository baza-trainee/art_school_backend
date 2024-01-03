import articles from '@/data/departments/preschool';
import DepartmentPage from '@/components/departments/DepartmentPage/DepartmentPage';

const PreschoolDepartment = () => {
  return (
    <DepartmentPage
      id={'6'}
      showSelect={false}
      title={'Дошкільне та підготовче відділення'}
      articles={articles}
    />
  );
};

export default PreschoolDepartment;
