import CloseIcon from '@/components/Icons/CloseIcon';
import { useConfirmDelete } from '@/store/confirmDelete';
import { useModal } from '@/store/modalStore';
import styles from './ConfirmDeleteModa.module.scss';

const ConfirmDeleteModal = ({ handleDelete }) => {
  const { confirmDelete } = useConfirmDelete();
  const { closeModal } = useModal();
  return (
    <div className={styles.deleteModal}>
      <div className={styles.contentWrapper}>
        <div onClick={() => closeModal()}>
          <CloseIcon />
        </div>

        <p>Ви дійсно бажаєте видалити?</p>
        <div className={styles.buttonsWrapper}>
          <button
            onClick={() => {
              closeModal();
            }}
          >
            Відміна
          </button>
          <button
            onClick={() => {
              confirmDelete();
              handleDelete();
              closeModal();
            }}
          >
            Видалити
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmDeleteModal;
