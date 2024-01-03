import { Link } from 'react-router-dom';
import Department from './Department/Department';
import Container from '@/components/Container/Container';

import musicImg from '/departments/music.webp';
import artImg from '/departments/art.webp';
import choreografyImg from '/departments/horeografy.webp';
import theaterImg from '/departments/theater.webp';
import vocalImg from '/departments/vocal.webp';

import styles from './Departments.module.scss';

const Departments = () => {
  const musicDepartment = 'Музичне відділення';
  const artDepartment = 'Образотворче відділення';
  const choreografyDepartment = 'Хореографічне відділення';
  const theaterDepartment = 'Театральне відділення';
  const vocalDepartment = 'Вокально-хорове відділення';
  const preschoolPreparatoryDepartment = 'Дошкільне та підготовче відділення';

  return (
    <Container>
      <div id="departmens" className={styles.wrapper}>
        <p className={`${styles.title} sectionTitle`}>Відділення</p>
        <div className={styles.buttonContainer}>
          <Link to="/statement">
            <button className={styles.buttonStyle}>завантажити заяву</button>
          </Link>
        </div>
        <div className={styles.departmentsContainer}>
          <Department
            title={musicDepartment}
            link="/music_department"
            img={musicImg}
          />
          <Department
            title={vocalDepartment}
            link="/vocal_department"
            img={vocalImg}
          />
          <Department
            title={choreografyDepartment}
            link="/сhoreographic_department"
            img={choreografyImg}
          />
          <Department
            title={artDepartment}
            link="/fine_arts_department"
            img={artImg}
          />
          <Department
            title={theaterDepartment}
            link="/theater_department"
            img={theaterImg}
          />
          <Department
            title={preschoolPreparatoryDepartment}
            link="/preschool_department"
            img={theaterImg}
          />
        </div>
      </div>
    </Container>
  );
};

export default Departments;
