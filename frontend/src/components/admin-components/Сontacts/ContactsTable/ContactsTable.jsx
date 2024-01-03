import { Link } from 'react-router-dom';
import { dataKeys } from './dataKeys';
import styles from './ContactsTable.module.scss';
import sprite from '@/assets/icons/sprite-admin.svg';

const ContactsTable = ({ data }) => {
  const dataValues = Object.keys(data);

  return (
    <div className={styles.contentWrap}>
      <ul className={styles.tableHeader}>
        <li className={styles.cellHeadingHeader}>Заголовок</li>
        <li className={styles.cellTextHeader}>Текст</li>
        <li className={styles.cellActionHeader}>Дія</li>
      </ul>
      <div className={styles.tbody}>
        {dataValues.map((item, index) => (
          <div className={styles.tableRow} key={index}>
            <div className={styles.cellHeadingRow}>{dataKeys[index]}</div>
            <div className={styles.cellTextRow}>{data[item]}</div>
            <div className={styles.cellActionRow}>
              <Link
                to={`edit/${item}`}
                state={{ title: dataKeys[index], key: item, value: data[item] }}
              >
                <div className={styles.cellActionContainer}>
                  <svg className={styles.iconEdit}>
                    <use href={`${sprite}#icon-edit`} width="20" height="20" />
                  </svg>
                </div>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default ContactsTable;
