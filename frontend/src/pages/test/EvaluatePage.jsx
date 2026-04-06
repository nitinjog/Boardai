import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { evaluateTest } from '../../api/evaluation'
import Spinner from '../../components/ui/Spinner'
import ErrorMessage from '../../components/shared/ErrorMessage'

export default function EvaluatePage() {
  const { testId } = useParams()
  const navigate = useNavigate()
  const [phase, setPhase] = useState('evaluating')
  const [error, setError] = useState('')

  useEffect(() => {
    evaluateTest(testId)
      .then((data) => {
        setPhase('done')
        setTimeout(() => navigate(`/results/${testId}`), 1500)
      })
      .catch((e) => {
        setError(e.message)
        setPhase('error')
      })
  }, [testId]) // eslint-disable-line

  if (phase === 'error') return <ErrorMessage message={error} onRetry={() => { setPhase('evaluating'); setError(''); evaluateTest(testId).then(() => navigate(`/results/${testId}`)).catch((e) => { setError(e.message); setPhase('error') }) }} />

  return (
    <div className="flex flex-col items-center justify-center py-24 gap-6">
      {phase === 'evaluating' ? (
        <>
          <div className="relative w-20 h-20">
            <Spinner size="lg" className="absolute inset-0 m-auto" />
            <div className="absolute inset-0 flex items-center justify-center text-3xl">📝</div>
          </div>
          <div className="text-center max-w-sm">
            <h2 className="text-xl font-bold text-gray-800 mb-2">AI is Evaluating Your Test</h2>
            <p className="text-gray-500 text-sm">
              Our AI examiner is reviewing every answer, awarding marks, and preparing your personalised feedback.
            </p>
            <p className="text-xs text-gray-400 mt-3">This takes 20–40 seconds…</p>
          </div>
          <div className="grid grid-cols-3 gap-4 mt-4 text-center">
            {['Checking answers', 'Awarding marks', 'Building report'].map((step, i) => (
              <div key={step} className="p-3 bg-brand-50 rounded-xl">
                <div className="text-brand-600 mb-1">{i === 0 ? '✅' : i === 1 ? '📊' : '📋'}</div>
                <p className="text-xs text-gray-600">{step}</p>
              </div>
            ))}
          </div>
        </>
      ) : (
        <>
          <div className="text-5xl">🎉</div>
          <h2 className="text-xl font-bold text-gray-800">Evaluation Complete!</h2>
          <p className="text-gray-500">Redirecting to your report…</p>
          <Spinner size="sm" />
        </>
      )}
    </div>
  )
}
