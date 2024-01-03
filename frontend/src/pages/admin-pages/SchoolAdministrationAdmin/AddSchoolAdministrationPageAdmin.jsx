import { useNavigate } from 'react-router-dom';
import { Formik, Form, Field } from 'formik';
import { administrationValidation } from './validationSchema';
import useAdministrationStore from '@/store/administrationStore';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import TextInput from '@/components/admin-components/formik/TextInput/TextInput';
import TextArea from '@/components/admin-components/formik/TextArea/TextArea';
import FileInput from '@/components/admin-components/formik/FileInput/FileInput';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import styles from './SchoolAdministration.module.scss';

const breadcrumbs = ['Адміністрація школи', 'Додати працівника'];

const initialValues = {
  full_name: '',
  position: '',
  image: [],
};

const AddSchoolAdministrationPage = () => {
  const navigate = useNavigate();
  const { addMember } = useAdministrationStore();
  const loading = useAdministrationStore(state => state.loading);

  const onSubmit = async values => {
    try {
      const formData = new FormData();
      formData.append('full_name', values.full_name);
      formData.append('position', values.position);
      formData.append('photo', values.image[0]);

      await addMember(formData);
      navigate(-1);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title="Додати працівника адміністрації"
        showBackButton={true}
        backButtonLink="/admin/administration"
        showActionButton={false}
      />
      <Formik
        initialValues={initialValues}
        validationSchema={administrationValidation}
        onSubmit={onSubmit}
      >
        {formik => {
          return (
            <Form>
              <div className={styles.layout}>
                <Field
                  name="full_name"
                  id="full_name"
                  component={TextInput}
                  maxLength={120}
                  showCharacterCount={true}
                  label="ПІБ Працівника"
                />
                <div className={styles.secondRow}>
                  <Field
                    name="position"
                    id="position"
                    component={TextArea}
                    maxLength={2000}
                    showCharacterCount={true}
                    label="Посада Працівника"
                  />
                  <Field
                    name="image"
                    id="image"
                    component={FileInput}
                    label="Фото"
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

export default AddSchoolAdministrationPage;
