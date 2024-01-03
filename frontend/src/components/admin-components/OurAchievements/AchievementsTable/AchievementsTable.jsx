import { useState, useEffect, useRef } from 'react'; //, useRef
import useServicesStore from '@/store/serviseStore';
import { useModal } from '@/store/modalStore';
import { useConfirmDelete } from '@/store/confirmDelete';
import SpinnerAdmin from '@/components/admin-components/SpinnerAdmin/SpinnerAdmin';
import PlaceholderAdmin from '../../PlaceholderAdmin/PlaceholderAdmin';
import ConfirmDeleteModal from '@/components/admin-components/modals/ConfirmDeleteModal/ConfirmDeleteModal';
import AchievementsTableRow from './AchievementsTableRow';
import s from './AchievementsTable.module.scss';

const AchievementsTable = ({ typeOfAchievements, url, departmentId}) => {
  const { deleteAchievement, getAllAchievements, getMainAchievements, getDepartmentAchievements  } = useServicesStore();
  const achievements = useServicesStore(state => state.achievements);
  const pageCount = useServicesStore(state => state.achievementPageCount);
  const loading = useServicesStore(state => state.loading);
  const { isDeleteConfirm } = useConfirmDelete();
  const { isModalOpen, openModal, closeModal } = useModal();
  const [currentId, setCurrentId] = useState('');
  const [page, setPage] = useState(1);
  const triggerRef = useRef(null);

  const removePost = async () => {
    if (isDeleteConfirm) {
      try {
        await deleteAchievement(url, currentId);
        setPage(1);
      } catch (error) {
        console.log(error);
      }
    } else {
      closeModal();
    }
  };

  const fetchData = async () => {
    try {
      if(typeOfAchievements === 'allAchievements'){
        await getAllAchievements(url, page);
      }else if (typeOfAchievements === 'mainAchievements') {
        await getMainAchievements(url);
        setPage(1);
      } else if (typeOfAchievements === 'departmentAchievements') {
        await getDepartmentAchievements(url, departmentId);
        setPage(1);
      }
    } catch (error) {
      console.log(error);
      setPage(1);
    }
  };

  // Використовуємо IntersectionObserver для визначення, коли елемент потрапив у зону видимості
  useEffect(() => {
    if(typeOfAchievements === 'allAchievements'){
    const observer = new IntersectionObserver(entries => {
      const isIntersecting = entries[0]?.isIntersecting;
      const canLoadMore = loading === 'success' && page < pageCount;
      if (isIntersecting && canLoadMore) {
        setPage(prevPage => prevPage + 1);
      }
    }, {});
    const triggerElement = triggerRef.current;
    if (triggerElement) {
      observer.observe(triggerElement);
    }
    return () => {
      if (triggerElement) {
        observer.unobserve(triggerElement);
      }
    };
  }
    //eslint-disable-next-line
  }, [loading]);

  useEffect(() => {
    fetchData()
    //eslint-disable-next-line
  }, [page,typeOfAchievements, departmentId]);

  return (
    <div className={s.table}>
      <div className={`${s.row} ${s.thead}`}>
        {typeOfAchievements === 'mainAchievements' && (
          <div className={s.num}>Слайди</div>
        )}
        <div className={s.description}>Опис</div>
        <div className={s.photo}>Фото</div>
        <div className={s.action}>Дія</div>
      </div>
      <div className={s.tbody}>
        {Array.isArray(achievements) &&
          achievements.length > 0 &&
          achievements.map((item, index) => (
            <AchievementsTableRow
              typeOfAchievements={typeOfAchievements}
              setCurrentId={setCurrentId}
              openModal={openModal}
              item={item}
              index={index}
              key={index}
            />
          ))}
        {loading === 'loading' && <SpinnerAdmin />}
        {loading === 'error' && <PlaceholderAdmin />}
        <div className={s.trigger} ref={triggerRef}></div>
      </div>
      {isModalOpen && <ConfirmDeleteModal handleDelete={removePost} />}
    </div>
  );
};

export default AchievementsTable;
