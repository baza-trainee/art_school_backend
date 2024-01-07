import { useState, useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import { useNavigate } from 'react-router-dom';
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
import AchievementPositions from '@/components/admin-components/OurAchievements/AchievementPositions/AchievementsPositions';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import s from '../../../../pages/admin-pages/OurAchievementsAdmin/AchievementsAdmin.module.scss';

const initialValues = {
  pinned_position: '',
  sub_department: '',
  description: '',
  image: [],
};

const AddNewObjectPage = ({
  pageTitle,
  backButtonLink,
  selectTitle,
  achievementPositionsTitle,
  url,
  maxSymbols,
}) => {
  const navigate = useNavigate();
  const { addAchievement, getAchievementsPositions } = useServicesStore();
  const achievementsPositions = useServicesStore(
    state => state.achievementsPositions
  );
  const [title, setTitle] = useState(selectTitle);
  const [isProcessing, setIsProcessing] = useState(false);
  let breadcrumbs;
  const setBreadcrumbs = url => {
    if (url === 'achievements') {
      breadcrumbs = ['Наші Досягнення', 'Додати досягнення'];
    } else if (url === 'gallery') {
      breadcrumbs = ['Фотогалерея', 'Додати фото в галерею'];
    }
    title !== selectTitle ? breadcrumbs.push(title) : '';
    return breadcrumbs;
  };
  setBreadcrumbs(url);

  const onSubmit = async values => {
    try {
      const formData = new FormData();
      formData.append('description', values.description);
      formData.append('pinned_position', values.pinned_position);
      formData.append('sub_department', values.sub_department);
      formData.append('media', values.image?.[0]);
      setIsProcessing(true);
      await addAchievement(url, formData);
      setIsProcessing(false);
      setTimeout(() => {
        navigate(`/admin/${url}`);
      }, 2000);
    } catch (error) {
      console.log(error);
    }
  };
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
                />
                <Field
                  name="image"
                  id="image"
                  component={FileInput}
                  label="Фото"
                />
              </div>

              <Field
                name="pinned_position"
                id="pinned_position"
                component={AchievementPositions}
                title={achievementPositionsTitle}
                achievementPositions={achievementsPositions}
              />

              <div className={s.button}>
                <ButtonSubmit
                  nameButton="Зберегти зміни"
                  isActive={formik.isValid}
                  isRight={true}
                  handlerSubmitButton={onSubmit}
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

export default AddNewObjectPage;
