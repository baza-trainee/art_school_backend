import { useAuthorized } from '@/store/IsAuthorizedStore';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children, redirectTo = '/login' }) => {
  const isAuthorized = useAuthorized(state => state.isAuthorized);
  return isAuthorized ? <>{children}</> : <Navigate to={redirectTo} replace />;
};

export default PrivateRoute;
