import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useConfirmDelete } from '@/store/confirmDelete';
import { useModal } from '@/store/modalStore';
import usePostersStore from '@/store/posterStore';
import ConfirmDeleteModal from '@/components/admin-components/modals/ConfirmDeleteModal/ConfirmDeleteModal';
import styles from './PostersList.module.scss';
import sprite from '@/assets/icons/sprite-admin.svg';

const PostersList = ({ data }) => {
  const { deletePostersById } = usePostersStore();
  const { isDeleteConfirm } = useConfirmDelete();
  const { isModalOpen, openModal, closeModal } = useModal();
  const [currentId, setCurrentId] = useState('');

  const handleDelete = async () => {
    if (isDeleteConfirm) {
      try {
        await deletePostersById(currentId);
      } catch (error) {
        console.log(error);
      }
    } else {
      closeModal();
    }
  };

  return (
    <div className={styles.contentWrap}>
      <div className={styles.tableHeader}>
        <p className={styles.cellHeadingHeader}>Заголовок Афіші</p>
        <div className={styles.cellActionWrapper}>
          <p className={styles.cellPhotoHeader}>Фото</p>
          <p className={styles.cellActionHeader}>Дія</p>
        </div>
      </div>
      <div className={styles.tbody}>
        {data.map((item, index) => (
          <div className={styles.tableRow} key={index}>
            <div className={styles.cellTextWrapper}>
              <div className={styles.cellHeadingRow}>{item.title}</div>
            </div>

            <div className={styles.cellPosterWrapper}>
              <div className={styles.cellPhotoRow}>
                <img
                  src={item.photo}
                  alt="Фото"
                  className={styles.contentElementImg}
                />
              </div>
              <div className={styles.cellActionRow}></div>

              <div className={styles.cellActionContainer}>
                <Link to={`edit/${item.id}`}>
                  <svg className={styles.iconEdit}>
                    <use href={`${sprite}#icon-edit`} width="20" height="20" />
                  </svg>
                </Link>
              </div>
              <div className={styles.cellActionContainer} onClick={openModal}>
                <svg
                  className={styles.iconTrash}
                  onClick={() => setCurrentId(item.id)}
                >
                  <use href={`${sprite}#icon-trash`} width="20" height="20" />
                </svg>
              </div>
            </div>
          </div>
        ))}
      </div>
      {isModalOpen && <ConfirmDeleteModal handleDelete={handleDelete} />}
    </div>
  );
};
export default PostersList;
