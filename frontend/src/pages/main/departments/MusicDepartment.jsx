import DepartmentPage from '@/components/departments/DepartmentPage/DepartmentPage';
import articles from '@/data/departments/music';

const MusicDepartment = () => {
  return (
    <DepartmentPage
      id={'1'}
      showSelect={true}
      title={'Музичне відділення'}
      articles={articles}
    />
  );
};

export default MusicDepartment;
