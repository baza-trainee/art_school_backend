import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Formik, Form, Field } from 'formik';
import { recoveryValidation } from './validationSchema';
import useAuthStore from '@/store/authStore';
import Heading from '../Heading/Heading';
import ButtonSubmit from '../../Buttons/SubmitButton/ButtonSubmit.jsx';
import TextInput from '@/components/admin-components/formik/TextInput/TextInput';
import PasswordRecoveryAlert from '../../modals/PasswordRecoveryAlert/PasswordRecoveryAlert';
import styles from './PasswordRecovery.module.scss';

const initialValues = {
  email: '',
};

const PasswordRecovery = () => {
  const { sendMail } = useAuthStore();
  const [isAlertOpen, setIsAlertOpen] = useState(false);
  const [message, setMessage] = useState('');

  const onSubmit = async values => {
    try {
      const data = {
        email: values.email,
      };
      setIsAlertOpen(true);
      setMessage(
        'Якщо у вас є акаунт, вам на електронну пошту буде надіслано посилання для відновлення паролю'
      );
      const response = await sendMail(data);
      if (response && response.detail.status === 'success') {
        setMessage('Листа надіслано. Перевірте електронну пошту');
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <Heading title="Відновлення паролю" />
      <p className={styles.message}>
        Введіть електронну пошту, пов’язану з вашим акаунтом Якщо у вас є
        акаунт, вам на електронну пошту буде надіслано посилання для відновлення
        паролю
      </p>
      <Formik
        initialValues={initialValues}
        onSubmit={onSubmit}
        validationSchema={recoveryValidation}
      >
        {formik => {
          return (
            <Form>
              <div className={styles.layout}>
                <Field
                  name="email"
                  id="email"
                  component={TextInput}
                  showCharacterCount={false}
                  label="Електронна пошта*"
                  placeholder="name@mail.com"
                />
                <div className={styles.button}>
                  <ButtonSubmit
                    handlerSubmitButton={onSubmit}
                    nameButton="Надіслати"
                    isActive={formik.isValid && formik.touched['email']}
                  />
                </div>
              </div>
            </Form>
          );
        }}
      </Formik>
      <Link to="/login" className={styles.link}>
        Я згадав пароль!
      </Link>
      {isAlertOpen && (
        <PasswordRecoveryAlert
          setIsAlertOpen={setIsAlertOpen}
          message={message}
        />
      )}
    </>
  );
};
export default PasswordRecovery;
