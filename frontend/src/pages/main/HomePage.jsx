import { useEffect } from 'react';
import Hero from '@/components/main/Hero/Hero';
import Gallery from '@/components/main/Gallery/Gallery';
import Achievements from '@/components/main/Achievements/Achievements';
import History from '@/components/main/History/History';
import Departments from '@/components/main/Departments/Departments';
import Map from '@/components/main/Map/Map';
import News from '@/components/main/News/News';

const HomePage = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <>
      <Hero />
      <History />
      <Departments />
      <News />
      <Gallery />
      <Achievements
        title={'Наші досягнення'}
        url={'achievements'}
        showSelect={false}
      />
      <Map />
    </>
  );
};

export default HomePage;
