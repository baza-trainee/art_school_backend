import articles from '@/data/departments/finearts';
import DepartmentPage from '@/components/departments/DepartmentPage/DepartmentPage';

const FineArtsDepartment = () => {
  return (
    <DepartmentPage
      id={'5'}
      showSelect={true}
      title={'Образотворче відділення'}
      articles={articles}
    />
  );
};

export default FineArtsDepartment;
