import { useState, useEffect, useRef } from 'react';
import { useMediaQuery } from 'react-responsive';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import SwiperButtons from '@/components/ui/SwiperButtons/SwiperButtons';
import Select from '@/components/ui/Select/Select';
import useServicesStore from '@/store/serviseStore';
import Spinner from '@/components/ui/Spinner/Spinner';
import Placeholder from '@/components/ui/Placeholder/Placeholder';
import s from './Achievements.module.scss';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css';

const Achievements = ({
  title,
  url,
  departmentId,
  changeDepartment,
  showSelect,
  selectOptions,
}) => {
  const swiperRef = useRef();
  const isDesktop = useMediaQuery({ minWidth: 1024 });
  const { getMainAchievements, getDepartmentAchievements } = useServicesStore();
  const achievements = useServicesStore(state => state.achievements);
  const [loadingState, setLoadingState] = useState('loading');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoadingState('loading');
        if (url === 'achievements') {
          await getMainAchievements(url);
        } else {
          await getDepartmentAchievements(url, departmentId);
        }
        setLoadingState('success');
      } catch (error) {
        setLoadingState('error');
      }
    };
    fetchData();
  }, [getMainAchievements, getDepartmentAchievements, url, departmentId]);

  return (
    <section className={s.achievements}>
      <h2>{title}</h2>
      {showSelect && isDesktop && (
        <Select
          title="Обрати відділ"
          options={selectOptions}
          changeDepartment={changeDepartment}
        />
      )}
      {loadingState === 'loading' && (
        <div className={s.errorData}>
          <Spinner />
        </div>
      )}
      {loadingState === 'error' && (
        <div className={s.errorData}>
          <Placeholder />
        </div>
      )}
      {loadingState === 'success' && achievements?.length > 0 && (
        <div className={s.slidersContainer}>
          {isDesktop && (
            <SwiperButtons
              onPrevClick={() => swiperRef.current.slidePrev()}
              onNextClick={() => swiperRef.current.slideNext()}
            />
          )}
          <Swiper
            onSwiper={swiper => {
              swiperRef.current = swiper;
            }}
            className={s.slider}
            modules={[Pagination]}
            spaceBetween={16}
            slidesPerView={1}
            breakpoints={{
              768: {
                slidesPerView: 2,
              },
              1280: {
                slidesPerView: 3,
              },
            }}
            pagination={{ clickable: true }}
            loop={true}
          >
            {achievements.map(item => (
              <SwiperSlide className={s.slideContent} key={item.id}>
                <div className={s.slidePhoto}>
                  <img src={item.media} alt={item.description} />
                </div>
                <p className={s.slideText}>{item.description}</p>
              </SwiperSlide>
            ))}
          </Swiper>
        </div>
      )}
      {showSelect && !isDesktop && (
        <Select
          title="Обрати відділ"
          options={selectOptions}
          changeDepartment={changeDepartment}
        />
      )}
    </section>
  );
};

export default Achievements;
