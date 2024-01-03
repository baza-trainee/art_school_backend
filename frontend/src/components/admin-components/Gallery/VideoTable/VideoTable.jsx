import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import useServicesStore from '@/store/serviseStore';
import { useModal } from '@/store/modalStore';
import { useConfirmDelete } from '@/store/confirmDelete';
import ConfirmDeleteModal from '@/components/admin-components/modals/ConfirmDeleteModal/ConfirmDeleteModal';
import sprite from '@/assets/icons/sprite-admin.svg';
import s from './VideoTable.module.scss';

const VideoTable = ({ url, videos }) => {
  const navigate = useNavigate();
  const { deleteAchievement } = useServicesStore();
  const { isDeleteConfirm } = useConfirmDelete();
  const { isModalOpen, openModal, closeModal } = useModal();
  const [currentId, setCurrentId] = useState('');
  const replaceUrl = videoUrl => {
    return videoUrl.replace('watch?v=', 'embed/');
  };

  useEffect(() => {}, [videos, currentId]);
  const removePost = async () => {
    if (isDeleteConfirm) {
      try {
        console.log(currentId);
        await deleteAchievement(url, currentId);
        navigate(`/admin/${url}`);
      } catch (error) {
        console.log(error);
      }
    } else {
      closeModal();
    }
  };

  return (
    <div className={s.galleryTable}>
      <div className={s.videos}>
        {videos?.length > 0 &&
          videos.map((item, i) => (
            <div className={s.photoContainer} key={i}>
              <div className={s.photo}>
                <iframe
                  src={replaceUrl(item.media)}
                  title={`Video ${i + 1}`}
                  width="150"
                  height="95"
                />
              </div>
              <div className={s.action}>
                <Link to={`edit/${item.id}`}>
                  <button className={s.edit}>
                  <svg>
                      <use
                        href={`${sprite}#icon-edit`}
                      />
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
                  <svg
                  onClick={() => setCurrentId(item.id)}
                >
                  <use href={`${sprite}#icon-trash`}/>
                </svg>
                </button>
              </div>
            </div>
          ))}
        {isModalOpen && <ConfirmDeleteModal handleDelete={removePost} />}
      </div>
    </div>
  );
};

export default VideoTable;
