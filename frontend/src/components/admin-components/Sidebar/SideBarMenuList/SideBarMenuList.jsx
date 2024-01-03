import { useLocation } from 'react-router-dom';
import { sideBarList } from './sideBarList';
import SideBarMenuItems from '../SideBarMenuItems/SideBarMenuItems';
import styles from './SideBarMenuList.module.scss';

const SideBarMenuList = () => {
  const { pathname } = useLocation();
  const pathNameArray = pathname.split('/');

  return (
    <div className={styles.sidebarMenuList}>
      {sideBarList.map((item, index) => (
        <SideBarMenuItems
          key={index}
          title={item.title}
          link={item.link}
          isFilled={item.isFilled}
          iconClass={item.iconClass}
          isLinkActive={pathNameArray.includes(item.link)}
        />
      ))}
    </div>
  );
};

export default SideBarMenuList;
