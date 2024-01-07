import { useState, useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import { useNavigate, useParams } from 'react-router-dom';
import {
  achievementsValidation,
  galleryValidation,
} from '@/components/admin-components/OurAchievements/achievementsValidationSchema';
import useServicesStore from '@/store/serviseStore';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import TextArea from '@/components/admin-components/formik/TextArea/TextArea';
import FileInput from '@/components/admin-components/formik/FileInput/FileInput';
import ButtonSubmit from '@/components/admin-components/Buttons/SubmitButton/ButtonSubmit';
import CustomTitle from '@/components/admin-components/OurAchievements/CustomTitle/CustomTitle';
import SelectAdminDouble from '@/components/admin-components/OurAchievements/SelectAdminDouble/SelectAdminDouble';
import AchievementPositions from '@/components/admin-components/OurAchievements/AchievementPositions/AchievementsPositions'; // Замініть шлях на реальний
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import s from '../../../../pages/admin-pages/OurAchievementsAdmin/AchievementsAdmin.module.scss';
import axios from '@/utils/axios';
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
  maxSymbols,
}) => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { getAchievementsPositions, getAchievemenById, editAchievement } =
    useServicesStore();
  const achievement = useServicesStore(state => state.achievement);
  const achievementsPositions = useServicesStore(
    state => state.achievementsPositions
  );
  const [isProcessing, setIsProcessing] = useState(false);
  const subDepartmentId = achievement.sub_department;
  const [title, setTitle] = useState(selectTitle);

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
    if (subDepartmentId) {
      axios
        .get(`/departments/sub_department/${subDepartmentId}`)
        .then(response => setTitle(response.data.sub_department_name))
        .catch(error => console.error(error));
    }
  }, [subDepartmentId]);

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
        validationSchema={
          url === 'achievements' ? achievementsValidation : galleryValidation
        }
        onSubmit={onSubmit}
      >
        {formik => (
          <Form>
            <div className={s.selectBlock}>
              <CustomTitle title={title} width={'fixed'} />
              <SelectAdminDouble
                changeDepartment={(id, title) => {
                  if (id !== undefined && id !== null) {
                    formik.setFieldValue('sub_department', id);
                    setTitle(title);
                  }
                }}
              />
            </div>

            <div className={s.form}>
              <div
                className={`${s.fieldSection} ${
                  url !== 'achievements' && s.reverse
                }`}
              >
                <Field
                  name="description"
                  id="description"
                  component={TextArea}
                  maxLength={maxSymbols}
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
                activePosition={achievement.pinned_position}
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
