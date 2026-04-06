import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom'
import useStudentStore from './store/useStudentStore'
import AppLayout from './components/layout/AppLayout'

import HomePage from './pages/HomePage'
import OnboardingPage from './pages/onboarding/OnboardingPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import DiagnosticPage from './pages/diagnostic/DiagnosticPage'
import GenerateTestPage from './pages/test/GenerateTestPage'
import TestModePage from './pages/test/TestModePage'
import OnlineTestPage from './pages/test/OnlineTestPage'
import EvaluatePage from './pages/test/EvaluatePage'
import UploadPage from './pages/upload/UploadPage'
import ResultsPage from './pages/report/ResultsPage'

function Protected({ children }) {
  const isLoggedIn = useStudentStore((s) => s.isLoggedIn())
  if (!isLoggedIn) return <Navigate to="/onboarding" replace />
  return children
}

const router = createBrowserRouter([
  { path: '/', element: <HomePage /> },
  { path: '/onboarding', element: <OnboardingPage /> },
  {
    element: <AppLayout />,
    children: [
      {
        path: '/dashboard',
        element: <Protected><DashboardPage /></Protected>,
      },
      {
        path: '/diagnostic/:subject',
        element: <Protected><DiagnosticPage /></Protected>,
      },
      {
        path: '/generate-test/:subject',
        element: <Protected><GenerateTestPage /></Protected>,
      },
      {
        path: '/test/:testId',
        element: <Protected><TestModePage /></Protected>,
      },
      {
        path: '/test/:testId/attempt',
        element: <Protected><OnlineTestPage /></Protected>,
      },
      {
        path: '/test/:testId/upload',
        element: <Protected><UploadPage /></Protected>,
      },
      {
        path: '/evaluate/:testId',
        element: <Protected><EvaluatePage /></Protected>,
      },
      {
        path: '/results/:testId',
        element: <Protected><ResultsPage /></Protected>,
      },
    ],
  },
  { path: '*', element: <Navigate to="/" replace /> },
])

export default function App() {
  return <RouterProvider router={router} />
}
