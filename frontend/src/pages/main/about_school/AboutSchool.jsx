import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useMediaQuery } from 'react-responsive';

import Container from '@/components/Container/Container';
import Administration from '@/pages/main/about_school/Administration/Administration';
import Museum from './Museum';

import aboutUsData from '@/data/about/about.json';
import historyData from '@/data/about/history.json';
import museumData from '@/data/about/museum.json';

import styles from './AboutSchool.module.scss';

const AboutSchool = () => {
  const isDesktop = useMediaQuery({ minWidth: 1280 });

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <>
      {/* <h1 className=''>про школу </h1> */}
      <section className={styles.history}>
        <Container>
          <div className={styles.history_wrapper}>
            <h2 className="department_title ">Історія школи</h2>
            <div className={styles.history_contentWrapper}>
              <div className={styles.history_textWrapper}>
                <p className={styles.history_content_text}>
                  {historyData[0].description}
                </p>
                {isDesktop && (
                  <Link
                    className={styles.readMoreButton}
                    to="/about_school_history"
                  >
                    Читати більше
                  </Link>
                )}
              </div>
              <img
                className={styles.history_content_img}
                src={historyData[0].media}
                alt=" scholl building  "
              />
            </div>

            {!isDesktop && (
              <Link
                className={styles.readMoreButton}
                to="/about_school_history"
              >
                Читати більше
              </Link>
            )}
          </div>
        </Container>
      </section>
      <section className={styles.aboutUs} id="about_us">
        <Container>
          <div className={styles.aboutUs_wrapper}>
            <h2 className="department_title">Про нас </h2>

            <div className={styles.aboutUs_contentWrapper}>
              <div className={styles.content}>
                <p className={styles.aboutUs_text}>
                  {aboutUsData.description1}
                  hello
                </p>
                <img
                  className={styles.aboutUs_img}
                  src={aboutUsData.media}
                  alt=""
                />
              </div>

              <div className={styles.benefits}>
                <ul className={styles.benefits_list}>
                  {aboutUsData.benefits.map((benefit, index) => (
                    <li key={index} className={styles.benefits_listItem}>
                      <p className={styles.benefits_listItem_text}>
                        {' '}
                        {benefit}
                      </p>
                    </li>
                  ))}
                </ul>
                <p className={styles.aboutUs_text}>
                  {aboutUsData.description2}
                </p>
              </div>
            </div>
          </div>
        </Container>
      </section>
      <section className={styles.museum} id="museum">
        <Container>
          <div className={styles.museum_contentWrapper}>
            <h2 className="department_title">Музей Михайла Вериківського</h2>
            <Museum museumData={museumData} />
          </div>
        </Container>
      </section>
      <section className={styles.administration} id="administration">
        <Container>
          <Administration />
        </Container>
      </section>
    </>
  );
};

export default AboutSchool;
