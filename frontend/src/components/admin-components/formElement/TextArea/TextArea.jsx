import { useState } from 'react';
import PropTypes from 'prop-types';
import styles from './TextArea.module.scss';

const TextArea = ({ label, maxLength, errorMessage, text = '', setText = () => {} }) => {
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
    <div className={styles.textAreaWrapper}>
      <label htmlFor="text-area" className={styles.inputLabel}>
        {label}
      </label>
      <textarea
        id="text-area"
        className={`${styles.textArea} ${getBorderColor()} ${getInputState()}`}
        value={text}
        onChange={handleInputChange}
        onFocus={handleFocus}
        onBlur={handleBlur}
      />
      <div className={styles.commentsWrapper}>
        <div className={styles.errorWrap}>
          {text.length > maxLength && (
            <p className={styles.errorMessage}>{errorMessage}</p>
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
    </div>
  );
};

TextArea.propTypes = {
  label: PropTypes.string.isRequired,
  maxLength: PropTypes.number.isRequired,
  errorMessage: PropTypes.string,
};

TextArea.defaultProps = {
  label: 'Текст*',
  maxLength: 2000,
  errorMessage: `Текст перевищує вказану кількість символів`,
};

export default TextArea;
