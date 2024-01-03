import { useRef, useEffect, useState } from 'react';
import { useMediaQuery } from 'react-responsive';
import { Pagination } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import { formatDate } from '@/utils/formatDate';
import useNewsStore from '@/store/newsStore';
import Container from '@/components/Container/Container';
import Placeholder from '@/components/ui/Placeholder/Placeholder';
import NavLinkButton from '@/components/ui/Buttons/NavLinkButton';
import Navigation from './Navigation/Navigation';
import styles from './News.module.scss';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css';
import { Link } from 'react-router-dom';
import usePostersStore from '@/store/posterStore';
import Spinner from '@/components/ui/Spinner/Spinner';

const News = () => {
  const swiperRef = useRef();
  const isLaptop = useMediaQuery({ minWidth: 1024 });
  const { getNews } = useNewsStore();
  const news = useNewsStore(state => state.news);
  const loading = usePostersStore(state => state.loading);

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
    <Container>
      <section className={styles.News}>
        <h1>Новини</h1>
        {isLaptop && (
          <div className={styles.ButtonContainer}>
            <NavLinkButton text={'Переглянути всі новини'} href={'/news'} />
          </div>
        )}
        {!loading ? (
          <div className={styles.wrapper}>
            {news?.length > 0 ? (
              <Swiper
                className={styles.Slider}
                spaceBetween={50}
                slidesPerView={1}
                modules={[Pagination]}
                pagination={{ clickable: true }}
                loop={true}
                onSwiper={swiper => {
                  swiperRef.current = swiper;
                }}
              >
                {news &&
                  Array.isArray(news) &&
                  news.map((slide, index) => (
                    <SwiperSlide key={index} className={styles.Slide}>
                      <div className={styles.image}>
                        {loading && (
                          <div className={styles.errorData}>
                            Завантаження...
                          </div>
                        )}
                        {!loading && (
                          <img
                            src={slide.photo}
                            alt={slide.title}
                            loading="lazy"
                          />
                        )}
                      </div>
                      <div className={styles.Text}>
                        <span>{formatDate(slide.created_at)}</span>
                        <p>{slide.title}</p>
                      </div>
                    </SwiperSlide>
                  ))}
                {isLaptop && (
                  <Navigation
                    onPrevClick={() => swiperRef.current.slidePrev()}
                    onNextClick={() => swiperRef.current.slideNext()}
                  />
                )}
              </Swiper>
            ) : (
              <div className={styles.errorData}>
                <Placeholder />
              </div>
            )}
          </div>
        ) : (
          <Spinner />
        )}

        {!isLaptop && (
          <div className={styles.ButtonContainer}>
            <NavLinkButton text={'Переглянути всі новини'} href={'/news'} />
          </div>
        )}
      </section>
    </Container>
  );
};

export default News;
