import { useMediaQuery } from 'react-responsive';
import styles from './YoutubeLink.module.scss';

const YoutubeLink = () => {
  const isMobile = useMediaQuery({ maxWidth: 767 });
  return (
    <div className={styles.youtubeLink}>
      <p>
        Дивитися більше відео {isMobile && <br />} на нашому
        <a
          href="https://www.youtube.com/@ArtSchoolVerykivskogo"
          target="_blank"
          rel="noreferrer"
        >
          <img src="/icons/youtube-icon.svg" alt="youtube" />
        </a>
      </p>
    </div>
  );
};

export default YoutubeLink;
