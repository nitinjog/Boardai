import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useStudentStore = create(
  persist(
    (set, get) => ({
      student: null,
      diagnostics: {},   // subject -> diagnostic result

      setStudent: (student) => set({ student }),
      clearStudent: () => set({ student: null, diagnostics: {} }),

      setDiagnostic: (subject, result) =>
        set((state) => ({
          diagnostics: { ...state.diagnostics, [subject]: result },
        })),

      getDiagnostic: (subject) => get().diagnostics[subject] || null,

      isLoggedIn: () => !!get().student?.id,
    }),
    {
      name: 'boardai_student',
      partialize: (state) => ({ student: state.student, diagnostics: state.diagnostics }),
    }
  )
)

export default useStudentStore
