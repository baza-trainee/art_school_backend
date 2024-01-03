import AchievementsGalleryPage from '@/components/admin-components/OurAchievements/AchievementsGalleryPage/AchievementsGalleryPage';

const GalleryPage = () => {
  return (
    <AchievementsGalleryPage
      url="gallery"
      pageTitle='Фотогалерея'
      actionButtonLink="/admin/gallery/add"
      actionButtonLabel='Додати Фото'
      selectTitle="Всі фото"
      buttonTitle1="Галерея"
      buttonTitle2="Закріпленні фотографії"
    />
  );
};

export default GalleryPage;
