import { useState } from 'react';
import { clsx } from 'clsx';
import { Link } from 'react-router-dom';
import useSlidersStore from '@/store/slidersStore';
import { useModal } from '@/store/modalStore';
import { useConfirmDelete } from '@/store/confirmDelete';
import { subString } from '@/utils/subString';
import ConfirmDeleteModal from '@/components/admin-components/modals/ConfirmDeleteModal/ConfirmDeleteModal';
import styles from './SlidersTable.module.scss';
import sprite from '@/assets/icons/sprite-admin.svg';

const SlidersTable = ({ data }) => {
  const { deleteSlide } = useSlidersStore();
  const { isDeleteConfirm } = useConfirmDelete();
  const { isModalOpen, openModal, closeModal } = useModal();
  const [currentId, setCurrentId] = useState('');

  const removePost = async () => {
    if (isDeleteConfirm && data.length > 1) {
      try {
        await deleteSlide(currentId);
      } catch (error) {
        console.log(error);
      }
    } else {
      closeModal();
    }
  };

  return (
    <div className={styles.contentWrap}>
      <ul className={styles.tableHeader}>
        <li className={styles.cellSlideHeader}>Слайди</li>
        <li className={styles.cellHeadingHeader}>Заголовок Слайду</li>
        <li className={styles.cellTextHeader}>Опис Слайду</li>
        <li className={styles.cellPhotoHeader}>Фото</li>
        <li className={styles.cellActionHeader}>Дія</li>
      </ul>
      <div className={styles.tbody}>
        {data &&
          Array.isArray(data) &&
          data.map((item, index) => (
            <div className={styles.tableRow} key={index}>
              <div className={styles.cellSliderRow}>{index + 1}</div>
              <div className={styles.cellHeadingRow}>{item.title}</div>
              <div className={styles.cellTextRow}>
                {subString(item.description)}
              </div>
              <div className={styles.cellPhotoRow}>
                <img
                  src={item.photo}
                  alt={item.title}
                  className={styles.contentElementImg}
                />
              </div>

              <div className={styles.cellActionRow}>
                <Link to={`edit/${item.id}`}>
                  <div className={styles.cellActionContainer}>
                    <svg className={styles.iconEdit}>
                      <use
                        href={`${sprite}#icon-edit`}
                        width="20"
                        height="20"
                      />
                    </svg>
                  </div>
                </Link>
                <button
                  className={styles.cellActionContainer}
                  onClick={openModal}
                  disabled={index === 0}
                >
                  <svg
                    className={clsx(
                      styles.iconTrash,
                      index === 0 && styles.disabled
                    )}
                    onClick={() => setCurrentId(item.id)}
                  >
                    <use href={`${sprite}#icon-trash`} width="20" height="20" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
      </div>
      {isModalOpen && <ConfirmDeleteModal handleDelete={removePost} />}
    </div>
  );
};
export default SlidersTable;
