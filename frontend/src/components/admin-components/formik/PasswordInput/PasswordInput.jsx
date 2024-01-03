import { useState } from 'react';
import { useFocused } from '@/store/focusStore';
import { FaRegEye, FaRegEyeSlash } from 'react-icons/fa';
import styles from './PasswordInput.module.scss';

const PasswordInput = ({
  id,
  field,
  label,
  form: { errors, handleBlur, touched },
  maxLength,
  showCharacterCount,
  placeholder,
}) => {
  const isFieldTouched = touched[field.name];
  const valueLength = field.value.length;
  const { isFocused, setIsFocused } = useFocused();
  const [inputType, setInputType] = useState('password-hide');

  const handleInputType = e => {
    e.preventDefault();
    setInputType(prev =>
      prev === 'password-show' ? 'password-hide' : 'password-show'
    );
  };

  const handleFocus = () => {
    setIsFocused(field.name);
  };

  const getBorderColor = () => {
    if (errors?.[field.name]) {
      return styles.redBorder;
    }
    if (isFocused === field.name) {
      return styles.blueBorder;
    }
    if (valueLength === 0 && isFieldTouched) {
      return styles.redBorder;
    }
    if (valueLength > 0) {
      return styles.greenBorder;
    } else {
      return styles.grayBorder;
    }
  };

  const getInputState = () => {
    if (valueLength > maxLength) {
      return styles.error;
    } else if (valueLength > 0 && !isFocused) {
      return styles.entered;
    } else {
      return '';
    }
  };
  return (
    <div className={styles.inputWrapper}>
      <label htmlFor={id} className={styles.inputLabel}>
        {label}
      </label>
      <div className={`${styles.wrapper}`}>
        <input
          id={id}
          type={inputType === 'password-hide' ? 'password' : 'text'}
          className={`${styles.input} ${getBorderColor()} ${getInputState()}`}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onClick={() => setIsFocused(field.name)}
          placeholder={placeholder ? placeholder : ''}
          {...field}
        />
        <button className={styles.icon} onClick={handleInputType}>
          {inputType === 'password-hide' ? <FaRegEyeSlash /> : <FaRegEye />}
        </button>
      </div>

      {showCharacterCount && (
        <div className={styles.commentsWrapper}>
          <p
            className={`${styles.counterMessage} ${
              valueLength > maxLength ? styles.redText : ''
            }`}
          >
            {`${valueLength}/${maxLength}`}
          </p>
        </div>
      )}
      {errors?.[field.name] && (
        <div className={styles.commentsWrapper}>
          <div className={styles.errorWrap}>
            {errors?.[field.name] && isFieldTouched && (
              <p className={styles.errorMessage}>{errors?.[field.name]}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default PasswordInput;
