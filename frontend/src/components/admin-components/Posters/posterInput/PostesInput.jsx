import TextArea from '@/components/admin-components/formElement/TextArea/TextArea';
import FileInput from '@/components/admin-components/formElement/FileInput/FileInput';
import styles from './PosterInput.module.scss';

const PostersInput = ({ label }) => {
  return (
    <div className={styles.layout}>
      <TextArea
        label="Заголовок"
        maxLength={120}
        errorMessage="Текст перевищує 2000 символів"
      />

      <FileInput label={label} />
    </div>
  );
};
export default PostersInput;
