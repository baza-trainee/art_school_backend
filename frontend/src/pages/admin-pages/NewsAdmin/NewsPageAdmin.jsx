import { useEffect } from 'react';
import useNewsStore from '@/store/newsStore';
import NewsTable from '@/components/admin-components/News/NewsTable/NewsTable';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import SpinnerAdmin from '@/components/admin-components/SpinnerAdmin/SpinnerAdmin';
import PlaceholderAdmin from '@/components/admin-components/PlaceholderAdmin/PlaceholderAdmin';

const breadcrumbs = ['Новини'];

const NewsPageAdmin = () => {
  const { getNews } = useNewsStore();
  const news = useNewsStore(state => state.news);
  const loading = useNewsStore(state => state.loading);
  const error = useNewsStore(state => state.error);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getNews();
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [getNews]);

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title="Новини"
        showBackButton={false}
        showActionButton={true}
        actionButtonLink="/admin/news/add"
        isActionButtonDisabled={false}
        actionButtonLabel="Додати новину"
      />
      {loading && !Object.keys(error).length ? (
        <SpinnerAdmin />
      ) : (
        <NewsTable data={news} />
      )}
      {error && Object.keys(error).length ? <PlaceholderAdmin /> : null}
    </div>
  );
};

export default NewsPageAdmin;
