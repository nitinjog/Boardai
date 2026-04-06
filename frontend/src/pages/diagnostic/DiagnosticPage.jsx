import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import useStudentStore from '../../store/useStudentStore'
import { startDiagnostic, submitDiagnostic } from '../../api/diagnostics'
import ProgressBar from '../../components/ui/ProgressBar'
import Spinner from '../../components/ui/Spinner'
import ErrorMessage from '../../components/shared/ErrorMessage'

export default function DiagnosticPage() {
  const { subject } = useParams()
  const decodedSubject = decodeURIComponent(subject)
  const { student, setDiagnostic } = useStudentStore()
  const navigate = useNavigate()

  const [sessionId, setSessionId] = useState(null)
  const [questions, setQuestions] = useState([])
  const [currentIdx, setCurrentIdx] = useState(0)
  const [responses, setResponses] = useState({})
  const [phase, setPhase] = useState('loading')  // loading | answering | submitting | done
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!student?.id) return navigate('/onboarding')
    startDiagnostic(student.id, decodedSubject)
      .then((data) => {
        setSessionId(data.session_id)
        setQuestions(data.questions)
        setPhase('answering')
      })
      .catch((err) => { setError(err.message); setPhase('error') })
  }, []) // eslint-disable-line

  const currentQ = questions[currentIdx]
  const isLast = currentIdx === questions.length - 1
  const answered = responses[currentQ?.id] !== undefined

  const handleSelect = (value) => {
    setResponses((prev) => ({ ...prev, [currentQ.id]: value }))
  }

  const handleNext = () => {
    if (!answered) return
    if (!isLast) { setCurrentIdx((i) => i + 1) }
    else handleSubmit()
  }

  const handleSubmit = async () => {
    setPhase('submitting')
    try {
      const data = await submitDiagnostic(sessionId, responses)
      setDiagnostic(decodedSubject, data)
      setResult(data)
      setPhase('done')
    } catch (err) {
      setError(err.message)
      setPhase('error')
    }
  }

  if (phase === 'loading') return (
    <div className="flex flex-col items-center justify-center py-20 gap-4">
      <Spinner size="lg" />
      <p className="text-gray-500">Preparing diagnostic questions…</p>
    </div>
  )

  if (phase === 'error') return <ErrorMessage message={error} onRetry={() => window.location.reload()} />

  if (phase === 'submitting') return (
    <div className="flex flex-col items-center justify-center py-20 gap-4">
      <Spinner size="lg" />
      <p className="text-gray-500 text-center">
        Analysing your responses with AI…<br />
        <span className="text-xs">This takes about 10 seconds</span>
      </p>
    </div>
  )

  if (phase === 'done' && result) {
    return (
      <div className="max-w-lg mx-auto animate-slide-up">
        <div className="card text-center">
          <div className="text-5xl mb-4">✅</div>
          <h2 className="text-xl font-bold text-gray-800 mb-2">Diagnostic Complete!</h2>
          <p className="text-gray-500 mb-6">{result.message}</p>

          <div className="mb-6">
            <div className="flex justify-center items-center gap-3 mb-3">
              <span className="text-sm font-medium text-gray-600">Confidence Score:</span>
              <span className="text-2xl font-bold text-brand-600">{result.confidence_score?.toFixed(1)}/5</span>
            </div>
            <ProgressBar value={result.confidence_score} max={5} color="brand" showPercent />
          </div>

          {result.weak_topics?.length > 0 && (
            <div className="text-left mb-4 p-4 bg-red-50 rounded-xl">
              <p className="text-sm font-semibold text-red-700 mb-2">📍 Topics to focus on:</p>
              <div className="flex flex-wrap gap-2">
                {result.weak_topics.map((t) => (
                  <span key={t} className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full">{t}</span>
                ))}
              </div>
            </div>
          )}

          {result.strong_topics?.length > 0 && (
            <div className="text-left mb-6 p-4 bg-green-50 rounded-xl">
              <p className="text-sm font-semibold text-green-700 mb-2">💪 Your strong areas:</p>
              <div className="flex flex-wrap gap-2">
                {result.strong_topics.map((t) => (
                  <span key={t} className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">{t}</span>
                ))}
              </div>
            </div>
          )}

          <div className="flex gap-3">
            <button onClick={() => navigate('/dashboard')} className="btn-ghost flex-1">← Dashboard</button>
            <button
              onClick={() => navigate(`/generate-test/${encodeURIComponent(decodedSubject)}`)}
              className="btn-primary flex-1"
            >
              Generate Mock Test →
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-lg mx-auto animate-fade-in">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-2">
          <button onClick={() => navigate('/dashboard')} className="text-gray-400 hover:text-gray-600 text-sm">← Back</button>
          <span className="text-gray-300">|</span>
          <span className="text-sm text-gray-500">{decodedSubject} Diagnostic</span>
        </div>
        <ProgressBar value={currentIdx + 1} max={questions.length} showPercent label={`Question ${currentIdx + 1} of ${questions.length}`} />
      </div>

      {currentQ && (
        <div className="card animate-slide-up">
          {/* Question type badge */}
          <div className="flex items-center gap-2 mb-4">
            <span className={`text-xs px-2 py-1 rounded-full font-medium
              ${currentQ.type === 'confidence' ? 'bg-blue-100 text-blue-700' :
                currentQ.type === 'topic_strength' ? 'bg-purple-100 text-purple-700' :
                'bg-yellow-100 text-yellow-700'}`}>
              {currentQ.type === 'confidence' ? '💬 Confidence' :
               currentQ.type === 'topic_strength' ? `📚 ${currentQ.topic}` : '📈 Past Performance'}
            </span>
          </div>

          <h2 className="text-lg font-semibold text-gray-800 mb-6 leading-relaxed">
            {currentQ.question}
          </h2>

          <div className="space-y-3 mb-8">
            {currentQ.options?.map((opt, i) => (
              <button
                key={i}
                onClick={() => handleSelect(opt)}
                className={`w-full text-left px-4 py-3 rounded-xl border-2 transition-all text-sm
                  ${responses[currentQ.id] === opt
                    ? 'border-brand-600 bg-brand-50 text-brand-700 font-medium'
                    : 'border-gray-200 hover:border-brand-300 text-gray-700'}`}
              >
                {opt}
              </button>
            ))}
          </div>

          <button
            onClick={handleNext}
            disabled={!answered}
            className="btn-primary w-full"
          >
            {isLast ? 'Submit Diagnostic →' : 'Next Question →'}
          </button>
        </div>
      )}
    </div>
  )
}
