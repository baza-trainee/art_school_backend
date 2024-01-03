import { useState, useEffect, useRef } from 'react';
import { useMediaQuery } from 'react-responsive';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import SwiperButtons from '@/components/ui/SwiperButtons/SwiperButtons';
import Spinner from '@/components/ui/Spinner/Spinner';
import useAdministrationStore from '@/store/administrationStore';
import s from './Administration.module.scss';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css';

const Administration = () => {
  const { getMembers } = useAdministrationStore();
  const isDextop = useMediaQuery({ minWidth: 1280 });
  const swiperAdministrationRef = useRef();
  const [loadingState, setLoadingState] = useState('loading');
  const members = useAdministrationStore(state => state.members);

  useEffect(() => {
    const fetchData = async () => {
      setLoadingState('loading');
      try {
        await getMembers();

        setLoadingState('success');
      } catch (error) {
        setLoadingState('error');
      }
    };
    fetchData();
  }, [getMembers]);

  return (
    <div className={s.administration_contentWrapper}>
      <h2 className="department_title">Адміністрація школи</h2>
      <div className={s.slidersContainer}>
        {loadingState === 'loading' && <Spinner />}
        {loadingState === 'success' ? (
          members && members.length > 0 ? (
            <div className={s.slidersContainer}>
              {isDextop && (
                <SwiperButtons
                  onPrevClick={() =>
                    swiperAdministrationRef.current.slidePrev()
                  }
                  onNextClick={() =>
                    swiperAdministrationRef.current.slideNext()
                  }
                />
              )}
              <Swiper
                onSwiper={swiper => {
                  swiperAdministrationRef.current = swiper;
                }}
                className={s.slider}
                modules={[Pagination]}
                spaceBetween={16}
                slidesPerView={1.2}
                breakpoints={{
                  768: {
                    slidesPerView: 2.1,
                  },
                  1280: {
                    slidesPerView: 3,
                  },
                }}
                pagination={{ clickable: true }}
                loop={true}
              >
                {members.map(item => (
                  <SwiperSlide className={s.slideContent} key={item.id}>
                    <div className={s.slidePhoto}>
                      <img src={item.photo} alt={item.full_name} />
                    </div>
                    <p className={s.slideText_name}>{item.full_name}</p>
                    <p className={s.slideText_position}>{item.position}</p>
                  </SwiperSlide>
                ))}
              </Swiper>
            </div>
          ) : (
            <div className={s.errorData}>Дані тимчасово відсутні</div>
          )
        ) : (
          loadingState === 'error' && (
            <div className={s.errorData}>Дані тимчасово відсутні</div>
          )
        )}
      </div>
    </div>
  );
};

export default Administration;
