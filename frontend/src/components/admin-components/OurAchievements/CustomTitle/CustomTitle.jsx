import s from './CustomTitle.module.scss';

const CustomTitle = ({ title, width }) => {

  return (
    <div 
      className={`${s.title} ${width === 'fixed' ? s.fixed : ''}`}>
      {title}
    </div>
  );
};

export default CustomTitle;
