import { Outlet } from 'react-router-dom';
import Header from '@/components/main/Header/Header';
import Footer from '@/components/main/Footer/Footer';

const Layout = () => {
  return (
    <>
      <Header />
      <main>
        <Outlet />
      </main>
      <Footer />
    </>
  );
};
export default Layout;
