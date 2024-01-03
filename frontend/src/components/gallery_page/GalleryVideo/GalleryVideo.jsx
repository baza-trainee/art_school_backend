import { useRef, useState, useEffect } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Mousewheel } from 'swiper/modules';
import { useMediaQuery } from 'react-responsive';
import Arrow from '@/components/Icons/Arrow/Arrow';
import styles from './GalleryVideo.module.scss';
import 'swiper/css/pagination';
import 'swiper/css';

const GalleryVideo = ({ videos }) => {
  const swiperRef = useRef(null);
  const [isUpHovered, setIsUpHovered] = useState(false);
  const [isDownHovered, setIsDownHovered] = useState(false);

  const isLaptop = useMediaQuery({ minWidth: 1280 });
  const isTablet = useMediaQuery({ minWidth: 768 });
  const isMobile = useMediaQuery({ maxWidth: 767 });

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const replaceUrl = url => {
    if (url && url.length) {
      return url?.replace('watch?v=', 'embed/');
    }
  };

  return (
    <>
      {isLaptop && (
        <div className={styles.videoWrapper}>
          <div className={styles.video}>
            {videos.length > 0 && Array.isArray(videos) && (
              <iframe
                src={replaceUrl(videos[0]?.media)}
                title="Відео з життя школи"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen
              ></iframe>
            )}
          </div>

          {videos.length > 0 && (
            <div className={styles.videos}>
              <button
                onClick={() => swiperRef.current.slidePrev()}
                onMouseEnter={() => setIsUpHovered(true)}
                onMouseLeave={() => setIsUpHovered(false)}
                className={styles.arrowUp}
              >
                <Arrow isHovered={isUpHovered} direction="up" />
              </button>
              <button
                onClick={() => swiperRef.current.slideNext()}
                onMouseEnter={() => setIsDownHovered(true)}
                onMouseLeave={() => setIsDownHovered(false)}
                className={styles.arrowDown}
              >
                <Arrow isHovered={isDownHovered} direction="down" />
              </button>
              <Swiper
                direction={'vertical'}
                slidesPerView={2}
                spaceBetween={15}
                mousewheel={true}
                modules={[Mousewheel]}
                onSwiper={swiper => (swiperRef.current = swiper)}
                className={styles.swiper}
              >
                {videos &&
                  Array.isArray(videos) &&
                  videos.slice(1).map((video, index) => (
                    <SwiperSlide className={styles.slide} key={index}>
                      <iframe
                        src={replaceUrl(video?.media)}
                        width="382"
                        height="190"
                        title="Відео з життя школи"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        allowfullscreen
                      ></iframe>
                    </SwiperSlide>
                  ))}
              </Swiper>
            </div>
          )}
        </div>
      )}

      {isTablet && !isLaptop && (
        <div className={styles.videoWrapper}>
          {videos.length > 0 && (
            <div className={styles.videos}>
              <button
                onClick={() => swiperRef.current.slidePrev()}
                onMouseEnter={() => setIsUpHovered(true)}
                onMouseLeave={() => setIsUpHovered(false)}
                className={styles.arrowUp}
              >
                <Arrow isHovered={isUpHovered} direction="up" />
              </button>
              <button
                onClick={() => swiperRef.current.slideNext()}
                onMouseEnter={() => setIsDownHovered(true)}
                onMouseLeave={() => setIsDownHovered(false)}
                className={styles.arrowDown}
              >
                <Arrow isHovered={isDownHovered} direction="down" />
              </button>
              <Swiper
                direction={'vertical'}
                slidesPerView={1}
                spaceBetween={25}
                mousewheel={true}
                modules={[Mousewheel]}
                onSwiper={swiper => (swiperRef.current = swiper)}
                className={styles.swiper}
              >
                {videos &&
                  Array.isArray(videos) &&
                  videos.map((video, index) => (
                    <SwiperSlide className={styles.slide} key={index}>
                      <iframe
                        src={replaceUrl(video?.media)}
                        width="382"
                        height="190"
                        title="Відео з життя школи"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        allowfullscreen
                      ></iframe>
                    </SwiperSlide>
                  ))}
              </Swiper>
            </div>
          )}
        </div>
      )}

      {isMobile && (
        <div className={styles.videoWrapper}>
          <div className={styles.videos}>
            <button
              onClick={() => swiperRef.current.slidePrev()}
              onMouseEnter={() => setIsUpHovered(true)}
              onMouseLeave={() => setIsUpHovered(false)}
              className={styles.arrowUp}
            >
              <Arrow isHovered={isUpHovered} direction="left" />
            </button>
            <button
              onClick={() => swiperRef.current.slideNext()}
              onMouseEnter={() => setIsDownHovered(true)}
              onMouseLeave={() => setIsDownHovered(false)}
              className={styles.arrowDown}
            >
              <Arrow isHovered={isDownHovered} direction="right" />
            </button>
            <Swiper
              direction={'horizontal'}
              slidesPerView={1}
              spaceBetween={25}
              mousewheel={true}
              modules={[Mousewheel]}
              onSwiper={swiper => (swiperRef.current = swiper)}
              className={styles.swiper}
            >
              {videos &&
                Array.isArray(videos) &&
                videos.map((video, index) => (
                  <SwiperSlide className={styles.slide} key={index}>
                    <iframe
                      src={replaceUrl(video?.media)}
                      width="382"
                      height="190"
                      allowFullScreen
                    ></iframe>
                  </SwiperSlide>
                ))}
            </Swiper>
          </div>
        </div>
      )}
    </>
  );
};

export default GalleryVideo;
