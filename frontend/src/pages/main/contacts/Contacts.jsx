import { Link } from 'react-router-dom';
import { Icon } from 'leaflet';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import s from './Contacts.module.scss';
import { useEffect } from 'react';

const Contacts = () => {
  const customIcon = new Icon({
    iconUrl: '/icons/location1.png',
    iconSize: [45, 42],
  } );
  
    useEffect(() => {
      window.scrollTo(0, 0);
    }, []);
  return (
      <div className={s.contacts}>
        <h2>Наші контакти</h2>
        <ul className="list">
          <li>вул. Бульварно-Кудрявська, 2.</li>
          <li>Пн-Пт 10:00-17:00</li>
          <li>
            <Link to="tel:+380442720030">044 272 00 30</Link>
          </li>
          <li>
            <Link to="mailto:Shkola_2@ukr.net">Shkola_2@ukr.net</Link>
          </li>
        </ul>
        <div className={s.mapContainer}>
          <MapContainer
            center={{ lat: 50.45449, lng: 30.50435 }}
            zoom={17}
            scrollWheelZoom={false}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Marker position={[50.45449, 30.50435]} icon={customIcon}>
              <Popup>
                <div className={s.popup}>
                  <h3>Наша адреса</h3>
                  <p>вул. Бульварно-Кудрявська, 2.</p>
                  <p>044 272 00 30</p>
                </div>
              </Popup>
            </Marker>
          </MapContainer>
        </div>
      </div>
  );
};

export default Contacts;
