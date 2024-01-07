import { useState } from 'react';
import Arrow from '@/components/Icons/Arrow/Arrow';
import styles from './ViewButton.module.scss';

const ViewButton = ({ isMaxAmount, viewMore, viewLess }) => {
  const [isHovered, setIsHovered] = useState(false);
  return (
    <button
      className={styles.viewMore}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={!isMaxAmount ? viewMore : viewLess}
    >
      {!isMaxAmount ? 'Дивитися більше' : 'Дивитися менше'}
      {!isMaxAmount ? (
        <Arrow isHovered={isHovered} direction="down" />
      ) : (
        <Arrow isHovered={isHovered} direction="up" />
      )}
    </button>
  );
};

export default ViewButton;
