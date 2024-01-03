import { useState, useEffect } from 'react';
import SortIcon from '@/components/Icons/SortIcon';
import ViewButton from '@/components/ui/Buttons/ViewButton/ViewButton';

import styles from './GalleryImages.module.scss';

const GalleryImages = ({ images }) => {
  const ITEMS_PER_PAGE = 5;
  const [isHovered, setIsHovered] = useState(false);
  const [itemsPerPage, setItemsPerPage] = useState(ITEMS_PER_PAGE);
  const [sorting, setSorting] = useState(false);
  const [sortedImages, setSortedImages] = useState(images);
  const isMaxAmount = images?.length <= itemsPerPage;

  const viewMore = () => {
    if (!isMaxAmount) {
      setItemsPerPage(prev => prev + ITEMS_PER_PAGE);
    }
  };

  const viewLess = () => {
    setItemsPerPage(ITEMS_PER_PAGE);
    window.scrollTo(0, 0);
  };

  useEffect(() => {
    if (sorting) {
      setSortedImages(
        images.sort(
          (a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        )
      );
    } else {
      setSortedImages(
        images.sort(
          (a, b) =>
            new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        )
      );
    }
  }, [setSortedImages, sorting, images]);

  return (
    <>
      {images?.length > 0 && (
        <div className={styles.sort}>
          <button onClick={() => setSorting(!sorting)}>
            {images?.length > 0 && <SortIcon />}
            {!sorting
              ? ' Сортування від новіших до старіших'
              : ' Сортування від старіших до новіших'}
          </button>
        </div>
      )}

      <div className={styles.gallery}>
        {sortedImages &&
          Array.isArray(sortedImages) &&
          sortedImages.slice(0, itemsPerPage).map((image, index) => (
            <div key={image.id} className={styles.item}>
              <img src={image.media} alt={`Image ${index + 1}`} />
            </div>
          ))}
      </div>

      {images.length > ITEMS_PER_PAGE && (
        <ViewButton
          isHovered={isHovered}
          setIsHovered={setIsHovered}
          isMaxAmount={isMaxAmount}
          viewMore={viewMore}
          viewLess={viewLess}
        />
      )}
    </>
  );
};

export default GalleryImages;
