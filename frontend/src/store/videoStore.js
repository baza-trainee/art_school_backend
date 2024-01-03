import { create } from 'zustand';
import axios from '@/utils/axios';
import { isDataValid } from '@/utils/formDataValidation';

const useVideoStore = create((set, get) => ({
  loading: false,
  videos: [],
  media: {},

  getAllVideo: async () => {
    const response = await axios.get(
      `/gallery/video?reverse=true&page=1&size=50`
    );
    try {
      set(() => {
        return {
          loading: true,
        };
      });
      set(() => {
        return {
          videos: response.data.items,
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

  getOneVideo: async id => {
    try {
      const response = await axios.get(`/gallery/video/${id}`);
      set(() => {
        return {
          video: response.data,
        };
      });
    } catch (error) {
      throw new Error(error);
    }
  },

  addVideo: async data => {
    if (isDataValid(data)) {
      try {
        const queryParams = new URLSearchParams();
        queryParams.append('media', data.get('media'));
        const response = await axios.post(
          `/gallery/video?${queryParams}`,
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
  editVideo: async (id, data) => {
    if (isDataValid(data)) {
      try {
        const queryParams = new URLSearchParams();
        queryParams.append('media', data.media);
        const response = await axios.put(
          `/gallery/video/${id}?${queryParams}`,
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
  deleteVideo: async id => {
    const response = await axios.delete(`/gallery/${id}`);
    set(() => {
      return {
        videos: get().videos.filter(video => video.id !== id),
      };
    });
    return response;
  },
}));

export default useVideoStore;
