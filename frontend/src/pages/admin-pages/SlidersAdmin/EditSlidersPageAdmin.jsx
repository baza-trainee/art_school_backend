import { useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import { useParams, useNavigate } from 'react-router-dom';
import useSlidersStore from '@/store/slidersStore';
import { slidersValidation } from './validationSchema';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import TextInput from '@/components/admin-components/formik/TextInput/TextInput';
import TextArea from '@/components/admin-components/formik/TextArea/TextArea';
import FileInput from '@/components/admin-components/formik/FileInput/FileInput';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import styles from './SlidersAdmin.module.scss';

const breadcrumbs = ['Слайдери', 'Редагувати слайд'];

const initialValues = {
  title: '',
  text: '',
  image: [],
};

const EditSlidersPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { getSlides, editSlide } = useSlidersStore();
  const loading = useSlidersStore(state => state.loading);
  const slide = useSlidersStore(state =>
    state.slides.find(item => item.id == id)
  );

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getSlides();
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [id, getSlides]);

  const onSubmit = async values => {
    try {
      const formData = new FormData();
      formData.append('title', values.title);
      formData.append('description', values.text);

      if (values.image[0].size === 0) {
        formData.append('photo', '');
      } else {
        formData.append('photo', values.image[0]);
      }

      await editSlide(id, formData);
      navigate(-1);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title="Редагувати слайд"
        showBackButton={true}
        backButtonLink="/admin/sliders"
        showActionButton={false}
      />
      <Formik
        initialValues={initialValues}
        validationSchema={slidersValidation}
        onSubmit={onSubmit}
      >
        {formik => {
          return (
            <Form>
              <div className={styles.layout}>
                <Field
                  name="title"
                  id="title"
                  component={TextInput}
                  maxLength={120}
                  showCharacterCount={true}
                  text={slide?.title}
                  label="Заголовок Слайду"
                />
                <div className={styles.secondRow}>
                  <Field
                    name="text"
                    id="text"
                    component={TextArea}
                    maxLength={200}
                    showCharacterCount={true}
                    text={slide?.description}
                    label="Опис Слайду"
                  />
                  <Field
                    name="image"
                    id="image"
                    component={FileInput}
                    photo={slide?.photo}
                    label="Фото*"
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

export default EditSlidersPage;
