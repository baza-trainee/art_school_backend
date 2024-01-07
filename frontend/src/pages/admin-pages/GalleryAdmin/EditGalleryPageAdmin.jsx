import EditObjectPage from "@/components/admin-components/OurAchievements/EditObjectPage/EditObjectPage";

const EditGalleryPage = () => {
  return (
    <EditObjectPage
      pageTitle='Додати фото'
      backButtonLink='/admin/gallery'
      achievementPositionsTitle='Закріпити в галерею на головній сторінці'
      url="gallery"
      selectTitle='Всі фото'
      maxSymbols={150}
    />
  );
};

export default EditGalleryPage;
