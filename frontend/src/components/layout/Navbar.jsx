import { Link, useNavigate } from 'react-router-dom'
import useStudentStore from '../../store/useStudentStore'

export default function Navbar() {
  const { student, clearStudent } = useStudentStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    clearStudent()
    navigate('/')
  }

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to={student ? '/dashboard' : '/'} className="flex items-center gap-2">
          <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">B</div>
          <span className="font-bold text-brand-900 text-lg">BoardAI</span>
        </Link>

        {student && (
          <div className="flex items-center gap-4">
            <Link to="/dashboard" className="text-sm text-gray-600 hover:text-brand-600 font-medium transition-colors">
              Dashboard
            </Link>
            <Link to="/diagnostic" className="text-sm text-gray-600 hover:text-brand-600 font-medium transition-colors">
              Diagnostic
            </Link>
            <div className="flex items-center gap-3 ml-4 pl-4 border-l border-gray-200">
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-800">{student.name}</p>
                <p className="text-xs text-gray-500">Class {student.class_level}</p>
              </div>
              <button onClick={handleLogout} className="text-xs text-gray-500 hover:text-red-600 transition-colors">
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
