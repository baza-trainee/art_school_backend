import { useState, useRef } from 'react';
import { useClickOutside } from '@/hooks/hooks';
import s from './Select.module.scss';

const Select = ({ title, options, changeDepartment }) => {
  const [isOptionsVisible, setOptionsVisible] = useState(false);
  const toggleOptions = () => {
    setOptionsVisible(!isOptionsVisible);
  };
  const selectRef = useRef(null);
  const selectOptionsRef = useRef(null);
  useClickOutside([selectRef, selectOptionsRef], () => {
    if (isOptionsVisible) {
      toggleOptions();
    }
  });

  return (
    <div className={s.selectContainer}>
      <button
        className={s.selectButton}
        onClick={toggleOptions}
        ref={selectRef}
      >
        {title}
      </button>
      {isOptionsVisible && (
        <div className={s.optionsContainer} ref={selectOptionsRef}>
          {options.map(option => (
            <div
              key={option.id}
              className={s.option}
              onClick={() => {
                changeDepartment(option.id);
                toggleOptions();
              }}
            >
              {option.sub_department_name}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Select;
