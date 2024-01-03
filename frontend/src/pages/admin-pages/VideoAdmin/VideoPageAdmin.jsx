import { useState, useEffect } from 'react';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import useVideoStore from '@/store/videoStore';
import SpinnerAdmin from '@/components/admin-components/SpinnerAdmin/SpinnerAdmin';
import PlaceholderAdmin from '@/components/admin-components/PlaceholderAdmin/PlaceholderAdmin';
import VideoTable from '@/components/admin-components/Gallery/VideoTable/VideoTable';
import s from './VideoPage.module.scss';

const breadcrumbs = ['Відеогалерея'];

const VideoPageAdmin = () => {
  const { getAllVideo } = useVideoStore();
  const videos = useVideoStore(state => state.videos);
  const [loadingState, setLoadingState] = useState('loading');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoadingState('loading');
        await getAllVideo();
        setLoadingState('success');
      } catch (error) {
        console.log(error);
        setLoadingState('error');
      }
    };
    fetchData();
  }, [getAllVideo]);

  return (
    <div className={s.container}>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title="Відеогалерея"
        showBackButton={false}
        showActionButton={true}
        actionButtonLink="/admin/video/add"
        isActionButtonDisabled={false}
        actionButtonLabel="Додати відео"
      />
      {loadingState === 'success' && videos?.length > 0 && (
        <VideoTable videos={videos} url="video" />
      )}
      {loadingState === 'loading' && (
        <div className={s.errorData}>
          <SpinnerAdmin />
        </div>
      )}
      {loadingState === 'error' && <PlaceholderAdmin />}
    </div>
  );
};

export default VideoPageAdmin;
