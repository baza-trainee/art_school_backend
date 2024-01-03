import { useNavigate, useLocation } from 'react-router-dom';
import { Formik, Form, Field } from 'formik';
import { newsValidation } from './validationSchema';
import { declineWord } from '@/utils/declineWord';
import useDepartmentsStore from '@/store/departmentsStore';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import TextInput from '@/components/admin-components/formik/TextInput/TextInput';
import TextArea from '@/components/admin-components/formik/TextArea/TextArea';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import styles from './DepartmentsAdmin.module.scss';

const initialValues = {
  title: '',
  text: '',
};

const AddSubDepartmentPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { title, departmentId } = location.state;
  const { addDepartment } = useDepartmentsStore();
  const loading = useDepartmentsStore(state => state.loading);

  const breadcrumbs = [
    'Відділення',
    `${title}`,
    `Додати відділ ${declineWord(title)}`,
  ];

  const onSubmit = async values => {
    try {
      const newSubDepartment = {
        sub_department_name: values.title,
        description: values.text,
        main_department_id: departmentId,
      };
      await addDepartment(newSubDepartment);
      setTimeout(() => {
        navigate(`/admin/departments/${departmentId}`);
      }, 2000);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title={`Додати відділ ${declineWord(title)}`}
        showBackButton={true}
        backButtonLink={`/admin/departments/${departmentId}`}
        showActionButton={false}
      />
      <Formik
        initialValues={initialValues}
        validationSchema={newsValidation}
        onSubmit={onSubmit}
      >
        {formik => {
          return (
            <Form>
              <div className={styles.layout}>
                <div className={styles.secondRow}>
                  <Field
                    name="title"
                    id="title"
                    placeholder="Title"
                    component={TextInput}
                    maxLength={120}
                    showCharacterCount={true}
                    label="Назва Відділу"
                  />
                  <Field
                    name="text"
                    id="text"
                    placeholder="Title"
                    component={TextArea}
                    maxLength={2000}
                    showCharacterCount={true}
                    label="Опис"
                  />
                </div>
                <div className={styles.button}>
                  <ButtonSubmit
                    nameButton="Зберегти зміни"
                    isActive={formik.isValid}
                    isRight={true}
                    handlerSubmitButton={onSubmit}
                    isProcessing={loading}
                  />
                </div>
              </div>
            </Form>
          );
        }}
      </Formik>
    </div>
  );
};

export default AddSubDepartmentPage;
