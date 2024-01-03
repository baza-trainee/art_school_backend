import { useLocation } from 'react-router-dom';
import s from './Spinner.module.scss';

const Spinner = () => {
  const { pathname } = useLocation();

  if (pathname.includes('admin')) {
    return <div className={s.adminSpinner}></div>;
  } else {
    return <div className={s.spinner}></div>;
  }
};

export default Spinner;
