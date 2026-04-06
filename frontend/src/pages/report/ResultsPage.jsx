import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getReport, downloadReportPdf } from '../../api/reports'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import Spinner from '../../components/ui/Spinner'
import Badge from '../../components/ui/Badge'
import ErrorMessage from '../../components/shared/ErrorMessage'

function ScoreCircle({ score, max, grade }) {
  const pct = (score / max) * 100
  const color = pct >= 75 ? '#059669' : pct >= 45 ? '#d97706' : '#dc2626'
  const gradeBg = pct >= 75 ? 'bg-green-100 text-green-800' : pct >= 45 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'
  return (
    <div className="text-center">
      <div className="relative inline-flex items-center justify-center w-36 h-36 mb-4">
        <svg className="absolute w-36 h-36 -rotate-90" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r="50" fill="none" stroke="#e5e7eb" strokeWidth="10" />
          <circle cx="60" cy="60" r="50" fill="none" stroke={color} strokeWidth="10"
            strokeDasharray={`${(pct / 100) * 314} 314`} strokeLinecap="round" />
        </svg>
        <div>
          <div className="text-3xl font-black" style={{ color }}>{score}</div>
          <div className="text-xs text-gray-400">/{max}</div>
        </div>
      </div>
      <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full font-bold text-lg ${gradeBg}`}>
        Grade {grade}
      </div>
      <p className="text-gray-500 text-sm mt-2">{pct.toFixed(1)}% · {pct >= 75 ? 'Excellent' : pct >= 60 ? 'Good' : pct >= 45 ? 'Average' : pct >= 33 ? 'Pass' : 'Needs Work'}</p>
    </div>
  )
}

function TopicChart({ topicScores }) {
  const data = topicScores.map((ts) => ({
    name: ts.topic.length > 18 ? ts.topic.slice(0, 18) + '…' : ts.topic,
    percentage: Math.round(ts.percentage),
    score: ts.score,
    max: ts.max_score,
  }))
  const getColor = (pct) => pct >= 70 ? '#059669' : pct >= 40 ? '#d97706' : '#dc2626'
  return (
    <div className="card">
      <h3 className="font-semibold text-gray-700 mb-4">Topic-wise Performance</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data} layout="vertical" margin={{ left: 20, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} tick={{ fontSize: 11 }} />
          <YAxis type="category" dataKey="name" width={140} tick={{ fontSize: 10 }} />
          <Tooltip
            formatter={(v, name, props) => [`${props.payload.score}/${props.payload.max} (${v}%)`, 'Score']}
          />
          <Bar dataKey="percentage" radius={[0, 4, 4, 0]}>
            {data.map((entry) => (
              <Cell key={entry.name} fill={getColor(entry.percentage)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function ResultsPage() {
  const { testId } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('overview')
  const [pdfLoading, setPdfLoading] = useState(false)

  useEffect(() => {
    getReport(testId)
      .then(setReport)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [testId])

  const handleDownloadReport = async () => {
    if (!report) return
    setPdfLoading(true)
    try {
      const blob = await downloadReportPdf(report.id)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `BoardAI_Report_${report.subject}_${report.id.slice(0, 8)}.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      setError(e.message)
    } finally {
      setPdfLoading(false)
    }
  }

  if (loading) return <div className="flex justify-center py-24"><Spinner size="lg" /></div>
  if (error) return <ErrorMessage message={error} />
  if (!report) return null

  const tabs = ['overview', 'questions', 'plan']

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="page-title mb-0">{report.subject} — Evaluation Report</h1>
          <p className="text-gray-500 text-sm">
            {new Date(report.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}
          </p>
        </div>
        <div className="flex gap-2">
          <button onClick={handleDownloadReport} disabled={pdfLoading} className="btn-secondary text-sm">
            {pdfLoading ? <Spinner size="sm" /> : '📥 Download PDF'}
          </button>
          <button onClick={() => navigate('/dashboard')} className="btn-ghost text-sm">← Dashboard</button>
        </div>
      </div>

      {/* Score card */}
      <div className="card mb-6 flex flex-col sm:flex-row items-center gap-8">
        <ScoreCircle score={report.total_score} max={report.max_score} grade={report.grade} />
        <div className="flex-1">
          <div className="grid grid-cols-2 gap-3 mb-4">
            {[
              { label: 'Total Score', value: `${report.total_score}/${report.max_score}` },
              { label: 'Percentage', value: `${report.percentage.toFixed(1)}%` },
              { label: 'Grade', value: report.grade },
              { label: 'Questions', value: report.question_feedback?.length || '—' },
            ].map(({ label, value }) => (
              <div key={label} className="bg-gray-50 rounded-xl p-3">
                <p className="text-xs text-gray-400 mb-0.5">{label}</p>
                <p className="font-bold text-gray-800">{value}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-gray-500">
            CBSE pass mark is <strong>33%</strong>.{' '}
            {report.percentage >= 75 ? '🏆 Outstanding performance!' :
             report.percentage >= 60 ? '👍 Good work — keep it up!' :
             report.percentage >= 33 ? "📚 Passed — but there's room to grow." :
             '⚠️ Below pass mark. Study the weak topics in your plan.'}
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-100 p-1 rounded-xl mb-6">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all capitalize
              ${activeTab === tab ? 'bg-white shadow text-brand-700' : 'text-gray-500 hover:text-gray-700'}`}
          >
            {tab === 'overview' ? '📊 Overview' : tab === 'questions' ? '📝 Questions' : '📅 Study Plan'}
          </button>
        ))}
      </div>

      {/* Overview tab */}
      {activeTab === 'overview' && (
        <div className="space-y-5 animate-fade-in">
          {report.topic_scores?.length > 0 && <TopicChart topicScores={report.topic_scores} />}

          <div className="grid sm:grid-cols-2 gap-4">
            {report.strengths?.length > 0 && (
              <div className="card bg-green-50 border-green-100">
                <h3 className="font-semibold text-green-800 mb-3">💪 Strengths</h3>
                <ul className="space-y-2">
                  {report.strengths.map((s, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-green-700">
                      <span className="text-green-500 mt-0.5">✓</span> {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {report.weaknesses?.length > 0 && (
              <div className="card bg-red-50 border-red-100">
                <h3 className="font-semibold text-red-800 mb-3">⚠️ Areas to Improve</h3>
                <ul className="space-y-2">
                  {report.weaknesses.map((w, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-red-700">
                      <span className="text-red-400 mt-0.5">✗</span> {w}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {report.recommendations?.length > 0 && (
            <div className="card">
              <h3 className="font-semibold text-gray-700 mb-3">💡 Recommendations</h3>
              <ol className="space-y-2">
                {report.recommendations.filter(Boolean).map((r, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-gray-600">
                    <span className="shrink-0 w-6 h-6 bg-brand-100 text-brand-600 rounded-full flex items-center justify-center text-xs font-bold">
                      {i + 1}
                    </span>
                    {r}
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>
      )}

      {/* Questions tab */}
      {activeTab === 'questions' && (
        <div className="space-y-3 animate-fade-in">
          {report.question_feedback?.map((qf, i) => {
            const pct = qf.max_marks > 0 ? (qf.marks_awarded / qf.max_marks) * 100 : 0
            const statusColor = pct === 100 ? 'green' : pct > 0 ? 'yellow' : 'red'
            return (
              <details key={qf.question_id} className="card cursor-pointer">
                <summary className="flex items-center gap-3 list-none">
                  <span className="shrink-0 font-bold text-gray-500 text-sm w-6">Q{i + 1}</span>
                  <span className="flex-1 text-sm text-gray-700 font-medium line-clamp-1">{qf.question_text}</span>
                  <Badge variant={statusColor}>
                    {qf.marks_awarded}/{qf.max_marks}
                  </Badge>
                </summary>
                <div className="mt-4 pt-4 border-t border-gray-100 space-y-3 text-sm">
                  <div>
                    <p className="text-xs font-semibold text-gray-400 mb-1">Your Answer:</p>
                    <p className="text-gray-700 bg-gray-50 rounded-lg p-3">{qf.student_answer || '(Not answered)'}</p>
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-gray-400 mb-1">Model Answer:</p>
                    <p className="text-gray-600 bg-green-50 rounded-lg p-3 text-xs leading-relaxed">{qf.expected_answer}</p>
                  </div>
                  <div className={`p-3 rounded-lg text-xs
                    ${statusColor === 'green' ? 'bg-green-50 text-green-700' :
                      statusColor === 'yellow' ? 'bg-yellow-50 text-yellow-700' : 'bg-red-50 text-red-700'}`}>
                    💬 {qf.feedback}
                  </div>
                  {qf.error_type && qf.error_type !== 'correct' && (
                    <Badge variant="yellow">Error type: {qf.error_type}</Badge>
                  )}
                </div>
              </details>
            )
          })}
        </div>
      )}

      {/* Study plan tab */}
      {activeTab === 'plan' && (
        <div className="animate-fade-in">
          {report.improvement_plan?.study_schedule ? (
            <div className="space-y-4">
              <p className="text-gray-500 text-sm mb-4">
                Here's your personalised 4-week study plan based on your performance:
              </p>
              {Object.entries(report.improvement_plan.study_schedule).map(([week, data]) => (
                <div key={week} className="card">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 bg-brand-100 text-brand-700 rounded-xl flex items-center justify-center font-bold text-sm">
                      {week.replace('week_', 'W')}
                    </div>
                    <div>
                      <p className="font-semibold text-gray-800">{data.focus}</p>
                      <p className="text-xs text-gray-400">{data.daily_hours} hrs/day</p>
                    </div>
                  </div>
                  <ul className="space-y-1 mb-3">
                    {data.activities?.map((a, i) => (
                      <li key={i} className="text-sm text-gray-600 flex items-center gap-2">
                        <span className="text-brand-400">•</span> {a}
                      </li>
                    ))}
                  </ul>
                  {data.resources?.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {data.resources.map((r, i) => (
                        <span key={i} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">📚 {r}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              {report.improvement_plan.expected_improvement && (
                <div className="card bg-brand-50 border-brand-200">
                  <p className="text-sm font-semibold text-brand-700 mb-1">🎯 Expected Outcome</p>
                  <p className="text-sm text-brand-600">{report.improvement_plan.expected_improvement}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="card text-center py-12">
              <p className="text-gray-400">Study plan not available for this report.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
