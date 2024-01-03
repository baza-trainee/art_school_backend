import EditObjectPage from '@/components/admin-components/OurAchievements/EditObjectPage/EditObjectPage';

const EditOurAchievementsPage = () => {
  return (
    <EditObjectPage
      pageTitle='Редагувати досягнення'
      backButtonLink='/admin/achievements'
      achievementPositionsTitle='Закріпити в  блок “Наші досягнення на головній сторінці”'
      url="achievements"
      selectTitle='Всі досягнення'
    />
  );
};

export default EditOurAchievementsPage;
