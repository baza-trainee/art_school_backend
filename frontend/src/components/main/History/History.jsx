import Container from '@/components/Container/Container';
import NavLinkButton from '@/components/ui/Buttons/DownloadButton';
import historyData from '@/data/about/history.json';
import styles from './History.module.scss';

const History = () => {
  const url = '/about_school_history';
  const buttonName = 'Читати більше';

  return (
    <Container>
      <div className={styles.wrapper}>
        <div className={styles.info}>
          <p className={`${styles.title} sectionTitle`}>Історія школи</p>
          <p className={styles.text}>{historyData[0].description}</p>
        </div>
        <div className={styles.buttonContainer}>
          <NavLinkButton title={buttonName} to={url} />
        </div>
        <div className={styles.img_container}>
          <img src="/school.webp" alt="school-building" />
        </div>
      </div>
    </Container>
  );
};

export default History;
