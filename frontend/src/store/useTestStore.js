import { create } from 'zustand'

const useTestStore = create((set, get) => ({
  currentTest: null,
  answers: {},          // question_id -> answer string
  timeRemaining: null,  // seconds
  status: 'idle',       // idle | loading | in_progress | submitted | evaluated

  setTest: (test) => set({ currentTest: test, answers: {}, status: 'in_progress' }),
  setAnswer: (questionId, value) =>
    set((state) => ({ answers: { ...state.answers, [questionId]: value } })),
  setTimeRemaining: (secs) => set({ timeRemaining: secs }),
  setStatus: (status) => set({ status }),
  resetTest: () => set({ currentTest: null, answers: {}, timeRemaining: null, status: 'idle' }),

  getAnsweredCount: () => {
    const answers = get().answers
    return Object.values(answers).filter((a) => a && a.trim() !== '').length
  },

  getTotalQuestions: () => {
    const test = get().currentTest
    if (!test) return 0
    return test.sections.reduce((sum, s) => sum + s.questions.length, 0)
  },
}))

export default useTestStore
