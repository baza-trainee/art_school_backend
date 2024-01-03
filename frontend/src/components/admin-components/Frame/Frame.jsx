import React, { useState } from 'react';
import InputSm from '../formElement/Inputs/InputSm';
import TextArea from '../formElement/TextArea/TextArea';
import FileInput from '../formElement/FileInput/FileInput';
import ButtonSubmit from '../Buttons/SubmitButton/ButtonSubmit';
import styles from './Frame.module.scss';

const Table = () => {
  const [inputText, setInputText] = useState('');
  const [textareaText, setTextareaText] = useState('');

  return (
    <div className={styles.tableWrap}>
      <div className={styles.table}>
        <InputSm
          label="Заголовок*"
          maxLength={120}
          errorMessage={`Текст перевищує 120 символів`}
          showCharacterCount={true}
          text={inputText}
          setText={setInputText}
        />
        
        <div className={styles.tableEdd}>
          <TextArea
            label="Текст*"
            maxLength={200}
            errorMessage="Текст перевищує 200 символів"
            text={textareaText}
            setText={setTextareaText}
          />
          <FileInput />
        </div>
      </div>
      <ButtonSubmit
        nameButton="Зберегти зміни"
        isActive={true}
        isRight={true}
      />
      
    </div>
  );
};

export default Table;

