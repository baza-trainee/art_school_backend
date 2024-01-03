import { useState } from 'react';

import { Link } from 'react-router-dom';

import { aboutUs, departmemts } from '@/constants/dropDownItems.js';
import { navItems } from '@/constants/navList.js';

import DropDownMenu from '../DropDown/DropDownMenu';

import styles from './NavList.module.scss';
import clsx from 'clsx';
import { useMediaQuery } from 'react-responsive';

const NavList = ({ toggleBurgerMenu }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentId, setCurrentId] = useState('');

  const isDesktop = useMediaQuery({ minWidth: 1240 });

  return (
    <nav className={styles.nav}>
      <div className={styles.navSelectMenu}>
        <DropDownMenu
          departmemts={departmemts}
          aboutSchool={aboutUs}
          isOpen={isOpen}
          currentId={currentId}
          setIsOpen={setIsOpen}
          setCurrentId={setCurrentId}
          toggleBurgerMenu={toggleBurgerMenu}
        />
      </div>

      <ul
        className={clsx(styles.navList, !isDesktop ? styles.navListMobile : '')}
      >
        {navItems.map(({ name, to }) => (
          <li className={styles.navList_item} key={name}>
            <Link
              className={styles.navList_link}
              key={name}
              to={to}
              onClick={toggleBurgerMenu}
            >
              {name}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default NavList;
