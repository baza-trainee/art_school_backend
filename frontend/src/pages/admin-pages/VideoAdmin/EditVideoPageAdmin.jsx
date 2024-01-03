import { useState, useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import { useNavigate, useParams } from 'react-router-dom';
import useVideoStore from '@/store/videoStore';
import { videoValidation } from './validationSchema';
import TextInput from '@/components/admin-components/formik/TextInput/TextInput';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import s from './VideoPage.module.scss';

const breadcrumbs = ['Відеогалерея', 'Редагувати відео'];
const initialValues = {
  media: '',
};

const EditVideoPage = () => {
  const { getOneVideo, editVideo } = useVideoStore();
  const { id } = useParams();
  const navigate = useNavigate();
  const [isProcessing, setIsProcessing] = useState(false);
  const video = useVideoStore(state => state.video);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getOneVideo(id);
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [id, getOneVideo]);

  const onSubmit = async values => {
    try {
      const formData = new FormData();
      formData.append('media', values.media);
      setIsProcessing(true);
      await editVideo(id, values);
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
        title="Редагувати відео"
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
                text={video?.media}
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

export default EditVideoPage;
