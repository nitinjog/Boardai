import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getTest, downloadTestPdf } from '../../api/tests'
import Spinner from '../../components/ui/Spinner'
import ErrorMessage from '../../components/shared/ErrorMessage'

export default function TestModePage() {
  const { testId } = useParams()
  const navigate = useNavigate()
  const [test, setTest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [pdfLoading, setPdfLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    getTest(testId)
      .then(setTest)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [testId])

  const handleDownloadPdf = async () => {
    setPdfLoading(true)
    try {
      const blob = await downloadTestPdf(testId)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `BoardAI_MockTest_${test.subject}_${testId.slice(0, 8)}.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      setError(e.message)
    } finally {
      setPdfLoading(false)
    }
  }

  if (loading) return <div className="flex justify-center py-20"><Spinner size="lg" /></div>
  if (error) return <ErrorMessage message={error} />
  if (!test) return null

  const totalQuestions = test.sections.reduce((s, sec) => s + sec.questions.length, 0)

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <div className="card mb-6 text-center">
        <div className="inline-flex items-center gap-2 bg-green-100 text-green-700 text-sm font-medium px-4 py-2 rounded-full mb-4">
          ✅ Test Generated Successfully
        </div>
        <h1 className="text-2xl font-bold text-gray-800 mb-1">{test.subject} Mock Test</h1>
        <p className="text-gray-500">Class {test.class_level} · {test.total_marks} Marks · {test.duration_minutes} Minutes</p>

        <div className="grid grid-cols-3 gap-4 mt-6 mb-2">
          <div className="text-center p-3 bg-gray-50 rounded-xl">
            <div className="text-xl font-bold text-brand-600">{test.sections.length}</div>
            <div className="text-xs text-gray-500">Sections</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-xl">
            <div className="text-xl font-bold text-brand-600">{totalQuestions}</div>
            <div className="text-xs text-gray-500">Questions</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-xl">
            <div className="text-xl font-bold text-brand-600">{test.total_marks}</div>
            <div className="text-xs text-gray-500">Total Marks</div>
          </div>
        </div>
      </div>

      <p className="text-center font-semibold text-gray-700 mb-6">Choose how you'd like to attempt the test:</p>

      <div className="grid sm:grid-cols-2 gap-4">
        {/* Online mode */}
        <div className="card hover:shadow-md transition-shadow border-2 border-brand-200">
          <div className="text-3xl mb-3">💻</div>
          <h2 className="text-lg font-bold text-gray-800 mb-2">Take Online</h2>
          <ul className="text-sm text-gray-500 space-y-1 mb-6">
            <li>⏱️ Built-in countdown timer</li>
            <li>💾 Answers auto-saved</li>
            <li>📊 Instant AI evaluation</li>
            <li>🔒 Basic anti-cheat controls</li>
          </ul>
          <button onClick={() => navigate(`/test/${testId}/attempt`)} className="btn-primary w-full">
            Start Now →
          </button>
        </div>

        {/* Offline mode */}
        <div className="card hover:shadow-md transition-shadow border-2 border-gray-200">
          <div className="text-3xl mb-3">📄</div>
          <h2 className="text-lg font-bold text-gray-800 mb-2">Download PDF</h2>
          <ul className="text-sm text-gray-500 space-y-1 mb-6">
            <li>🖨️ Print and write by hand</li>
            <li>📸 Upload a scan after</li>
            <li>🤖 Same AI evaluation</li>
            <li>✏️ Pen & paper practice</li>
          </ul>
          <button onClick={handleDownloadPdf} disabled={pdfLoading} className="btn-secondary w-full">
            {pdfLoading ? <Spinner size="sm" className="mx-auto" /> : 'Download PDF →'}
          </button>
          {!pdfLoading && (
            <button
              onClick={() => navigate(`/test/${testId}/upload`)}
              className="btn-ghost w-full text-sm mt-2"
            >
              Already have answers? Upload scan →
            </button>
          )}
        </div>
      </div>

      {error && <p className="text-red-600 text-sm mt-4 text-center">{error}</p>}
    </div>
  )
}
