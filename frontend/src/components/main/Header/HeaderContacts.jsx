import { useEffect, useState } from 'react';
import { clsx } from 'clsx';

import LocationIcon from '@/components/Icons/LocationIcon';
import PhoneIcon from '@/components/Icons/PhoneIcon';
import EmailIcon from '@/components/Icons/EmailIcon';
import SocialList from './SosialList/SocialList';

import styles from './Header.module.scss';

const HeaderContacts = () => {
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
  return (
    <div className={clsx(styles.contactsWrapper, show ? '' : styles.hidden)}>
      <ul className={styles.contactsList}>
        <li className={styles.contactsListItem}>
          <a
            className={styles.contactsListLink}
            href="https://maps.app.goo.gl/jv2N9vFL6ZiJhosc6"
            target="_blank"
            rel="noopener noreferrer nofollow"
          >
            <LocationIcon />
            вул. Бульварно-Кудрявська, 2.
          </a>
        </li>
        <li className={styles.contactsListItem}>
          <PhoneIcon />

          <div className={styles.contactsListItem_PhoneWrapper}>
            <a className={styles.contactsListLink} href="tel:+380442720030">
              044 272 00 30
            </a>
          </div>
        </li>
        <li className={styles.contactsListItem}>
          <a className={styles.contactsListLink} href="mailto:Shkola_2@ukr.net">
            <EmailIcon /> Shkola_2@ukr.net
          </a>
        </li>
      </ul>
      <SocialList type="headerIcon " />
    </div>
  );
};

export default HeaderContacts;
