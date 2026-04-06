import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import useStudentStore from '../../store/useStudentStore'
import { getStudentTests } from '../../api/tests'
import { getStudentHistory } from '../../api/reports'
import { SUBJECT_ICONS, SUBJECT_COLORS } from '../../constants/subjects'
import Badge from '../../components/ui/Badge'
import Spinner from '../../components/ui/Spinner'

const STATUS_BADGE = {
  generated: { label: 'Ready', variant: 'blue' },
  in_progress: { label: 'In Progress', variant: 'yellow' },
  submitted: { label: 'Submitted', variant: 'orange' },
  evaluated: { label: 'Evaluated', variant: 'green' },
}

export default function DashboardPage() {
  const { student, diagnostics } = useStudentStore()
  const navigate = useNavigate()
  const [tests, setTests] = useState([])
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  const subjects = student?.subjects || []

  useEffect(() => {
    if (!student?.id) return
    Promise.all([
      getStudentTests(student.id).catch(() => []),
      getStudentHistory(student.id).catch(() => []),
    ]).then(([t, h]) => {
      setTests(t)
      setHistory(h)
      setLoading(false)
    })
  }, [student?.id])

  const getLatestTestForSubject = (subject) =>
    tests.find((t) => t.subject === subject)

  const hasDiagnostic = (subject) => !!diagnostics[subject]

  const avgScore = history.length
    ? (history.reduce((sum, h) => sum + h.percentage, 0) / history.length).toFixed(0)
    : null

  if (loading) return (
    <div className="flex justify-center py-20"><Spinner size="lg" /></div>
  )

  return (
    <div className="animate-fade-in">
      {/* Welcome header */}
      <div className="mb-8">
        <h1 className="page-title">Welcome back, {student?.name?.split(' ')[0]}! 👋</h1>
        <p className="text-gray-500">Class {student?.class_level} · {subjects.length} subjects enrolled</p>
      </div>

      {/* Stats row */}
      {history.length > 0 && (
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="card text-center">
            <div className="text-3xl font-bold text-brand-600">{history.length}</div>
            <div className="text-xs text-gray-500 mt-1">Tests Taken</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl font-bold text-green-600">{avgScore}%</div>
            <div className="text-xs text-gray-500 mt-1">Average Score</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl font-bold text-purple-600">
              {subjects.filter(hasDiagnostic).length}/{subjects.length}
            </div>
            <div className="text-xs text-gray-500 mt-1">Diagnostics Done</div>
          </div>
        </div>
      )}

      {/* Subject cards */}
      <h2 className="section-title mb-4">Your Subjects</h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-10">
        {subjects.map((subject) => {
          const diag = diagnostics[subject]
          const latestTest = getLatestTestForSubject(subject)
          const color = SUBJECT_COLORS[subject] || 'blue'

          return (
            <div key={subject} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{SUBJECT_ICONS[subject] || '📚'}</span>
                  <div>
                    <h3 className="font-semibold text-gray-800">{subject}</h3>
                    <p className="text-xs text-gray-400">Class {student?.class_level}</p>
                  </div>
                </div>
                {diag ? (
                  <Badge variant="green">Diagnosed ✓</Badge>
                ) : (
                  <Badge variant="gray">Not started</Badge>
                )}
              </div>

              {diag && (
                <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500 mb-2">Weak topics:</p>
                  <div className="flex flex-wrap gap-1">
                    {(diag.weak_topics || []).slice(0, 3).map((t) => (
                      <span key={t} className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full">{t}</span>
                    ))}
                    {!diag.weak_topics?.length && <span className="text-xs text-green-700">No major weak areas</span>}
                  </div>
                </div>
              )}

              {latestTest && (
                <div className="mb-4 flex items-center justify-between text-sm">
                  <span className="text-gray-500">Last test:</span>
                  <Badge variant={STATUS_BADGE[latestTest.status]?.variant || 'gray'}>
                    {STATUS_BADGE[latestTest.status]?.label || latestTest.status}
                  </Badge>
                </div>
              )}

              <div className="flex gap-2 mt-auto">
                {!diag ? (
                  <Link to={`/diagnostic/${encodeURIComponent(subject)}`} className="btn-primary text-xs flex-1 text-center">
                    Start Diagnostic →
                  </Link>
                ) : !latestTest || latestTest.status === 'evaluated' ? (
                  <Link
                    to={`/generate-test/${encodeURIComponent(subject)}`}
                    className="btn-primary text-xs flex-1 text-center"
                  >
                    Generate Test →
                  </Link>
                ) : latestTest.status === 'generated' ? (
                  <Link to={`/test/${latestTest.id}`} className="btn-primary text-xs flex-1 text-center">
                    Start Test →
                  </Link>
                ) : latestTest.status === 'in_progress' ? (
                  <Link to={`/test/${latestTest.id}`} className="btn-primary text-xs flex-1 text-center">
                    Resume Test →
                  </Link>
                ) : latestTest.status === 'submitted' ? (
                  <Link to={`/evaluate/${latestTest.id}`} className="btn-primary text-xs flex-1 text-center">
                    Get Results →
                  </Link>
                ) : null}

                {latestTest?.status === 'evaluated' && (
                  <Link to={`/results/${latestTest.id}`} className="btn-secondary text-xs flex-1 text-center">
                    View Report
                  </Link>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {/* Recent test history */}
      {history.length > 0 && (
        <div>
          <h2 className="section-title mb-4">Recent Results</h2>
          <div className="card overflow-hidden p-0">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  {['Subject', 'Date', 'Score', 'Grade'].map((h) => (
                    <th key={h} className="text-left text-xs font-semibold text-gray-500 px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {history.slice(0, 5).map((h) => (
                  <tr key={h.test_id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-gray-800">
                      {SUBJECT_ICONS[h.subject]} {h.subject}
                    </td>
                    <td className="px-4 py-3 text-gray-500">
                      {new Date(h.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
                    </td>
                    <td className="px-4 py-3 font-semibold">
                      <span className={h.percentage >= 60 ? 'text-green-600' : h.percentage >= 33 ? 'text-yellow-600' : 'text-red-600'}>
                        {h.score}/{h.max_score} ({h.percentage.toFixed(0)}%)
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <Badge variant={h.grade.startsWith('A') ? 'green' : h.grade.startsWith('B') ? 'blue' : h.grade === 'E' ? 'red' : 'yellow'}>
                        {h.grade}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
