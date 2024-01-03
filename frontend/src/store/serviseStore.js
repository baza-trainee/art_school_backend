import { create } from 'zustand';
import axios from '@/utils/axios';
import { isDataValid } from '@/utils/formDataValidation';

const useServicesStore = create((set, get) => ({
  departments: [],
  subDepartments: [],
  achievements: [],
  gallery: [],
  achievementsPositions: [],
  achievement: {},
  achievementPageCount: '',
  galleryPageCount: '',
  pageSize: 10,
  loading: false,
  //отримати всі основні відділення
  getMainDepartments: async () => {
    const response = await axios.get('/departments');
    try {
      set(() => {
        return {
          departments: response.data,
        };
      });
    } catch (error) {
      throw new Error(error);
    }
  },
  //отримати всі відділи відділень по id основних відділень
  getSubDepartments: async id => {
    const response = await axios.get(`/departments/${id}`);
    try {
      set(() => {
        return {
          subDepartments: response.data,
        };
      });
    } catch (error) {
      throw new Error(error);
    }
  },

  //всі досягнення
  getAllAchievements: async (url, page) => {
    const newUrl = url === 'gallery' ? 'gallery/photo' : url;
    const size = get().pageSize;
    try {
      set(() => {
        return {
          loading: 'loading',
        };
      });
      const response = await axios.get(`/${newUrl}?page=${page}&size=${size}`);
      if (url === 'gallery') {
        set(state => {
          return {
            ...state,
            gallery: page === 1 ? response.data.items : [...state.gallery, ...response.data.items],
            galleryPageCount: response.data.pages,
          };
        });
      } else {
        set(state => {
          return {
            ...state,
            achievements:page === 1? response.data.items: [...state.achievements, ...response.data.items],
            achievementPageCount: response.data.pages,
          };
        });
      }
      set(state => ({ ...state, loading: 'success'}));
    } catch (error) {
      set(state => ({ ...state, loading: 'error'}));
      throw new Error(error);
    }
  },
  //досягнення головної сторінки
  getMainAchievements: async url => {
    const newUrl = url === 'gallery' ? 'gallery/photo' : url;
    try {
      set(() => {
        return {
          loading: 'loading',
        };
      });
      const response = await axios.get(`/${newUrl}?is_pinned=true`);
      set(() => {
        if (url === 'gallery') {
          return {
            gallery: response.data.items,
          };
        } else {
          return {
            achievements: response.data.items,
          };
        }
      })
      set(state => ({ ...state, loading: 'success'}));
    } catch (error) {
      set(() => {
        if (url === 'gallery') {
          return {
            gallery: [],
          };
        } else {
          return {
            achievements: [],
          };
        }
      });
      set(state => ({ ...state, loading: 'error'}));
      throw new Error(error);
    }
  },
  // досягнення відділу по id
  getDepartmentAchievements: async (url, id) => {
    const newUrl = url === 'achievements' ? 'achievement' : url;
    try {
      set(() => {
        return {
          loading: 'loading',
        };
      });
      const response = await axios.get(
        `/departments/sub_department_${newUrl}/${id}`
      );
      set(() => {
        if (url === 'gallery') {
          return {
            gallery: response.data,
            loading: 'success',
          };
        } else {
          return {
            achievements: response.data,
            loading: 'success',
          };
        }
      });
    } catch (error) {
      set(() => {
        if (url === 'gallery') {
          return {
            gallery: [],
            loading: 'error',
          };
        } else {
          return {
            achievements: [],
            loading: 'error',
          };
        }
      });
      throw new Error(error);
    }
  },
  //конкретне досягнення по id
  getAchievemenById: async (url, id) => {
    const newUrl = url === 'gallery' ? 'gallery/photo' : url;
    try {
      const response = await axios.get(`/${newUrl}/${id}`);
      set(() => {
        return {
          achievement: response.data,
        };
      });
    } catch (error) {
      throw new Error(error);
    }
  },
  // додати досягнення
  addPost: async data => {
    if (isDataValid(data)) {
      try {
        const response = await axios.post('/news', data, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        return response;
      } catch (error) {
        throw new Error(error);
      }
    }
  },
  addAchievement: async (url, data) => {
    const newUrl = url === 'gallery' ? 'gallery/photo' : url;
    if (isDataValid(data)) {
      try {
        const queryParams = new URLSearchParams();
        if (data.get('pinned_position') !== '' && data.get('pinned_position') !== null) {
          queryParams.append('pinned_position', data.get('pinned_position'));
        }
        if (data.get('sub_department') !== '' && data.get('sub_department') !== null) {
          queryParams.append('sub_department', data.get('sub_department'));
        }
        if (data.get('description') !== '') {
          queryParams.append('description', data.get('description'));
        }
        const response = await axios.post(
          `/${newUrl}?${queryParams.toString()}`,
          data,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        );
        return response;
      } catch (error) {
        throw new Error(error);
      }
    }
  },
  //зміна досягнення
  editAchievement: async (url, id, data) => {
    const newUrl = url === 'gallery' ? 'gallery/photo' : url;
    try {
      if (isDataValid(data)) {
        const queryParams = new URLSearchParams();
        if (data.get('pinned_position') !== '' && data.get('pinned_position') !== null) {
          queryParams.append('pinned_position', data.get('pinned_position'));
        }
        if (data.get('sub_department') !== '' && data.get('sub_department') !== null) {
          queryParams.append('sub_department', data.get('sub_department'));
        }
        if (data.get('description') !== '') {
          queryParams.append('description', data.get('description'));
        }
        const response = await axios.put(
          `/${newUrl}/${id}?${queryParams.toString()}`,
          data,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        );
        return response;
      }
    } catch (error) {
      throw new Error(error);
    }
  },
  //видалення досягнення
  deleteAchievement: async (url, id) => {
    try {
      const response = await axios.delete(`/${url}/${id}`);
      if (url === 'gallery') {
        set(state => ({
          gallery: state.gallery.filter(item => item.id !== id),
        }));
      } else {
        set(state => ({
          achievements: state.achievements.filter(item => item.id !== id),
        }));
      }
      return response;
    } catch (error) {
      throw new Error(error);
    }
  },
  //Позиції досягнень головної сторінки
  getAchievementsPositions: async url => {
    try {
      const response = await axios.get(`/${url}/positions`);
      set(() => {
        return {
          achievementsPositions: response.data,
        };
      });
    } catch (error) {
      throw new Error(error);
    }
  },

  getAdministrationData: async () => {
    try {
      const response = await axios.get(`/school_administration`);
      set(() => {
        return {
          members: response.data,
        };
      });
    } catch (error) {
      throw new Error(error);
    }
  },
}));

export default useServicesStore;
