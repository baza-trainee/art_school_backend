import clsx from 'clsx';
import styles from './Icons.module.scss';

const FacebookIcon = ({ type }) => {
  return (
    <svg
      className={clsx(
        styles.facebookIcon,
        type === 'burgerMenuIcon' ? styles.burgerMenuIcon : ''
      )}
      xmlns="http://www.w3.org/2000/svg"
      width="32"
      height="32"
      viewBox="0 0 32 32"
      fill="none"
    >
      <rect x="5" y="5" width="22" height="22" rx="6" />
      <path
        d="M18.5008 16.6717L18.7993 14.7267H16.933V13.4645C16.933 12.9324 17.1937 12.4138 18.0295 12.4138H18.878V10.7578C18.878 10.7578 18.108 10.6264 17.3719 10.6264C15.835 10.6264 14.8304 11.558 14.8304 13.2443V14.7267H13.1219V16.6717H14.8304V21.3736H16.933V16.6717H18.5008Z"
        fill={type === 'burgerMenuIcon' ? ' #fffcfc' : '#120000'}
      />
    </svg>
  );
};
export default FacebookIcon;
