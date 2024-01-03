import { Link } from 'react-router-dom';
import Logo from '@/components/Logo/Logo';
import LocationIcon from '@/components/Icons/LocationIcon';
import PhoneIcon from '@/components/Icons/PhoneIcon';
import EmailIcon from '@/components/Icons/EmailIcon';
import FacebookIcon from '@/components/Icons/FacebookIcon';
import YoutubeIcon from '@/components/Icons/YoutubeIcon';
import DownloadButton from '@/components/ui/Buttons/NavLinkButton';
import styles from './Footer.module.scss';
import ClockIcon from '@/components/Icons/ClockIcon';

const Footer = () => {
  return (
    <div className={styles.footer}>
      <div className={styles.footerWrap}>
        <div className={styles.footerContentWrap}>
          <div className={styles.footerContent}>
            <div className={styles.footerLogo}>
              <Logo />
            </div>
            <ul className={styles.social}>
              <li>
                <a
                  className={styles.socialLink}
                  href="https://www.facebook.com/KyivArtsSchool/"
                  target="_blank"
                  rel="noreferrer"
                >
                  <FacebookIcon width="32" height="32" />
                </a>
              </li>
              <li>
                <a
                  className={styles.socialLink}
                  href="https://www.youtube.com/c/ArtSchoolVerykivskogo"
                  target="_blank"
                  rel="noreferrer"
                >
                  <YoutubeIcon width="40" height="32" />
                </a>
              </li>
            </ul>

            <div className={styles.footerButton}>
              <Link to="/statement">
                <DownloadButton link="#" text="Завантажити заяву" />
              </Link>
            </div>
          </div>
          <div className={styles.footerLinksSectionWrap}>
            <div className={styles.footerLinksSection}>
              <div className={styles.footerLinksColumn}>
                <Link to="/">Головна</Link>
                <Link to="/about">Наша школа</Link>
                <Link to="/events">Наші події</Link>
                <Link to="/schedule">Афіша</Link>
                <Link to="/gallery">Галерея</Link>
                <Link to="/partners">Співпраця</Link>
              </div>
              <div className={styles.footerLinksColumnDepartment}>
                <Link to="/music-department">Музичне відділення</Link>
                <Link to="/vocal-choral-department">
                  Вокально-хорове відділення
                </Link>
                <Link to="/choreographic-department">
                  Хореографічне відділення
                </Link>
                <Link to="/visual-arts-department">
                  Образотворче відділення
                </Link>
                <Link to="/theater-department">Театральне відділення</Link>
                <Link to="#">Дошкільне та підготовче відділення</Link>
              </div>
            </div>
            <div className={styles.contactsListWrap}>
              <ul className={styles.contactsList}>
                <li className={styles.contactsListItem}>
                  <LocationIcon />
                  <a
                    href="https://maps.app.goo.gl/jv2N9vFL6ZiJhosc6"
                    target="_blank"
                    rel="noopener noreferrer nofollow"
                  >
                    вул. Бульварно-Кудрявська, 2.
                  </a>
                </li>
                <li className={styles.contactsListItem}>
                  <ClockIcon />
                  <div className={styles.contactsListItem_PhoneWrapper}>
                    Пн-Пт 10:00-17:00
                  </div>
                </li>
                <li className={styles.contactsListItem}>
                  <PhoneIcon />
                  <div className={styles.contactsListItem_PhoneWrapper}>
                    <a href="tel:+380442720030">044 272 00 30</a>
                  </div>
                </li>
                <li className={styles.contactsListItem}>
                  <EmailIcon />
                  <a href="mailto:Shkola_2@ukr.net">Shkola_2@ukr.net</a>
                </li>
              </ul>
              <div className={styles.footerButtonAdaptive}>
                <DownloadButton link="#" text="Завантажити заяву" />
              </div>
            </div>
          </div>
        </div>

        <ul className={styles.socialAdaptive}>
          <li>
            <a
              className={styles.socialLink}
              href="https://www.facebook.com/KyivArtsSchool/"
              target="_blank"
              rel="noreferrer"
            >
              <FacebookIcon width="32" height="32" />
            </a>
          </li>
          <li>
            <a
              className={styles.socialLink}
              href="https://www.youtube.com/c/ArtSchoolVerykivskogo"
              target="_blank"
              rel="noreferrer"
            >
              <YoutubeIcon width="40" height="32" />
            </a>
          </li>
        </ul>

        <div className={styles.footerLinksRulesWrap}>
          <div className={styles.footerSecurity}>
            © Розробка{' '}
            <a
              href="https://baza-trainee.tech/"
              rel="noreferrer"
              target="_blank"
            >
              Baza Trainee Ukraine,{' '}
            </a>
            2023
          </div>
          <div className={styles.footerLinksRules}>
            <a href="#" target="_blank">
              Офіційна інформація
            </a>
            <a href="#" target="_blank">
              Політика конфіденційності
            </a>
            <a href="#" target="_blank">
              Правила користування сайтом
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Footer;
