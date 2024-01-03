import { useState } from 'react';
import PropTypes from 'prop-types';
import styles from './InputSm.module.scss';

const InputSm = ({
  label,
  maxLength,
  errorText,
  showCharacterCount,
  text = '', 
  setText = () => {}, 
}) => {
  // const [text, setText] = useState('');
  const [isFocused, setIsFocused] = useState(false);

  const handleInputChange = event => {
    const inputValue = event.target.value;
    setText(inputValue);
  };

  const handleFocus = () => {
    setIsFocused(true);
  };

  const handleBlur = () => {
    setIsFocused(false);
  };

  const getBorderColor = () => {
    if (text.length > maxLength) {
      return styles.redBorder;
    } else if (isFocused) {
      return styles.blueBorder;
    } else if (text.length > 0 && !isFocused) {
      return styles.greenBorder;
    } else {
      return styles.grayBorder;
    }
  };

  const getInputState = () => {
    if (text.length > maxLength) {
      return styles.error;
    } else if (text.length > 0 && !isFocused) {
      return styles.entered;
    } else {
      return '';
    }
  };

  return (
    <div className={styles.inputWrapper}>
      <label htmlFor="text-input" className={styles.inputLabel}>
        {label}
      </label>
      <input
        id="text-input"
        className={`${styles.input} ${getBorderColor()} ${getInputState()}`}
        value={text}
        onChange={handleInputChange}
        onFocus={handleFocus}
        onBlur={handleBlur}
      />
      {showCharacterCount && (
        <div className={styles.commentsWrapper}>
          <div className={styles.errorWrap}>
            {text.length > maxLength && (
              <p className={styles.errorMessage}>{errorText}</p>
            )}
          </div>
          <p
            className={`${styles.counterMessage} ${
              text.length > maxLength ? styles.redText : ''
            }`}
          >
            {`${text.length}/${maxLength}`}
          </p>
        </div>
      )}
    </div>
  );
};

InputSm.propTypes = {
  label: PropTypes.string.isRequired,
  maxLength: PropTypes.number.isRequired,
  errorText: PropTypes.string,
  showCharacterCount: PropTypes.bool,
};

InputSm.defaultProps = {
  errorText: 'Текст перевищує вказану кількість символів',
  showCharacterCount: true,
};

export default InputSm;
