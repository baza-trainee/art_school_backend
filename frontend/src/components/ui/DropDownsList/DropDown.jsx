// DropDown.jsx
import arrowIcon from '../../../assets/icons/bottom-arrow.svg';
import s from './DropDown.module.scss';

const DropDown = ({ subDep, isOpen, onDropDownClick }) => {
  return (
    <div className={s.dropdown}>
      <div className={s.dropdownHead} onClick={onDropDownClick}>
        <p className={s.dropdownName}>{subDep.sub_department_name}</p>
        <button className={isOpen ? s.rotateIcon : s.icon}>
          <img src={arrowIcon} alt="Arrow Icon" />
        </button>
      </div>
      {isOpen && <p className={s.dropdownContent}>{subDep.description}</p>}
    </div>
  );
};

export default DropDown;
