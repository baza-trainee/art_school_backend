import AddNewObjectPage from '@/components/admin-components/OurAchievements/AddNewObjectPage/AddNewObjectPage';

const AddGalleryPage = () => {
  return (
    <AddNewObjectPage
      pageTitle='Додати фото'
      backButtonLink='/admin/gallery'
      achievementPositionsTitle='Закріпити в галерею на головній сторінці'
      url="gallery"
      selectTitle='Всі фото'
      maxSymbols={150}
    />
  );
};

export default AddGalleryPage;
