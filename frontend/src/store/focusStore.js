import { create } from 'zustand';

export const useFocused = create(set => ({
  isFocused: '',

  setIsFocused: fieldName => {
    set(() => {
      return {
        isFocused: fieldName,
      };
    });
  },
}));
