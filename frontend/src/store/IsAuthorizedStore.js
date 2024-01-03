import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';

export const useAuthorized = create()(
  devtools(
    persist(
      set => ({
        isAuthorized: false,
        setIsAuthorized: () => set({ isAuthorized: true }),
        setUnAuthorized: () => set({ isAuthorized: false }),
      }),

      {
        name: 'auth-storage',
      }
    )
  )
);
