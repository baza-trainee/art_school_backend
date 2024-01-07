import Container from '@/components/Container/Container';
import { useEffect } from 'react';
import historyData from '@/data/about/history.json';
import styles from './SchoolHistory.module.scss';
const SchoolHistory = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <section>
      <Container>
        <div className={styles.contentWrapper}>
          <h1 className="department_title">Історія нашої школи</h1>
          <div>
            <div className={styles.imgWrapper}>
              <p>{historyData[0].description}</p>
              <img
                src={historyData[0].media}
                alt=" будівля школи 
              "
              />
            </div>
            <div>
              {historyData.slice(1, historyData.length - 1).map(text => (
                <p key={text.id} className={styles.text}>
                  {text.description}
                </p>
              ))}
              <p className={`${styles.text} ${styles.text_bold}  `}>
                Tворімо історію нашого міста разом!
              </p>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
};

export default SchoolHistory;
