import React from 'react';
import { Link } from 'react-router-dom';
import styles from './LogoAdmin.module.scss';
import sprite from '../../../../assets/icons/sprite-admin.svg';

const LogoAdmin = () => {
   return (
      <Link
         aria-label="company logo navigation to home page"
         to="/"
         className={styles.logoWrapper}
      >
         <svg className={styles.logoIcon} width="42" height="42">
            <use href={`${sprite}#icon-logo`} />
         </svg>
         
         <div className={styles.logoText}>
            <p>Київська дитяча школа мистецтв №2</p>
            <span> ім. М. I. Вериківського</span>
         </div>
      </Link>
   );
};

export default LogoAdmin;
