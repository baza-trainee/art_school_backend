import { useLocation } from 'react-router-dom';

import Container from '@/components/Container/Container';

import styles from './NewsPost.module.scss';
import NavLinkButton from '@/components/ui/Buttons/NavLinkButton';
import { formatDate } from '@/utils/formatDate';

const NewsPost = () => {
  const location = useLocation();
  const { post } = location.state;

  return (
    <Container>
      <section className={styles.wrapper}>
        <div className={styles.buttonContainer}>
          <NavLinkButton href={'/news'} text={'переглянути всі новини'} />
        </div>
        <p className={`${styles.title} sectionTitle`}>{post.title}</p>
        <p className={styles.date}>{formatDate(post.created_at)}</p>
        <div className={styles.img}>
          <img src={post.photo} alt="slide" />
        </div>
        <p className={styles.text}>{post.text}</p>
      </section>
    </Container>
  );
};

export default NewsPost;
