import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createStudent } from '../../api/students'
import useStudentStore from '../../store/useStudentStore'
import { SUBJECTS_BY_CLASS, SUBJECT_ICONS } from '../../constants/subjects'
import Spinner from '../../components/ui/Spinner'

export default function OnboardingPage() {
  const navigate = useNavigate()
  const { setStudent } = useStudentStore()

  const [step, setStep] = useState(1)
  const [name, setName] = useState('')
  const [classLevel, setClassLevel] = useState(null)
  const [subjects, setSubjects] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const availableSubjects = SUBJECTS_BY_CLASS[classLevel] || []

  const toggleSubject = (s) =>
    setSubjects((prev) => prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s])

  const handleSubmit = async () => {
    if (!name.trim()) return setError('Please enter your name')
    if (!classLevel) return setError('Please select your class')
    if (subjects.length === 0) return setError('Please select at least one subject')

    setLoading(true)
    setError('')
    try {
      const student = await createStudent({ name: name.trim(), class_level: classLevel, subjects })
      setStudent(student)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-50 to-white flex items-center justify-center p-6">
      <div className="w-full max-w-lg">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-brand-600 rounded-xl flex items-center justify-center text-white font-bold text-xl mx-auto mb-3">B</div>
          <h1 className="text-2xl font-bold text-brand-900">Welcome to BoardAI</h1>
          <p className="text-gray-500 text-sm mt-1">Set up your profile to get started</p>
        </div>

        {/* Step indicator */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {[1, 2, 3].map((s) => (
            <div key={s} className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-all
                ${step >= s ? 'bg-brand-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
                {step > s ? '✓' : s}
              </div>
              {s < 3 && <div className={`w-12 h-0.5 ${step > s ? 'bg-brand-600' : 'bg-gray-200'}`} />}
            </div>
          ))}
        </div>

        <div className="card shadow-lg animate-fade-in">
          {/* Step 1: Name */}
          {step === 1 && (
            <div>
              <h2 className="section-title">What's your name?</h2>
              <p className="text-gray-500 text-sm mb-6">We'll use this to personalise your tests and reports.</p>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && name.trim() && setStep(2)}
                placeholder="Enter your full name"
                className="input-field text-base mb-6"
                autoFocus
              />
              <button
                onClick={() => { if (!name.trim()) setError('Please enter your name'); else { setError(''); setStep(2) } }}
                className="btn-primary w-full"
              >
                Continue →
              </button>
            </div>
          )}

          {/* Step 2: Class */}
          {step === 2 && (
            <div>
              <h2 className="section-title">Which class are you in?</h2>
              <p className="text-gray-500 text-sm mb-6">BoardAI supports CBSE Class 10 and Class 12 syllabi.</p>
              <div className="grid grid-cols-2 gap-4 mb-6">
                {[10, 12].map((cls) => (
                  <button
                    key={cls}
                    onClick={() => { setClassLevel(cls); setSubjects([]) }}
                    className={`p-6 rounded-xl border-2 text-center transition-all
                      ${classLevel === cls
                        ? 'border-brand-600 bg-brand-50 text-brand-700'
                        : 'border-gray-200 hover:border-brand-300 text-gray-600'}`}
                  >
                    <div className="text-3xl font-bold mb-1">{cls}</div>
                    <div className="text-sm font-medium">Class {cls}</div>
                    <div className="text-xs text-gray-400 mt-1">
                      {cls === 10 ? 'Board Exam 2025' : 'Board Exam 2025'}
                    </div>
                  </button>
                ))}
              </div>
              <div className="flex gap-3">
                <button onClick={() => setStep(1)} className="btn-ghost flex-1">← Back</button>
                <button
                  onClick={() => { if (!classLevel) setError('Please select a class'); else { setError(''); setStep(3) } }}
                  className="btn-primary flex-1"
                >
                  Continue →
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Subjects */}
          {step === 3 && (
            <div>
              <h2 className="section-title">Select your subjects</h2>
              <p className="text-gray-500 text-sm mb-6">Choose the subjects you want mock tests for. You can select multiple.</p>
              <div className="grid grid-cols-2 gap-3 mb-6">
                {availableSubjects.map((s) => (
                  <button
                    key={s}
                    onClick={() => toggleSubject(s)}
                    className={`p-3 rounded-xl border-2 text-left transition-all flex items-center gap-2
                      ${subjects.includes(s)
                        ? 'border-brand-600 bg-brand-50'
                        : 'border-gray-200 hover:border-brand-300'}`}
                  >
                    <span className="text-xl">{SUBJECT_ICONS[s] || '📚'}</span>
                    <span className={`text-sm font-medium ${subjects.includes(s) ? 'text-brand-700' : 'text-gray-700'}`}>
                      {s}
                    </span>
                    {subjects.includes(s) && <span className="ml-auto text-brand-600 text-sm">✓</span>}
                  </button>
                ))}
              </div>
              <p className="text-xs text-gray-400 mb-4 text-center">
                {subjects.length} subject{subjects.length !== 1 ? 's' : ''} selected
              </p>
              <div className="flex gap-3">
                <button onClick={() => setStep(2)} className="btn-ghost flex-1">← Back</button>
                <button onClick={handleSubmit} disabled={loading || subjects.length === 0} className="btn-primary flex-1">
                  {loading ? <Spinner size="sm" className="mx-auto" /> : 'Create My Profile →'}
                </button>
              </div>
            </div>
          )}

          {error && (
            <p className="text-red-600 text-sm mt-4 text-center">{error}</p>
          )}
        </div>
      </div>
    </div>
  )
}
