import styles from './Articles.module.scss';

const Articles = ({ articles, title }) => {
  return (
    <>
      {articles &&
        Array.isArray(articles) &&
        articles.map((article, index) => (
          <article key={index} className={styles.article}>
            <div className={styles.textWrapper}>
              <p className={styles.text}>{article.text}</p>
            </div>
            <div className={styles.image}>
              <img src={article.image} alt={title} />
            </div>
          </article>
        ))}
    </>
  );
};

export default Articles;
