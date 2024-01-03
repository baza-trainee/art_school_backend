import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import useServicesStore from '@/store/serviseStore';
import SpinnerAdmin from '@/components/admin-components/SpinnerAdmin/SpinnerAdmin';
import PlaceholderAdmin from '../../PlaceholderAdmin/PlaceholderAdmin';
import { useModal } from '@/store/modalStore';
import { useConfirmDelete } from '@/store/confirmDelete';
import ConfirmDeleteModal from '@/components/admin-components/modals/ConfirmDeleteModal/ConfirmDeleteModal';
import sprite from '@/assets/icons/sprite-admin.svg';
import s from './GalleryTable.module.scss';

const GalleryTable = ({ typeOfAchievements, url, departmentId }) => {
  const {
    deleteAchievement,
    getAllAchievements,
    getMainAchievements,
    getDepartmentAchievements,
  } = useServicesStore();
  const gallery = useServicesStore(state => state.gallery);
  const pageCount = useServicesStore(state => state.galleryPageCount);
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
      if (typeOfAchievements === 'allAchievements') {
        await getAllAchievements(url, page);
      } else if (typeOfAchievements === 'mainAchievements') {
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
    if (typeOfAchievements === 'allAchievements') {
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
    fetchData();
    //eslint-disable-next-line
  }, [page, typeOfAchievements]);

  return (
    <div className={s.galleryTable}>
      <div className={s.gallary}>
        {Array.isArray(gallery) &&
          gallery?.length > 0 &&
          gallery.map((item, i) => (
            <div className={s.photoContainer} key={i}>
              <div className={s.photo}>
                <div>
                  <img src={item.media} alt="Фото" />
                </div>
              </div>
              <div className={s.action}>
                {typeOfAchievements === 'mainAchievements' && (
                  <div className={s.count}>{item.pinned_position}</div>
                )}
                <Link to={`edit/${item.id}`}>
                  <button className={s.edit}>
                    <svg>
                      <use href={`${sprite}#icon-edit`} />
                    </svg>
                  </button>
                </Link>
                <button
                  className={s.delete}
                  onClick={() => {
                    setCurrentId(item.id);
                    openModal();
                  }}
                >
                  <svg>
                    <use href={`${sprite}#icon-trash`} />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        {loading === 'loading' && <SpinnerAdmin />}
        <div className={s.trigger} ref={triggerRef}></div>
        {isModalOpen && <ConfirmDeleteModal handleDelete={removePost} />}
      </div>
      {loading === 'error' && <PlaceholderAdmin />}
    </div>
  );
};

export default GalleryTable;
