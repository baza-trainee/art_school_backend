import { useNavigate } from 'react-router-dom';
import { useModal } from '@/store/modalStore';
import styles from './ConfirmModal.module.scss';
import sprite from '@/assets/icons/sprite-admin.svg';

const ConfirmModal = ({ message }) => {
  const navigate = useNavigate();
  const { closeModal } = useModal();

  return (
    <div className={styles.modal}>
      <div className={styles.contentWrapper}>
        <p>{message}</p>
        <svg>
          <use href={`${sprite}#icon-success`} width="90" height="90" />
        </svg>
        <button
          onClick={() => {
            closeModal();
            navigate('/login');
          }}
        >
          Закрити
        </button>
      </div>
    </div>
  );
};

export default ConfirmModal;
