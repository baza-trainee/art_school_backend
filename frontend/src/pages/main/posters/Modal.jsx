import { useEffect } from 'react';
import styles from './Modal.module.scss'
const  Modal=({toggleModal, children }) =>{
  const closeOnBackdropClick = event => {
    if (event.target === event.currentTarget) toggleModal();
  };

  useEffect(() => {
    const handleEscKeyDown = event => {
      if (event.code === 'Escape') toggleModal();
    };
    window.addEventListener('keydown', handleEscKeyDown);
    return () => {
      window.removeEventListener('keydown', handleEscKeyDown);
    };
  }, [toggleModal]);

  return (
    <div className={styles.Overlay} onClick={closeOnBackdropClick}>
      <div className={styles.Modal} onClick={toggleModal}>
        {children}

        {/* <button onClick={toggleModal} aria-label="close">
          <AiOutlineClose />
        </button> */}
      </div>
    </div>
  );

}

export default Modal
