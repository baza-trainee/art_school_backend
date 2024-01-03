import { useLocation, useNavigate } from 'react-router-dom';
import { Formik, Form, Field } from 'formik';
import { declineWord } from '@/utils/declineWord';
import { contactsValidation } from './validationSchema';
import useContactsStore from '@/store/contactsStore';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import TextInput from '@/components/admin-components/formik/TextInput/TextInput';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import styles from './ContactsAdmin.module.scss';

const EditContactsPageAdmin = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { key, title, value } = location.state;
  const { editContact } = useContactsStore();
  const loading = useContactsStore(state => state.loading);

  const breadcrumbs = [`${title}`, `Редагувати ${declineWord(title)}`];

  const initialValues = {};

  const onSubmit = async values => {
    try {
      await editContact(values);
      navigate(-1);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title={`Редагувати ${declineWord(title)}`}
        showBackButton={true}
        backButtonLink="/admin/contacts"
        showActionButton={false}
      />
      <Formik
        initialValues={initialValues}
        validationSchema={contactsValidation}
        onSubmit={onSubmit}
      >
        {formik => {
          return (
            <Form>
              <div className={styles.layout}>
                <Field
                  name={`${key.toLowerCase()}`}
                  id={`${key.toLowerCase()}`}
                  component={TextInput}
                  showCharacterCount={false}
                  text={value}
                  label={`${title}`}
                />
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

export default EditContactsPageAdmin;
