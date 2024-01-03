import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import useNewsStore from '@/store/newsStore';
import Spinner from '@/components/ui/Spinner/Spinner';
import NewsItem from './news_item/NewsItem';
import Container from '@/components/Container/Container';
import ViewButton from '@/components/ui/Buttons/ViewButton/ViewButton';

import styles from './AllNews.module.scss';

const AllNews = () => {
  const ITEMS_PER_PAGE = 6;
  const { getNews } = useNewsStore();
  const news = useNewsStore(state => state.news);
  const loading = useNewsStore(state => state.loading);
  const [itemsPerPage, setItemsPerPage] = useState(ITEMS_PER_PAGE);
  const isMaxAmount = itemsPerPage >= news.length;

  const viewMore = () => {
    if (!isMaxAmount) {
      setItemsPerPage(prev => prev + ITEMS_PER_PAGE);
    }
  };
  const viewLess = () => {
    setItemsPerPage(ITEMS_PER_PAGE);
    window.scrollTo(0, 0);
  };

  useEffect(() => {
    const fetchNews = async () => {
      await getNews();
    };
    fetchNews();
  }, [getNews]);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <Container>
      <section className={styles.wrapper}>
        <p className={`${styles.title} sectionTitle`}>Новини</p>
        {loading ? (
          <Spinner />
        ) : (
          <div className={styles.newsWrapper}>
            {news &&
              Array.isArray(news) &&
              news.slice(0, itemsPerPage).map((item, index) => (
                <Link
                  to={`/news/${item.id}`}
                  state={{ post: item }}
                  key={index}
                >
                  <NewsItem
                    imgSrc={item.photo}
                    date={item.created_at}
                    title={item.title}
                  />
                </Link>
              ))}
          </div>
        )}
        <div className={styles.buttonContainer}>
          {news.length > ITEMS_PER_PAGE && (
            <ViewButton
              isMaxAmount={isMaxAmount}
              viewMore={viewMore}
              viewLess={viewLess}
            />
          )}
        </div>
      </section>
    </Container>
  );
};

export default AllNews;
