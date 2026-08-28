import { create } from 'zustand'

type UIStore = {
  selectedFacility: string
  sidebarOpen: boolean
  analystOpen: boolean
  setFacility: (id: string) => void
  setSidebarOpen: (open: boolean) => void
  setAnalystOpen: (open: boolean) => void
}

export const useUIStore = create<UIStore>((set) => ({
  selectedFacility: 'all',
  sidebarOpen: false,
  analystOpen: false,
  setFacility: (selectedFacility) => set({ selectedFacility }),
  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
  setAnalystOpen: (analystOpen) => set({ analystOpen }),
}))

