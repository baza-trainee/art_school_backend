import { Link } from 'react-router-dom';
import sprite from '@/assets/icons/sprite-admin.svg';
import s from './AchievementsTable.module.scss';

const AchievementsTableRow = ({typeOfAchievements, item, index, setCurrentId, openModal}) => {

  return (
    <div className={s.row}>
      {typeOfAchievements === 'mainAchievements' && (
        <div className={s.num}>{index + 1}</div>
      )}
      <div className={s.description}>{item.description}</div>
      <div className={s.photo}>
        <div>
          <img src={item.media} alt="Фото" />
        </div>
      </div>
      <div className={s.action}>
        <Link to={`edit/${item.id}`}>
          <button className={s.edit}>
            <svg>
              <use href={`${sprite}#icon-edit`} />
            </svg>
          </button>
        </Link>
        <button
          className={s.delete}
          onClick={() => {
            setCurrentId(item.id);
            openModal();
          }}
        >
          <svg>
            <use href={`${sprite}#icon-trash`} />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default AchievementsTableRow;
