import styles from './Pagetitle.module.scss';

const PageTitle = ({ title }) => {
  return (
    <div className={styles.title}>
      <h1>{title}</h1>
    </div>
  );
};

export default PageTitle;
