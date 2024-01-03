import { create } from 'zustand';

export const useConfirmDelete = create(set => ({
  isDeleteConfirm: false,
  confirmDelete: () => set({ isDeleteConfirm: true }),
}));
