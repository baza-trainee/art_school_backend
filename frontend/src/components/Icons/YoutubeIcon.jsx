import clsx from 'clsx';
import styles from './Icons.module.scss';

const YoutubeIcon = ({ type }) => {
  // console.log(type);
  return (
    <svg
      className={clsx(
        styles.youtubeIcon,
        type === 'burgerMenuIcon' ? styles.burgerMenuIcon : ''
      )}
      xmlns="http://www.w3.org/2000/svg"
      width="40"
      height="32"
      viewBox="0 0 40 32"
      fill="none"
    >
      <path d="M2.66663 16.9427V15.056C2.66663 11.196 2.66663 9.26533 3.87329 8.02399C5.08129 6.78133 6.98263 6.72799 10.784 6.61999C12.584 6.56933 14.424 6.53333 16 6.53333C17.5746 6.53333 19.4146 6.56933 21.216 6.61999C25.0173 6.72799 26.9186 6.78133 28.1253 8.02399C29.3333 9.26533 29.3333 11.1973 29.3333 15.056V16.9427C29.3333 20.804 29.3333 22.7333 28.1266 23.976C26.9186 25.2173 25.0186 25.272 21.216 25.3787C19.416 25.4307 17.576 25.4667 16 25.4667C14.261 25.4614 12.5221 25.4321 10.784 25.3787C6.98263 25.272 5.08129 25.2187 3.87329 23.976C2.66663 22.7333 2.66663 20.8027 2.66663 16.944V16.9427Z" />
      <path
        className="path"
        d="M18.6661 16L13.9994 18.6667V13.3334L18.6661 16Z"
        fill={type === 'burgerMenuIcon' ? ' #fffcfc' : '#120000'}
        stroke={type === 'burgerMenuIcon' ? '# #fffcfc' : '#120000'}
        strokeWidth="1.25"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};

export default YoutubeIcon;
