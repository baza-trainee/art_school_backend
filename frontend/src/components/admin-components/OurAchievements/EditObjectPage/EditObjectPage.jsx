import { useState, useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import { useNavigate, useParams } from 'react-router-dom';
import { achievementsValidation } from '@/components/admin-components/OurAchievements/validationSchema';
import useServicesStore from '@/store/serviseStore';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import TextArea from '@/components/admin-components/formik/TextArea/TextArea';
import FileInput from '@/components/admin-components/formik/FileInput/FileInput';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import CustomTitle from '@/components/admin-components/OurAchievements/CustomTitle/CustomTitle';
import AchievementPositions from '@/components/admin-components/OurAchievements/AchievementPositions/AchievementsPositions'; // Замініть шлях на реальний
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import s from '../../../../pages/admin-pages/OurAchievementsAdmin/AchievementsAdmin.module.scss';

const initialValues = {
  pinned_position: '',
  sub_department: '',
  description: '',
  image: [],
};

const EditObjectPage = ({
  url,
  pageTitle,
  backButtonLink,
  achievementPositionsTitle,
  selectTitle,
}) => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { getAchievementsPositions, getAchievemenById, editAchievement } =
    useServicesStore();
  const achievement = useServicesStore(state => state.achievement);
  const achievementsPositions = useServicesStore(
    state => state.achievementsPositions
  );
  const title = selectTitle;
  const [isProcessing, setIsProcessing] = useState(false);
  let breadcrumbs;
  const setBreadcrumbs = url => {
    if (url === 'achievements') {
      breadcrumbs = ['Наші Досягнення', 'Редагувати досягнення'];
    } else if (url === 'gallery') {
      breadcrumbs = ['Фотогалерея', 'Редагувати фото'];
    }
    return breadcrumbs;
  };
  setBreadcrumbs(url);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getAchievementsPositions(url);
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }, [getAchievementsPositions, url]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getAchievemenById(url, id);
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }, [getAchievemenById, id, url]);

  const onSubmit = async values => {
    try {
      const formData = new FormData();
      formData.append('pinned_position', values.pinned_position);
      formData.append('description', values.description);
      values.sub_department === ''
        ? formData.append('sub_department', '')
        : formData.append('sub_department', values.sub_department);
      values.image?.[0].size === 0
        ? formData.append('media', '')
        : formData.append('media', values.image[0]);
      setIsProcessing(true);
      await editAchievement(url, id, formData);
      setIsProcessing(false);
      setTimeout(() => {
        navigate(`/admin/${url}`);
      }, 2000);
    } catch (error) {
      console.error(error);
      setIsProcessing(false);
    }
  };

  return (
    <div className={s.container}>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title={pageTitle}
        showBackButton={true}
        backButtonLink={backButtonLink}
        showActionButton={false}
      />
      <Formik
        initialValues={initialValues}
        validationSchema={achievementsValidation}
        onSubmit={onSubmit}
      >
        {formik => (
          <Form>
            <div className={s.selectBlock}>
              <CustomTitle title={title} width={'fixed'} />
            </div>

            <div className={s.form}>
              <div className={s.fieldSection}>
                <Field
                  name="description"
                  id="description"
                  component={TextArea}
                  maxLength={200}
                  showCharacterCount={true}
                  label="Опис"
                  text={achievement?.description}
                />
                <Field
                  name="image"
                  id="image"
                  component={FileInput}
                  photo={achievement?.media}
                  label="Фото"
                />
              </div>
              <Field
                name="pinned_position"
                id="pinned_position"
                component={AchievementPositions}
                title={achievementPositionsTitle}
                achievementPositions={achievementsPositions}
                activePosition={achievement?.pinned_position}
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

export default EditObjectPage;
