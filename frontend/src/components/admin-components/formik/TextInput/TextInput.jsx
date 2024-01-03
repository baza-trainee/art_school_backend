import { useEffect } from 'react';
import { useFocused } from '@/store/focusStore';
import styles from './TextInput.module.scss';

const TextInput = ({
  id,
  field,
  text,
  label,
  form: { errors, handleBlur, touched, setFieldValue },
  maxLength,
  showCharacterCount,
  placeholder,
}) => {
  const name = field.name;
  const isFieldTouched = touched[field.name];
  const valueLength = field.value?.length;
  const { isFocused, setIsFocused } = useFocused();

  useEffect(() => {
    if (!text) return;
    setFieldValue(`${name}`, text);
  }, [text, setFieldValue, name]);

  const handleFocus = () => {
    setIsFocused(name);
  };

  const getBorderColor = () => {
    if (valueLength > maxLength) {
      return styles.redBorder;
    }
    if (errors?.[field.name]) {
      return styles.redBorder;
    }
    if (isFocused === name) {
      return styles.blueBorder;
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
      <input
        id={id}
        type="text"
        className={`${styles.input} ${getBorderColor()} ${getInputState()}`}
        onFocus={handleFocus}
        onBlur={handleBlur}
        onClick={() => setIsFocused(name)}
        placeholder={placeholder ? placeholder : ''}
        {...field}
      />

      <div className={styles.commentsWrapper}>
        <div className={styles.errorWrap}>
          {errors?.[field.name] && isFieldTouched && (
            <p className={styles.errorMessage}>{errors?.[field.name]}</p>
          )}
        </div>
        {showCharacterCount && (
          <p
            className={`${styles.counterMessage} ${
              valueLength > maxLength ? styles.redText : ''
            }`}
          >
            {`${valueLength}/${maxLength}`}
          </p>
        )}
      </div>
    </div>
  );
};

export default TextInput;
