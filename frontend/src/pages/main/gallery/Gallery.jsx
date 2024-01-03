import { useEffect } from 'react';
import useVideoStore from '@/store/videoStore';
import useServicesStore from '@/store/serviseStore';
import Container from '@/components/Container/Container';
import GalleryVideo from '@/components/gallery_page/GalleryVideo/GalleryVideo';
import YoutubeLink from '@/components/gallery_page/YoutubeLink/YoutubeLink';
import GalleryImages from '@/components/gallery_page/GalleryImages/GalleryImages';
import PageTitle from '@/components/ui/PageTitle/PageTitle';
import Spinner from '@/components/ui/Spinner/Spinner';
import styles from './Gallery.module.scss';

const Gallery = () => {
  const { getAllVideo } = useVideoStore();
  const { getAllAchievements } = useServicesStore();
  const videos = useVideoStore(state => state.videos);
  const gallery = useServicesStore(state => state.gallery);
  const loading = useVideoStore(state => state.loading);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  useEffect(() => {
    const fetchVideo = async () => {
      try {
        await getAllVideo();
        await getAllAchievements('gallery');
      } catch (error) {
        console.log(error);
      }
    };
    fetchVideo();
  }, [getAllVideo, getAllAchievements]);

  return (
    <Container>
      <section className={styles.Gallery}>
        <PageTitle title="Галерея" />
        <YoutubeLink />
        {loading ? (
          <Spinner />
        ) : (
          <>
            <GalleryVideo videos={videos} />
            <GalleryImages images={gallery} />
          </>
        )}
      </section>
    </Container>
  );
};

export default Gallery;
