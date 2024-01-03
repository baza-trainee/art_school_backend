import { create } from 'zustand';
import axios from '@/utils/axios';

const useDepartmentsStore = create((set, get) => ({
  loading: false,
  error: {},
  departments: [],
  department: [],
  sub_department: {},

  getDepartments: async () => {
    try {
      set(() => {
        return {
          loading: true,
        };
      });
      const response = await axios.get(`/departments`);
      set(() => {
        return {
          departments: response.data,
        };
      });
      set(() => {
        return {
          loading: false,
        };
      });
    } catch (error) {
      set(() => {
        return {
          error: error,
        };
      });
      throw new Error(error);
    }
  },

  getOneDepartment: async id => {
    try {
      const response = await axios.get(`/departments/${id}`);
      set(() => {
        return {
          department: response.data,
        };
      });
    } catch (error) {
      throw new Error(error);
    }
  },

  getOneSubDepartment: async id => {
    try {
      set(() => {
        return {
          loading: true,
        };
      });
      const response = await axios.get(`/departments/sub_department/${id}`);
      set(() => {
        return {
          sub_department: response.data,
        };
      });
      set(() => {
        return {
          loading: false,
        };
      });
    } catch (error) {
      throw new Error(error);
    }
  },

  addDepartment: async data => {
    try {
      set(() => {
        return {
          loading: true,
        };
      });
      if (!Object.values(data).includes(undefined)) {
        const body = JSON.stringify(data);
        const response = await axios.post('/departments/sub_department', body, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        set(() => {
          return {
            loading: false,
          };
        });
        return response;
      }
    } catch (error) {
      throw new Error(error);
    }
  },

  editDepartment: async (id, data) => {
    try {
      set(() => {
        return {
          loading: true,
        };
      });
      if (!Object.values(data).includes(undefined)) {
        const body = JSON.stringify(data);
        const response = await axios.patch(
          `/departments/sub_department/${id}`,
          body,
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
        set(() => {
          return {
            loading: false,
          };
        });
        return response;
      }
    } catch (error) {
      throw new Error(error);
    }
  },

  deleteSubDepartment: async id => {
    if (id) {
      try {
        set(() => {
          return {
            loading: true,
          };
        });
        const response = await axios.delete(
          `/departments/sub_department/${id}`
        );
        set(() => {
          return {
            department: get().department.filter(
              sub_department => sub_department.id !== id
            ),
          };
        });
        set(() => {
          return {
            loading: false,
          };
        });
        return response;
      } catch (error) {
        throw new Error(error);
      }
    }
  },
}));

export default useDepartmentsStore;
