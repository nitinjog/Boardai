import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import useStudentStore from '../../store/useStudentStore'
import { generateTest } from '../../api/tests'
import Spinner from '../../components/ui/Spinner'

export default function GenerateTestPage() {
  const { subject } = useParams()
  const decodedSubject = decodeURIComponent(subject)
  const { student, diagnostics } = useStudentStore()
  const navigate = useNavigate()

  const [totalMarks, setTotalMarks] = useState(80)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const diag = diagnostics[decodedSubject]

  const handleGenerate = async () => {
    setLoading(true)
    setError('')
    try {
      const test = await generateTest({
        student_id: student.id,
        subject: decodedSubject,
        total_marks: totalMarks,
      })
      navigate(`/test/${test.id}`)
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  if (loading) return (
    <div className="flex flex-col items-center justify-center py-24 gap-6">
      <div className="relative">
        <Spinner size="lg" />
        <div className="absolute inset-0 flex items-center justify-center text-2xl">🤖</div>
      </div>
      <div className="text-center">
        <p className="text-gray-700 font-semibold text-lg">Generating your mock test…</p>
        <p className="text-gray-500 text-sm mt-1">
          Our AI is crafting a personalised CBSE {decodedSubject} paper.<br />
          This takes 15–30 seconds on the free tier.
        </p>
      </div>
    </div>
  )

  return (
    <div className="max-w-lg mx-auto animate-fade-in">
      <button onClick={() => navigate('/dashboard')} className="text-sm text-gray-500 hover:text-gray-700 mb-6 flex items-center gap-1">
        ← Dashboard
      </button>

      <div className="card">
        <h1 className="page-title mb-1">Generate Mock Test</h1>
        <p className="text-gray-500 text-sm mb-6">{decodedSubject} · Class {student?.class_level}</p>

        {diag && (
          <div className="mb-6 p-4 bg-brand-50 rounded-xl">
            <p className="text-sm font-semibold text-brand-700 mb-2">🎯 Your test will focus on:</p>
            {diag.weak_topics?.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {diag.weak_topics.map((t) => (
                  <span key={t} className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full">{t}</span>
                ))}
              </div>
            ) : (
              <p className="text-xs text-gray-500">No weak areas identified — you'll get a balanced paper.</p>
            )}
          </div>
        )}

        {!diag && (
          <div className="mb-6 p-4 bg-yellow-50 rounded-xl border border-yellow-200">
            <p className="text-sm text-yellow-700">
              ⚠️ You haven't completed the diagnostic for {decodedSubject} yet.
              The test will be generated with a standard balanced distribution.
            </p>
          </div>
        )}

        {/* Paper type selection */}
        <div className="mb-6">
          <p className="text-sm font-semibold text-gray-700 mb-3">Select paper type:</p>
          <div className="grid grid-cols-2 gap-3">
            {[
              { marks: 80, label: 'Full Paper', time: '3 hours', sections: 'MCQ + Short + Long + Case-based', badge: 'Recommended' },
              { marks: 40, label: 'Half Paper', time: '1.5 hours', sections: 'MCQ + Short + Long', badge: 'Practice' },
            ].map((opt) => (
              <button
                key={opt.marks}
                onClick={() => setTotalMarks(opt.marks)}
                className={`p-4 rounded-xl border-2 text-left transition-all
                  ${totalMarks === opt.marks ? 'border-brand-600 bg-brand-50' : 'border-gray-200 hover:border-brand-300'}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className={`font-bold text-lg ${totalMarks === opt.marks ? 'text-brand-700' : 'text-gray-700'}`}>
                    {opt.marks} marks
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full
                    ${opt.marks === 80 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                    {opt.badge}
                  </span>
                </div>
                <p className="text-xs text-gray-500">{opt.label} · {opt.time}</p>
                <p className="text-xs text-gray-400 mt-1">{opt.sections}</p>
              </button>
            ))}
          </div>
        </div>

        {error && <p className="text-red-600 text-sm mb-4">{error}</p>}

        <button onClick={handleGenerate} className="btn-primary w-full text-base py-3">
          🤖 Generate My Personalised Test →
        </button>

        <p className="text-xs text-gray-400 text-center mt-3">
          Powered by Google Gemini AI · CBSE 2024-25 pattern
        </p>
      </div>
    </div>
  )
}
