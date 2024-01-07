import { useEffect } from 'react';
import useVideoStore from '@/store/videoStore';
import useGalleryStore from '@/store/galleryStore';
import Container from '@/components/Container/Container';
import GalleryVideo from '@/components/gallery_page/GalleryVideo/GalleryVideo';
import YoutubeLink from '@/components/gallery_page/YoutubeLink/YoutubeLink';
import GalleryImages from '@/components/gallery_page/GalleryImages/GalleryImages';
import PageTitle from '@/components/ui/PageTitle/PageTitle';
import Spinner from '@/components/ui/Spinner/Spinner';
import styles from './Gallery.module.scss';

const Gallery = () => {
  const { getAllVideo } = useVideoStore();
  const { getAllImages } = useGalleryStore();
  const videos = useVideoStore(state => state.videos);
  const images = useGalleryStore(state => state.images);
  const loading = useVideoStore(state => state.loading);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  useEffect(() => {
    const fetchVideo = async () => {
      try {
        await getAllVideo();
        await getAllImages();
      } catch (error) {
        console.log(error);
      }
    };
    fetchVideo();
  }, [getAllVideo, getAllImages]);

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
            <GalleryImages images={images} />
          </>
        )}
      </section>
    </Container>
  );
};

export default Gallery;
