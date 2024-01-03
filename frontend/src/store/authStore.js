import { create } from 'zustand';
import axios from '@/utils/axios';
import { isDataValid } from '@/utils/formDataValidation';

const useAuthStore = create(set => ({
  loading: false,

  login: async data => {
    try {
      if (isDataValid(data)) {
        const requestData = new URLSearchParams(data);
        await axios
          .post(`/auth/login`, requestData, {})
          .then(response => {
            const token = response.data.access_token;
            if (token) {
              window.localStorage.setItem('access_token', token);
            }
          })
          .catch(error => {
            console.error('Fetch error:', error);
          });
      }
    } catch (error) {
      console.error(error);
    }
  },

  sendMail: async data => {
    if (data.email !== undefined) {
      try {
        const response = await axios.post(`/auth/forgot-password`, data, {});
        console.log(response.data);
        return response.data;
      } catch (error) {
        console.error(error);
      }
    }
  },

  resetPassword: async data => {
    try {
      if (!Object.values(data).includes(undefined)) {
        const response = await axios.post(`/auth/reset-password`, data, {});
        return response;
      }
    } catch (error) {
      console.error(error);
    }
  },

  changePassword: async data => {
    try {
      set(() => {
        return {
          loading: true,
        };
      });
      if (isDataValid(data)) {
        const requestData = new URLSearchParams(data);
        const response = await axios.post(
          `/auth/change-password`,
          requestData,
          {}
        );
        set(() => {
          return {
            loading: false,
          };
        });
        return response;
      }
    } catch (error) {
      console.error(error);
    }
  },
}));

export default useAuthStore;
