import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';

import BasicContainerLogin from '../BasicContainerLogin/BasicContainerLogin';
import styles from './LoginLayout.module.scss';

export const LoginLayout = () => {
  return (
    <div className={styles.backgroundContainer}>
      <BasicContainerLogin>
        <Suspense fallback={<div>Loading...</div>}>
          <Outlet />
        </Suspense>
      </BasicContainerLogin>
    </div>
  );
};

export default LoginLayout;
