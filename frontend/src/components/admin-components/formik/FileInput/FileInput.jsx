import { useState, useEffect } from 'react';
import Dropzone from 'react-dropzone';
import { AiOutlinePlus } from 'react-icons/ai';
import styles from './FileInput.module.scss';

const FileInput = ({
  label,
  field,
  photo,
  form: { errors, setFieldValue },
  ...props
}) => {
  const name = field.name;
  const [imagePreview, setImagePreview] = useState('');
  const fieldValue = field.value;

  useEffect(() => {
    if (!photo) return;
    setFieldValue(`${name}`, [new File([], photo, { type: 'for-url' })]);
  }, [photo, setFieldValue, name]);

  useEffect(() => {
    setImagePreview(fieldValue?.[0]?.name);
  }, [fieldValue]);

  const setFileToBase64 = file => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
  };

    const onDrop = async files => {
      setFieldValue('image', files);
      const file = files[0];
      setFileToBase64(file);
    };

  return (
    <div className={styles.wrapper}>
      <label htmlFor="dropzone" className={styles.inputLabel}>
        {label}
      </label>
      <Dropzone
        onDrop={onDrop}
        multiple={false}
        maxSize={8000000000}
        id="dropzone"
        {...field}
        {...props}
      >
        {({ getRootProps, getInputProps }) => (
          <section className={styles.section}>
            <div className={styles.dropzone} {...getRootProps()}>
              <input {...getInputProps()} />
              {imagePreview ? (
                <div className={styles.imagePreview}>
                  <img src={imagePreview} />
                </div>
              ) : null}
              {!imagePreview && (
                <div className={styles.innerWrapper}>
                  <AiOutlinePlus className={styles.icon} />
                  <p>Перетягніть або натисніть тут, щоб завантажити файл</p>
                </div>
              )}
            </div>
          </section>
        )}
      </Dropzone>
      <div className={styles.errorWrap}>
        {errors?.[field.name] && (
          <p className={styles.errorMessage}>{errors?.[field.name]}</p>
        )}
      </div>
    </div>
  );
};

export default FileInput;

/*
import { useState, useEffect } from 'react';
import Dropzone from 'react-dropzone';
import { AiOutlinePlus } from 'react-icons/ai';
import styles from './FileInput.module.scss';

const FileInput = ({
  label,
  field,
  photo,
  form: { errors, setFieldValue },
  ...props
}) => {
  const name = field.name;
  const [imagePreview, setImagePreview] = useState('');
 // const fieldValue = field.value;

  useEffect(() => {
    if (!photo) return;
    setFieldValue(`${name}`, [new File([], photo, { type: 'for-url' })]);
  }, [photo, setFieldValue, name]);
  /*
  useEffect(() => {
    console.log(fieldValue);
    setImagePreview((fieldValue && fieldValue.length > 0) ? fieldValue[0].name : '');
  }, [fieldValue]);
*/
/*
  const setFileToBase64 = file => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
  };

  const onDrop = async files => {
    setFieldValue('image', files);
    const file = files[0];
    setFileToBase64(file);
  };

  return (
    <div className={styles.wrapper}>
      <label htmlFor="dropzone" className={styles.inputLabel}>
        {label}
      </label>
      <Dropzone
        onDrop={onDrop}
        multiple={false}
        maxSize={8000000000}
        id="dropzone"
        {...field}
        {...props}
      >
        {({ getRootProps, getInputProps }) => (
          <section>
            <div className={styles.dropzone} {...getRootProps()}>
              <input {...getInputProps()} />
              {imagePreview ? (
                <div className={styles.imagePreview}>
                  <img src={imagePreview} />
                </div>
              ) : null}
              {!imagePreview && (
                <div className={styles.innerWrapper}>
                  <AiOutlinePlus className={styles.icon} />
                  <p>Перетягніть або натисніть тут, щоб завантажити файл</p>
                </div>
              )}
            </div>
          </section>
        )}
      </Dropzone>
      <div className={styles.errorWrap}>
        {errors?.[field.name] && (
          <p className={styles.errorMessage}>{errors?.[field.name]}</p>
        )}
      </div>
    </div>
  );
};

export default FileInput;
*/