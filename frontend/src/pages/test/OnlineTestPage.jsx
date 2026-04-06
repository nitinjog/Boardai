import { useState, useEffect, useCallback, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getTest, startTest, submitTest } from '../../api/tests'
import useStudentStore from '../../store/useStudentStore'
import useTestStore from '../../store/useTestStore'
import { useTimer } from '../../hooks/useTimer'
import Spinner from '../../components/ui/Spinner'
import ProgressBar from '../../components/ui/ProgressBar'
import ErrorMessage from '../../components/shared/ErrorMessage'
import { AUTOSAVE_INTERVAL_MS } from '../../constants/config'

function TimerBar({ formattedTime, percentRemaining, isWarning }) {
  return (
    <div className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-brand-600 rounded flex items-center justify-center text-white text-xs font-bold">B</div>
          <span className="font-semibold text-gray-700 text-sm">BoardAI Test</span>
        </div>
        <div className="flex-1 max-w-xs">
          <ProgressBar
            value={percentRemaining}
            max={100}
            color={percentRemaining > 20 ? 'brand' : percentRemaining > 10 ? 'yellow' : 'red'}
          />
        </div>
        <div className={`font-mono font-bold text-lg ${isWarning ? 'timer-warning' : 'text-gray-800'}`}>
          ⏱ {formattedTime}
        </div>
      </div>
    </div>
  )
}

function QuestionNav({ sections, answers, currentQId, onJump }) {
  const allQuestions = sections.flatMap((s) => s.questions)
  let idx = 0
  return (
    <div className="space-y-4">
      {sections.map((sec) => (
        <div key={sec.name}>
          <p className="text-xs font-semibold text-gray-400 mb-2 uppercase tracking-wide">{sec.name}</p>
          <div className="grid grid-cols-5 gap-1">
            {sec.questions.map((q) => {
              const num = ++idx
              const isAnswered = answers[q.id]?.trim()
              const isCurrent = q.id === currentQId
              return (
                <button
                  key={q.id}
                  onClick={() => onJump(q.id)}
                  className={`w-8 h-8 rounded text-xs font-semibold transition-all
                    ${isCurrent ? 'bg-brand-600 text-white ring-2 ring-brand-300' :
                      isAnswered ? 'bg-green-500 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                >
                  {num}
                </button>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}

export default function OnlineTestPage() {
  const { testId } = useParams()
  const navigate = useNavigate()
  const { student } = useStudentStore()
  const { currentTest, answers, setTest, setAnswer, setStatus, resetTest } = useTestStore()

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [currentQId, setCurrentQId] = useState(null)
  const [showSubmitModal, setShowSubmitModal] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [durationSecs, setDurationSecs] = useState(0)
  const startTimeRef = useRef(null)

  // Prevent copy/paste
  useEffect(() => {
    const prevent = (e) => e.preventDefault()
    document.addEventListener('copy', prevent)
    document.addEventListener('paste', prevent)
    document.addEventListener('contextmenu', prevent)
    return () => {
      document.removeEventListener('copy', prevent)
      document.removeEventListener('paste', prevent)
      document.removeEventListener('contextmenu', prevent)
    }
  }, [])

  useEffect(() => {
    const init = async () => {
      try {
        const [testData, startData] = await Promise.all([
          getTest(testId),
          startTest(testId),
        ])
        setTest(testData)
        const secs = startData.duration_minutes * 60
        setDurationSecs(secs)
        const firstQ = testData.sections[0]?.questions[0]
        if (firstQ) setCurrentQId(firstQ.id)
        startTimeRef.current = Date.now()
        setLoading(false)
      } catch (e) {
        setError(e.message)
        setLoading(false)
      }
    }
    init()
    return () => resetTest()
  }, [testId]) // eslint-disable-line

  const handleExpire = useCallback(() => {
    if (!submitting) handleSubmit(true)
  }, [submitting]) // eslint-disable-line

  const { formattedTime, isWarning, percentRemaining } = useTimer(durationSecs, handleExpire)

  // Autosave to backend every 10s (simplified: just keep in store)
  useEffect(() => {
    const interval = setInterval(() => {
      // In production: POST to /answers with current answers batch
      // For now answers are kept in Zustand and submitted on final submit
    }, AUTOSAVE_INTERVAL_MS)
    return () => clearInterval(interval)
  }, [answers])

  const handleSubmit = async (autoSubmit = false) => {
    setSubmitting(true)
    setShowSubmitModal(false)
    const timeTaken = startTimeRef.current
      ? Math.round((Date.now() - startTimeRef.current) / 60000)
      : null
    try {
      await submitTest(testId, {
        test_id: testId,
        student_id: student.id,
        answers,
        time_taken_minutes: timeTaken,
      })
      setStatus('submitted')
      navigate(`/evaluate/${testId}`)
    } catch (e) {
      setError(e.message)
      setSubmitting(false)
    }
  }

  if (loading || !currentTest) return <div className="flex justify-center py-32"><Spinner size="lg" /></div>
  if (error) return <ErrorMessage message={error} />

  const allQuestions = currentTest.sections.flatMap((s) => s.questions)
  const currentQ = allQuestions.find((q) => q.id === currentQId) || allQuestions[0]
  const currentIdx = allQuestions.findIndex((q) => q.id === currentQId)
  const answeredCount = Object.values(answers).filter((a) => a?.trim()).length

  const currentSection = currentTest.sections.find((s) =>
    s.questions.some((q) => q.id === currentQId)
  )

  return (
    <>
      <TimerBar formattedTime={formattedTime} percentRemaining={percentRemaining} isWarning={isWarning} />

      <div className="flex gap-6 pt-16 min-h-screen">
        {/* Sidebar */}
        <aside className="hidden lg:block w-52 shrink-0">
          <div className="sticky top-20 card p-4">
            <p className="text-xs font-semibold text-gray-500 mb-4">
              {answeredCount}/{allQuestions.length} answered
            </p>
            <QuestionNav
              sections={currentTest.sections}
              answers={answers}
              currentQId={currentQId}
              onJump={setCurrentQId}
            />
            <div className="mt-4 pt-4 border-t border-gray-100 space-y-1 text-xs text-gray-400">
              <div className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-green-500 inline-block"/> Answered</div>
              <div className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-brand-600 inline-block"/> Current</div>
              <div className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-gray-100 inline-block"/> Unanswered</div>
            </div>
          </div>
        </aside>

        {/* Question area */}
        <main className="flex-1 max-w-2xl pb-24">
          {/* Section header */}
          <div className="bg-brand-900 text-white px-5 py-3 rounded-xl mb-5 flex items-center justify-between">
            <span className="font-semibold">{currentSection?.name}</span>
            <span className="text-brand-200 text-sm">{currentSection?.description}</span>
          </div>

          {/* Question card */}
          {currentQ && (
            <div className="card mb-5">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <span className="badge badge-blue text-xs mb-2">{currentQ.topic}</span>
                  <p className="text-xs text-gray-400">{currentQ.difficulty} · {currentQ.marks} mark{currentQ.marks !== 1 ? 's' : ''}</p>
                </div>
                <span className="shrink-0 text-xs text-gray-500">Q{currentIdx + 1}/{allQuestions.length}</span>
              </div>

              <p className="text-gray-800 font-medium leading-relaxed mb-6 text-base select-none">
                {currentQ.question}
              </p>

              {/* MCQ */}
              {currentQ.type === 'mcq' && currentQ.options && (
                <div className="space-y-3">
                  {currentQ.options.map((opt) => (
                    <button
                      key={opt.label}
                      onClick={() => setAnswer(currentQ.id, opt.label)}
                      className={`w-full text-left px-4 py-3 rounded-xl border-2 transition-all text-sm
                        ${answers[currentQ.id] === opt.label
                          ? 'border-brand-600 bg-brand-50 text-brand-700 font-medium'
                          : 'border-gray-200 hover:border-brand-200 text-gray-700'}`}
                    >
                      <span className="font-bold mr-2">{opt.label}.</span> {opt.text}
                    </button>
                  ))}
                </div>
              )}

              {/* Short / Long answer */}
              {(currentQ.type === 'short_answer' || currentQ.type === 'long_answer' || currentQ.type === 'case_based') && (
                <textarea
                  value={answers[currentQ.id] || ''}
                  onChange={(e) => setAnswer(currentQ.id, e.target.value)}
                  placeholder={`Write your answer here… (~${currentQ.marks * 30} words for full marks)`}
                  rows={currentQ.type === 'long_answer' ? 8 : 4}
                  className="input-field resize-none text-sm leading-relaxed"
                />
              )}

              {currentQ.hint && (
                <details className="mt-3">
                  <summary className="text-xs text-brand-600 cursor-pointer hover:text-brand-700">💡 Show hint</summary>
                  <p className="text-xs text-gray-500 mt-2 pl-4">{currentQ.hint}</p>
                </details>
              )}
            </div>
          )}

          {/* Navigation */}
          <div className="flex gap-3">
            <button
              onClick={() => setCurrentQId(allQuestions[currentIdx - 1]?.id)}
              disabled={currentIdx === 0}
              className="btn-ghost"
            >
              ← Prev
            </button>
            <button
              onClick={() => setCurrentQId(allQuestions[currentIdx + 1]?.id)}
              disabled={currentIdx === allQuestions.length - 1}
              className="btn-secondary flex-1"
            >
              Save & Next →
            </button>
            <button onClick={() => setShowSubmitModal(true)} className="btn-primary">
              Submit
            </button>
          </div>
        </main>
      </div>

      {/* Submit modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-8 max-w-sm w-full shadow-xl">
            <h2 className="text-xl font-bold text-gray-800 mb-2">Submit Test?</h2>
            <p className="text-gray-500 text-sm mb-4">
              You have answered <strong>{answeredCount}</strong> of <strong>{allQuestions.length}</strong> questions.
              {answeredCount < allQuestions.length && (
                <span className="text-red-600"> {allQuestions.length - answeredCount} questions unanswered.</span>
              )}
            </p>
            <p className="text-xs text-gray-400 mb-6">This cannot be undone. Your answers will be sent for AI evaluation.</p>
            <div className="flex gap-3">
              <button onClick={() => setShowSubmitModal(false)} className="btn-ghost flex-1">Cancel</button>
              <button onClick={() => handleSubmit(false)} disabled={submitting} className="btn-primary flex-1">
                {submitting ? <Spinner size="sm" className="mx-auto" /> : 'Yes, Submit →'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
