import { Link } from "react-router-dom";
import styles from "./NotFoundAdmin.module.scss";

const NotFoundAdmin = () => {
   return (
      <div className={styles.adminWrapperError}>
         <div className={styles.adminErrorContent}>
            <h1 className={styles.adminErrorTitle}>404</h1>
            <h3 className={styles.adminErrorTextWarning}>На жаль, сторінку не знайдено</h3>
            <p className={styles.adminErrorText}>
               Сторінка, яку ви намагаєтесь знайти не існує, або була видалена
            </p>
         </div>
         <Link to={"/admin"} className={styles.adminErrorBtn}>
            На головну
         </Link>
      </div>
   );
};

export default NotFoundAdmin;

