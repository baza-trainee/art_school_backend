import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { Formik, Form, Field } from 'formik';
import usePostersStore from '@/store/posterStore';
import { posterValidation } from './validationSchema';
import TextArea from '@/components/admin-components/formik/TextArea/TextArea';
import FileInput from '@/components/admin-components/formik/FileInput/FileInput';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import styles from './PostersAdmin.module.scss';

const breadcrumbs = ['Афіші', 'Редагувати афішу'];

const initialValues = {
  title: '',
  image: [],
};

const EditPostersPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { getPostersById } = usePostersStore();
  const { updatePoster } = usePostersStore();
  const loading = usePostersStore(state => state.loading);
  const poster = usePostersStore(state => state.poster);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getPostersById(id);
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [getPostersById, id]);

  const onSubmit = async values => {
    try {
      const formData = new FormData();
      formData.append('title', values.title);

      if (values.image[0].size === 0) {
        formData.append('photo', '');
      } else {
        formData.append('photo', values.image[0]);
      }

      await updatePoster(formData, id);
      navigate(-1);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <div>
        <PageTitle
          title="Редагувати Афішу"
          showBackButton={true}
          backButtonLink="/admin/posters"
          showActionButton={false}
        />
        <Formik
          initialValues={initialValues}
          validationSchema={posterValidation}
          onSubmit={onSubmit}
        >
          {formik => {
            return (
              <Form>
                <div className={styles.layout}>
                  <div className={styles.inputWrapper}>
                    <Field
                      name="title"
                      id="title"
                      placeholder="Title"
                      component={TextArea}
                      maxLength={120}
                      showCharacterCount={true}
                      text={poster?.title}
                      label="Заголовок Афіші"
                    />
                    <Field
                      name="image"
                      id="image"
                      component={FileInput}
                      photo={poster?.photo}
                    />
                  </div>
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
              </Form>
            );
          }}
        </Formik>
      </div>
    </div>
  );
};

export default EditPostersPage;
