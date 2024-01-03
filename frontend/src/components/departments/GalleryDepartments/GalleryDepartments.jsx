import { useState, useEffect, useRef } from 'react';
import { useMediaQuery } from 'react-responsive';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import SwiperButtons from '@/components/ui/SwiperButtons/SwiperButtons';
import Select from '@/components/ui/Select/Select';
import useServicesStore from '@/store/serviseStore';
import Spinner from '@/components/ui/Spinner/Spinner';
import Placeholder from '@/components/ui/Placeholder/Placeholder';
import s from './GalleryDepartments.module.scss';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css';

const GalleryDepartments = ({
  url,
  departmentId,
  changeDepartment,
  showSelect,
  selectOptions,
}) => {
  console.log('  selectOptions: ', selectOptions);
  const { getDepartmentAchievements } = useServicesStore();
  const gallery = useServicesStore(state => state.gallery);
  const isDextop = useMediaQuery({ minWidth: 1280 });
  const swiperGalaryRef = useRef();
  const [loadingState, setLoadingState] = useState('loading');

  useEffect(() => {
    const fetchData = async () => {
      setLoadingState('loading');
      try {
        await getDepartmentAchievements(url, departmentId);
        setLoadingState('success');
      } catch (error) {
        setLoadingState('error');
      }
    };
    fetchData();
  }, [getDepartmentAchievements, url, departmentId]);

  return (
    <section className={s.galary}>
      {showSelect && isDextop && (
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
      {loadingState === 'success' && gallery?.length > 0 && (
        <div className={s.slidersContainer}>
          {isDextop && (
            <SwiperButtons
              onPrevClick={() => swiperGalaryRef.current.slidePrev()}
              onNextClick={() => swiperGalaryRef.current.slideNext()}
            />
          )}
          <Swiper
            onSwiper={swiper => {
              swiperGalaryRef.current = swiper;
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
            {gallery.map(item => (
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
      {showSelect && !isDextop && (
        <Select
          title="Обрати відділ"
          options={selectOptions}
          changeDepartment={changeDepartment}
        />
      )}
    </section>
  );
};

export default GalleryDepartments;
