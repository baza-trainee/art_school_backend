import { useState } from 'react';
import { Link } from 'react-router-dom';
import useAdministrationStore from '@/store/administrationStore';
import { useModal } from '@/store/modalStore';
import { useConfirmDelete } from '@/store/confirmDelete';
import ConfirmDeleteModal from '@/components/admin-components/modals/ConfirmDeleteModal/ConfirmDeleteModal';
import styles from './AdminTable.module.scss';
import sprite from '@/assets/icons/sprite-admin.svg';

const AdminTable = ({ data }) => {
  const { deleteMember } = useAdministrationStore();
  const { isDeleteConfirm } = useConfirmDelete();
  const { isModalOpen, openModal, closeModal } = useModal();
  const [currentId, setCurrentId] = useState('');

  const removeMember = async () => {
    if (isDeleteConfirm) {
      try {
        await deleteMember(currentId);
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
        <li className={styles.cellHeadingHeader}>ПІБ Працівника</li>
        <li className={styles.cellTextHeader}>Посада</li>
        <li className={styles.cellPhotoHeader}>Фото</li>
        <li className={styles.cellActionHeader}>Дія</li>
      </ul>
      <div className={styles.tbody}>
      {data &&
        Array.isArray(data) &&
        data.map((item, index) => (
          <div className={styles.tableRow} key={index}>
            <div className={styles.cellHeadingRow}>{item.full_name}</div>
            <div className={styles.cellTextRow}>{item.position}</div>
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
                    <use href={`${sprite}#icon-edit`} width="20" height="20" />
                  </svg>
                </div>
              </Link>

              <button
                onClick={() => {
                  setCurrentId(item.id);
                  openModal();
                }}
              >
                <svg className={styles.iconTrash}>
                  <use href={`${sprite}#icon-trash`} width="20" height="20" />
                </svg>
              </button>
            </div>
          </div>
        ))}
        </div>
      {isModalOpen && <ConfirmDeleteModal handleDelete={removeMember} />}
    </div>
  );
};
export default AdminTable;
