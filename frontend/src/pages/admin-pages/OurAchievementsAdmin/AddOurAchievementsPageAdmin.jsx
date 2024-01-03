import AddNewObjectPage from '@/components/admin-components/OurAchievements/AddNewObjectPage/AddNewObjectPage';

const AddOurAchievementsPage = () => {
  return (
    <AddNewObjectPage
      pageTitle='Додати досягнення'
      backButtonLink='/admin/achievements'
      achievementPositionsTitle='Закріпити в  блок “Наші досягнення на головній сторінці”'
      url="achievements"
      selectTitle='Всі досягнення'
    />
  );
};

export default AddOurAchievementsPage;
