import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useModal } from '@/store/modalStore';
import useDepartmentsStore from '@/store/departmentsStore';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import DepartmentsTable from '@/components/admin-components/Departments/DepartmentsTable/DepartmentsTable';
import DepartmentsTabs from '@/components/admin-components/Departments/DepartmentsTabs/DepartmentsTabs';
import SpinnerAdmin from '@/components/admin-components/SpinnerAdmin/SpinnerAdmin';
import PlaceholderAdmin from '@/components/admin-components/PlaceholderAdmin/PlaceholderAdmin';

const DepartmentPageAdmin = () => {
  const { id } = useParams();
  const { isModalOpen } = useModal();
  const { getOneDepartment, getDepartments } = useDepartmentsStore();
  const [thisDepartment, setThisdepartment] = useState([]);
  const [title, setTitle] = useState([]);
  const department = useDepartmentsStore(state => state.department);
  const departments = useDepartmentsStore(state => state.departments);
  const loading = useDepartmentsStore(state => state.loading);
  const error = useDepartmentsStore(state => state.error);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getDepartments();
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [getDepartments]);

  useEffect(() => {
    const foundDepartment = departments.filter(item => item.id == id);
    setThisdepartment(foundDepartment);
  }, [id, departments]);

  useEffect(() => {
    if (thisDepartment) {
      setTitle(thisDepartment[0]?.department_name);
    }
  }, [thisDepartment]);

  const breadcrumbs = ['Відділення', `${title}`];

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getOneDepartment(id);
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [getOneDepartment, isModalOpen, id]);

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title={`${title}`}
        showBackButton={false}
        showActionButton={true}
        actionButtonLink="/admin/departments/sub_department/add"
        isActionButtonDisabled={false}
        actionButtonLabel="Додати відділ"
        stateTitle={title}
        stateId={id}
      />
      <DepartmentsTabs departments={departments} />
      {loading && !Object.keys(error).length ? (
        <SpinnerAdmin />
      ) : (
        <DepartmentsTable
          data={department}
          departmentId={thisDepartment[0]?.id}
        />
      )}
      {error && Object.keys(error).length ? <PlaceholderAdmin /> : null}
    </div>
  );
};

export default DepartmentPageAdmin;
