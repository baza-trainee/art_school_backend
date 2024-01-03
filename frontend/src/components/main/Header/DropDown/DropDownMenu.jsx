import { clsx } from 'clsx';
import styles from './DropDown.module.scss';
import { Link } from 'react-router-dom';
import { useMediaQuery } from 'react-responsive';
import { HashLink } from 'react-router-hash-link';

const DropDownMenu = ({
  departmemts,
  aboutSchool,
  toggleBurgerMenu,
  isOpen,
  currentId,
  setCurrentId,
  setIsOpen,
}) => {
  const isDesktop = useMediaQuery({ minWidth: 1280 });

  return (
    <>
      <HashLink
        className={clsx(styles.dropDown, !isDesktop && styles.dropDownMobile)}
        onClick={() => {
          setIsOpen(!isOpen);
          setCurrentId('departments');
        }}
        onMouseEnter={() => {
          setIsOpen(true);
          setCurrentId('departments');
        }}
        onMouseLeave={() => {
          setIsOpen(false);
          setCurrentId('');
        }}
        scroll={el => {
          if (isDesktop) {
            el.scrollIntoView({
              behavior: 'smooth',
              block: 'center',
            });
          }
        }}
        to="/#departmens"
      >
        <div className={styles.dropDownNameWrapper}>
          <span
            className={clsx(
              styles.dropDownName,
              isOpen && currentId === 'departments' ? styles.open : ''
            )}
          >
            {/* {type} */}
            Відділення
          </span>

          {isOpen && currentId === 'departments' ? (
            <span className={styles.dropDown_iconUp}></span>
          ) : (
            <span className={styles.dropDown_iconDown}></span>
          )}
        </div>

        {isOpen && currentId === 'departments' && (
          <ul
            className={clsx(
              styles.menu,
              isOpen && currentId === 'departments' ? styles.open : '',
              styles.departmentsMenu
            )}
          >
            {departmemts.map(({ name, to }) => (
              <li className={styles.menuItem} key={name}>
                <Link
                  className={clsx(styles.menulink, open ? styles.open : '')}
                  key={name}
                  to={to}
                  onClick={() => {
                    !isDesktop && toggleBurgerMenu();
                  }}
                >
                  {name}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </HashLink>

      <Link
        className={clsx(styles.dropDown, !isDesktop && styles.dropDownMobile)}
        to="/about_school"
        onMouseEnter={() => {
          setCurrentId('about_school');
          setIsOpen(true);
        }}
        onMouseLeave={() => {
          setIsOpen(false);
          setCurrentId('');
        }}
        onClick={() => {
          setIsOpen(!isOpen);
          setCurrentId('about_school');
        }}
      >
        <div className={styles.dropDownNameWrapper}>
          <span className={clsx(styles.dropDownName, open ? styles.open : '')}>
            {/* {type} */}
            Наша школа
          </span>

          {isOpen && currentId === 'about_school' ? (
            <span className={styles.dropDown_iconUp}></span>
          ) : (
            <span className={styles.dropDown_iconDown}></span>
          )}
        </div>

        {isOpen && currentId === 'about_school' && (
          <ul
            className={clsx(
              styles.menu,
              isOpen && currentId === 'about_school' ? styles.open : '',
              styles.aboutUsMenu
            )}
          >
            <li className={styles.menuItem} key={name}>
              <Link
                className={clsx(styles.menulink, open ? styles.open : '')}
                key={name}
                to="/about_school_history"
                onClick={() => {
                  !isDesktop && toggleBurgerMenu();
                }}
              >
                Історія Школи
              </Link>
            </li>
            {aboutSchool.map(({ name, to }) => (
              <li className={styles.menuItem} key={name}>
                <HashLink
                  className={clsx(styles.menulink, open ? styles.open : '')}
                  key={name}
                  to={to}
                  onClick={() => {
                    !isDesktop && toggleBurgerMenu();
                  }}
                  scroll={el => {
                    el.scrollIntoView({
                      behavior: 'smooth',
                      block: 'start',
                    });
                  }}
                >
                  {name}
                </HashLink>
              </li>
            ))}
          </ul>
        )}
      </Link>
    </>
  );
};

export default DropDownMenu;
