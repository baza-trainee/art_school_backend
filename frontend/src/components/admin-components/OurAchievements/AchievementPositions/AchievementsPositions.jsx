import { useEffect, useState } from 'react';
import s from './AchievementPositions.module.scss';

const AchievementPositions = ({
  field,
  title,
  form: { setFieldValue },
  activePosition,
  achievementPositions,
}) => {
  const name = field.name;
  const [isActivePosition, setIsActivePosition] = useState(activePosition);
  const positionsCount =
    achievementPositions?.free_positions?.length +
    achievementPositions?.taken_positions?.length;

  useEffect(() => {
    if (!activePosition) return;
    setFieldValue(`${name}`, activePosition);
    setIsActivePosition(activePosition);
  }, [setFieldValue, activePosition, name]);

  const renderRadios = () => {
    const radios = [];

    for (let i = 1; i <= positionsCount; i++) {
      const isActive = isActivePosition === i;
      const isTaken =
        i === isActivePosition || i === activePosition
          ? false
          : achievementPositions?.taken_positions?.includes(i) || false;
      let inputClassName;
      if (isActive) {
        inputClassName = s.active;
      } else if (isTaken) {
        inputClassName = s.taken;
      } else {
        inputClassName = s.free;
      }
      radios.push(
        <div key={i} className={s.radioContainer}>
          <label htmlFor={`radio-${i}`} className={s.label}>
            Фото{i}
          </label>
          <input
            className={inputClassName}
            type="radio"
            id={`radio-${i}`}
            name="position"
            disabled={isTaken}
            checked={isActive}
            onClick={() => {
              if (isActive) {
                setFieldValue(`${name}`, ''); // Скасовує вибір, якщо вже обрано
                setIsActivePosition('');
              }
            }}
            onChange={() => {
              setFieldValue(`${name}`, i);
              setIsActivePosition(i);
            }}
          />
        </div>
      );
    }
    return radios;
  };

  return (
    <div className={s.container}>
      <h4 className={s.title}>{title}</h4>
      <div className={s.radioList}>{renderRadios()}</div>
    </div>
  );
};

export default AchievementPositions;

/*
import { useEffect, useState } from 'react';
import s from './AchievementPositions.module.scss';

const AchievementPositions = ({
  field,
  title,
  form: { setFieldValue },
  activePosition,
  achievementPositions,
}) => {
  const name = field.name;
  const [isActivePosition, setIsActivePosition] = useState(activePosition);
  const positionsCount = achievementPositions?.free_positions?.length + achievementPositions?.taken_positions?.length;
  useEffect(() => {
    if (!activePosition) return;
    setFieldValue(`${name}`, activePosition);
    setIsActivePosition(activePosition);
  }, [setFieldValue, activePosition, name]);

  const renderRadios = () => {
    const radios = [];

    for (let i = 1; i <= positionsCount; i++) {
      const isActive = isActivePosition === i;
      const isTaken = (i === isActive || i === activePosition) ? false : achievementPositions?.taken_positions?.includes(i) || false;
      let inputClassName;
      if (isActive) {
        inputClassName = s.active;
      } else if (isTaken) {
        inputClassName = s.taken;
      } else {
        inputClassName = s.free;
      }
      radios.push(
        <div key={i} className={s.radioContainer}>
          <label htmlFor={`radio-${i}`} className={s.label}>
            Фото{i}
          </label>
          <input
            className={inputClassName}
            type="radio"
            id={`radio-${i}`}
            name="position"
            disabled={isTaken}
            checked={isActive}
            onChange={() => {
              setFieldValue(`${name}`, i);
              setIsActivePosition(i);
            }}
          />
        </div>
      );
    }
    return radios;
  };

  return (
    <div className={s.container}>
      <h4 className={s.title}>{title}</h4>
      <div className={s.radioList}>{renderRadios()}</div>
    </div>
  );
};

export default AchievementPositions;
*/
