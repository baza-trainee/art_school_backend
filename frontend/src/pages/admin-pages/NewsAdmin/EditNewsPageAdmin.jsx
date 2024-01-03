import { useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import { useParams, useNavigate } from 'react-router-dom';
import useNewsStore from '@/store/newsStore';
import { newsValidation } from './validationSchema';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import TextInput from '@/components/admin-components/formik/TextInput/TextInput';
import TextArea from '@/components/admin-components/formik/TextArea/TextArea';
import FileInput from '@/components/admin-components/formik/FileInput/FileInput';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import styles from './NewsAdmin.module.scss';

const breadcrumbs = ['Новини', 'Редагувати новину'];

const initialValues = {
  title: '',
  text: '',
  image: [],
};

const EditNewsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { getOnePost, editPost } = useNewsStore();
  const post = useNewsStore(state => state.post);
  const loading = useNewsStore(state => state.loading);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getOnePost(id);
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [id, getOnePost]);

  const onSubmit = async values => {
    try {
      const formData = new FormData();
      formData.append('title', values.title);
      formData.append('text', values.text);

      if (values.image[0].size === 0) {
        formData.append('photo', '');
      } else {
        formData.append('photo', values.image[0]);
      }
      await editPost(id, formData);
      navigate(-1);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title="Редагувати новину"
        showBackButton={true}
        backButtonLink="/admin/news"
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
                <Field
                  name="title"
                  id="title"
                  placeholder="Title"
                  component={TextInput}
                  maxLength={120}
                  showCharacterCount={true}
                  text={post?.title}
                  label="Заголовок Новини"
                />
                <div className={styles.secondRow}>
                  <Field
                    name="text"
                    id="text"
                    placeholder="Title"
                    component={TextArea}
                    maxLength={2000}
                    showCharacterCount={true}
                    text={post?.text}
                    label="Текст Новини"
                  />
                  <Field
                    name="image"
                    id="image"
                    component={FileInput}
                    photo={post?.photo}
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

export default EditNewsPage;
