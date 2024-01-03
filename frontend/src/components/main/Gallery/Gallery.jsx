import { useRef, useState, useEffect } from 'react';
import { useMediaQuery } from 'react-responsive';
import Container from '@/components/Container/Container';
import NavLinkButton from '@/components/ui/Buttons/NavLinkButton';
import { Pagination } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import useServicesStore from '@/store/serviseStore';
import Spinner from '@/components/ui/Spinner/Spinner';
import Placeholder from '@/components/ui/Placeholder/Placeholder';
import s from './Gallery.module.scss';

const Gallery = () => {
  const { getMainAchievements } = useServicesStore();
  const swiperRef = useRef();
  const isDesktop = useMediaQuery({ minWidth: 1024 });
  const gallery = useServicesStore(state => state.gallery);
  const [loadingState, setLoadingState] = useState('loading');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoadingState('loading');
        await getMainAchievements('gallery');
        setLoadingState('success');
      } catch (error) {
        setLoadingState('error');
      }
    };
    fetchData();
  }, [getMainAchievements]);

  return (
    <Container>
      <section className={s.gallerySection}>
        <h2 className={s.title}>Галерея</h2>

        {isDesktop && (
          <div className={s.ButtonContainer}>
            <NavLinkButton text={'Дивитися більше'} href={'/gallery'} />
          </div>
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
        {loadingState === 'success' &&
          gallery?.length > 0 &&
          (isDesktop ? (
            <div className={s.gallery}>
              {gallery.map((image, i) => (
                <div key={i} className={s.item}>
                  <img
                    src={image.media}
                    alt={image.description}
                  
                  />
                </div>
              ))}
            </div>
          ) : (
            <Swiper
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
              onSwiper={swiper => {
                swiperRef.current = swiper;
              }}
            >
              {gallery.map((slide, index) => (
                <SwiperSlide key={index} className={s.slide}>
                  <img src={slide.media} alt={slide.description} />
                </SwiperSlide>
              ))}
            </Swiper>
          ))}
        {!isDesktop && (
          <div className={s.ButtonContainer}>
            <NavLinkButton text={'Дивитися більше'} href={'/gallery'} />
          </div>
        )}
      </section>
    </Container>
  );
};

export default Gallery;
