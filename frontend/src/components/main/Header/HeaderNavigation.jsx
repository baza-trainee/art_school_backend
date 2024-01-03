import { useEffect, useState } from 'react';
import { clsx } from 'clsx';

import Logo from '../../Logo/Logo';
import NavList from './NavList/NavList';
import BurgerMenu from './BurgerMenu/BurgerMenu';
import BurgerIcon from '@/components/Icons/BurgerIcon';

import styles from './Header.module.scss';

const HeaderNavigation = ({ windowWidth }) => {
  const [showBurgerMenu, setShowBurgerMenu] = useState(false);
  const [show, setShow] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    const controlNavbar = () => {
      if (typeof window !== 'undefined') {
        if (window.scrollY > lastScrollY) {
          setShow(false); //  scroll down  hide header contacts l
        } else {
          setShow(true); // srroll up,  show header contacts again
        }
        setLastScrollY(window.scrollY); // scroll number
      }
    };

    if (typeof window !== 'undefined') {
      window.addEventListener('scroll', controlNavbar);
      return () => {
        window.removeEventListener('scroll', controlNavbar);
      };
    }
  }, [lastScrollY]);

  const handelClickBurgerButton = () => setShowBurgerMenu(!showBurgerMenu);

  useEffect(() => {
    const closeOnESC = event => {
      // console.log('event.code : ', event.code);
      if (event.code === 'Escape') {
        setShowBurgerMenu(false);
      }
    };
    window.addEventListener('keydown', closeOnESC);
    return () => {
      window.removeEventListener('keydown', closeOnESC);
    };
  }, [showBurgerMenu]);

  return (
    <div
      className={clsx(
        styles.headerNavigationWrapper,
        show ? '' : styles.hidden
      )}
    >
      <Logo className="header_logo" />
      {windowWidth >= 1280 ? (
        <NavList />
      ) : (
        <button
          aria-label="navigation menu"
          tabIndex="0"
          className={styles.burgerButton}
          type="button"
          onClick={handelClickBurgerButton}
        >
          <BurgerIcon />
        </button>
      )}

      <BurgerMenu
        showBurgerMenu={showBurgerMenu}
        setShowBurgerMenu={setShowBurgerMenu}
      />
    </div>
  );
};

export default HeaderNavigation;
