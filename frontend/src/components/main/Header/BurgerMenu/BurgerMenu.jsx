import NavList from '../NavList/NavList';
import styles from './BurgerMenu.module.scss';
import CloseIcon from '@/components/Icons/CloseIcon';
import clsx from 'clsx';
import SocialList from '../SosialList/SocialList';
const BurgerMenu = ({ showBurgerMenu, setShowBurgerMenu }) => {
  // console.log('showBurgerMenu: ', showBurgerMenu);

  const toggleBurgerMenu = () => setShowBurgerMenu(!showBurgerMenu);
  return (
    <div
      className={clsx(
        styles.burgerMenuWrapper,
        showBurgerMenu ? '' : styles.hidden
      )}
    >
      <div className={styles.burgerMenuContent}>
        <NavList toggleBurgerMenu={toggleBurgerMenu} />
      </div>
      <button
        aria-label=" menu close button"
        tabIndex="0"
        type="button"
        className={styles.burgerMenuCloseButton}
        onClick={toggleBurgerMenu}
      >
        <CloseIcon />
      </button>
      <SocialList type="burgerMenuIcon" />
    </div>
  );
};

export default BurgerMenu;
