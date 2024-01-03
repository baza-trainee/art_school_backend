import AchievementsGalleryPage from '@/components/admin-components/OurAchievements/AchievementsGalleryPage/AchievementsGalleryPage';

const OurAchievementsPage = () => {
  return(
     <AchievementsGalleryPage 
     url="achievements" 
     pageTitle='Наші досягнення'
     actionButtonLink='/admin/achievements/add'
     actionButtonLabel='Додати Досягнення'
     selectTitle='Всі досягнення'
     buttonTitle1 = 'Наші досягнення'
     buttonTitle2 = 'Закріпленні досягнення'
     />
  );
};

export default OurAchievementsPage;
