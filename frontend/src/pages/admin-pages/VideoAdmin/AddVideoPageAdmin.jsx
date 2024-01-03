import { useState } from 'react';
import { Formik, Form, Field } from 'formik';
import { useNavigate } from 'react-router-dom';
import useVideoStore from '@/store/videoStore';
import { videoValidation } from './validationSchema';
import TextInput from '@/components/admin-components/formik/TextInput/TextInput';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';

import s from './VideoPage.module.scss';

const breadcrumbs = ['Відеогалерея', 'Додати відео'];
const initialValues = {
  media: '',
};

const AddVideoPage = () => {
  const { addVideo } = useVideoStore();
  const navigate = useNavigate();
  const [isProcessing, setIsProcessing] = useState(false);

  const onSubmit = async value => {
    try {
      const formData = new FormData();
      formData.append('media', value.media);
      setIsProcessing(true);
      await addVideo(formData);
      setIsProcessing(false);
      navigate(-1);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className={s.container}>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title="Додати відео в галерею"
        showBackButton={true}
        backButtonLink="/admin/video"
        showActionButton={false}
      />
      <Formik
        initialValues={initialValues}
        validationSchema={videoValidation}
        onSubmit={onSubmit}
      >
        {formik => (
          <Form>
            <div className={s.form}>
              <Field
                name="media"
                id="media"
                placeholder="_Link"
                component={TextInput}
                maxLength={200}
                label="Посилання відео"
              />
              <div className={s.button}>
                <ButtonSubmit
                  nameButton="Зберегти зміни"
                  isActive={formik.isValid}
                  isRight={true}
                  handlerSubmitButton={formik.handleSubmit}
                  isProcessing={isProcessing}
                />
              </div>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default AddVideoPage;
