import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useModal } from '@/store/modalStore';
import { useConfirmDelete } from '@/store/confirmDelete';
import { subString } from '@/utils/subString';
import useDepartmentsStore from '@/store/departmentsStore';
import ConfirmDeleteModal from '@/components/admin-components/modals/ConfirmDeleteModal/ConfirmDeleteModal';
import styles from './DepartmentsTable.module.scss';
import sprite from '@/assets/icons/sprite-admin.svg';

const DepartmentsTable = ({ data, departmentId }) => {
  const { deleteSubDepartment } = useDepartmentsStore();
  const { isDeleteConfirm } = useConfirmDelete();
  const { isModalOpen, openModal, closeModal } = useModal();
  const [currentId, setCurrentId] = useState('');

  const removePost = async () => {
    if (isDeleteConfirm) {
      console.log(currentId);
      try {
        await deleteSubDepartment(currentId);
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
        <li className={styles.cellHeadingHeader}>Відділ</li>
        <li className={styles.cellTextHeader}>Опис Відділу</li>
        <li className={styles.cellActionHeader}>Дія</li>
      </ul>
      <div className={styles.tbody}>
        {data &&
          Array.isArray(data) &&
          data.map((item, index) => (
            <div className={styles.tableRow} key={index}>
              <div className={styles.cellHeadingRow}>
                {item.sub_department_name}
              </div>
              <div className={styles.cellTextRow}>
                {subString(item.description)}
              </div>
              <div className={styles.cellActionRow}>
                <Link
                  to={`/admin/departments/sub_department/edit/${item.id}`}
                  state={{
                    title: item.sub_department_name,
                    departmentId: departmentId,
                  }}
                >
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
                  onClick={openModal}
                  className={styles.cellActionContainer}
                >
                  <svg
                    className={styles.iconTrash}
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
export default DepartmentsTable;
