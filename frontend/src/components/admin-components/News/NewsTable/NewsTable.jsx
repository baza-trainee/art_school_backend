import { useState } from 'react';
import { Link } from 'react-router-dom';
import useNewsStore from '@/store/newsStore';
import { useModal } from '@/store/modalStore';
import { useConfirmDelete } from '@/store/confirmDelete';
import { subString } from '@/utils/subString';
import ConfirmDeleteModal from '@/components/admin-components/modals/ConfirmDeleteModal/ConfirmDeleteModal';
import styles from './NewsTable.module.scss';
import sprite from '@/assets/icons/sprite-admin.svg';

const NewsTable = ({ data }) => {
  const { deletePost } = useNewsStore();
  const { isDeleteConfirm } = useConfirmDelete();
  const { isModalOpen, openModal, closeModal } = useModal();
  const [currentId, setCurrentId] = useState('');

  const removePost = async () => {
    if (isDeleteConfirm) {
      try {
        await deletePost(currentId);
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
        <li className={styles.cellHeadingHeader}>Заголовок Новини</li>
        <li className={styles.cellTextHeader}>Текст Новини</li>
        <li className={styles.cellPhotoHeader}>Фото</li>
        <li className={styles.cellActionHeader}>Дія</li>
      </ul>
      <div className={styles.tbody}>
        {data &&
          Array.isArray(data) &&
          data.map((item, index) => (
            <div className={styles.tableRow} key={index}>
              <div className={styles.cellHeadingRow}>{item.title}</div>
              <div className={styles.cellTextRow}>{subString(item.text)}</div>
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
                  onClick={() => {
                    setCurrentId(item.id);
                    openModal();
                  }}
                  className={styles.cellActionContainer}
                >
                  <svg className={styles.iconTrash}>
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
export default NewsTable;
