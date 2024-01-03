import { Link } from 'react-router-dom';
import sprite from '../../../assets/icons/sprite-admin.svg';
import styles from './PageTitle.module.scss';

const PageTitle = ({
  title,
  stateTitle,
  stateId,
  showBackButton,
  backButtonLink,
  showActionButton,
  actionButtonLink,
  isActionButtonDisabled,
  actionButtonLabel,
}) => {
  return (
    <div className={styles.pageTitle}>
      <div className={styles.titleWrap}>
        {showBackButton && (
          <Link
            to={backButtonLink}
            className={styles.backButton}
            state={{ title: stateTitle, departmentId: stateId }}
          >
            <svg width="20" height="21">
              <use href={`${sprite}#icon-arrow-left`} className={styles.icon} />
            </svg>
          </Link>
        )}
        <div className={styles.headerTitle}>{title}</div>
      </div>
      {showActionButton && (
        <Link
          to={actionButtonLink}
          state={{ title: stateTitle, departmentId: stateId }}
          className={`${styles.actionButton} ${
            isActionButtonDisabled ? styles.disabled : ''
          }`}
          disabled={isActionButtonDisabled}
        >
          <svg width="15" height="15">
            <use href={`${sprite}#icon-plus`} className={styles.iconPlus} />
          </svg>
          {actionButtonLabel && <span>{actionButtonLabel}</span>}
        </Link>
      )}
    </div>
  );
};

export default PageTitle;
