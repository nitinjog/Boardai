import { useState, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import useStudentStore from '../../store/useStudentStore'
import { uploadScan } from '../../api/evaluation'
import { ALLOWED_UPLOAD_TYPES, MAX_FILE_SIZE_MB } from '../../constants/config'
import Spinner from '../../components/ui/Spinner'
import ProgressBar from '../../components/ui/ProgressBar'

export default function UploadPage() {
  const { testId } = useParams()
  const navigate = useNavigate()
  const { student } = useStudentStore()
  const fileInputRef = useRef(null)

  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState('')

  const validateFile = (f) => {
    if (!ALLOWED_UPLOAD_TYPES.includes(f.type)) {
      return 'Invalid file type. Upload JPG, PNG, WebP, or PDF.'
    }
    if (f.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      return `File too large. Maximum size is ${MAX_FILE_SIZE_MB} MB.`
    }
    return null
  }

  const handleFileSelect = (f) => {
    const err = validateFile(f)
    if (err) { setError(err); return }
    setError('')
    setFile(f)
    if (f.type.startsWith('image/')) {
      const url = URL.createObjectURL(f)
      setPreview(url)
    } else {
      setPreview(null)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFileSelect(f)
  }

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    setProgress(0)
    setError('')

    const formData = new FormData()
    formData.append('file', file)
    formData.append('test_id', testId)
    formData.append('student_id', student.id)

    // Simulate progress for UX
    const progressInterval = setInterval(() => {
      setProgress((p) => Math.min(p + 10, 85))
    }, 500)

    try {
      await uploadScan(formData)
      clearInterval(progressInterval)
      setProgress(100)
      setTimeout(() => navigate(`/evaluate/${testId}`), 800)
    } catch (e) {
      clearInterval(progressInterval)
      setError(e.message)
      setUploading(false)
      setProgress(0)
    }
  }

  return (
    <div className="max-w-lg mx-auto animate-fade-in">
      <button onClick={() => navigate('/dashboard')} className="text-sm text-gray-500 hover:text-gray-700 mb-6">
        ← Dashboard
      </button>

      <div className="card">
        <h1 className="page-title mb-1">Upload Answer Sheet</h1>
        <p className="text-gray-500 text-sm mb-6">
          Take a clear photo or scan of your completed answer sheet and upload it below.
          Our AI will extract your answers and evaluate them.
        </p>

        {/* Instructions */}
        <div className="bg-blue-50 rounded-xl p-4 mb-6">
          <p className="text-sm font-semibold text-blue-700 mb-2">📸 Tips for a good scan:</p>
          <ul className="text-xs text-blue-600 space-y-1">
            <li>• Ensure all text is clearly visible and in focus</li>
            <li>• Use good lighting — avoid shadows</li>
            <li>• Keep the paper flat and straight</li>
            <li>• Include all pages in one PDF if writing more than one sheet</li>
          </ul>
        </div>

        {/* Drop zone */}
        <div
          onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all mb-4
            ${dragging ? 'border-brand-500 bg-brand-50' : 'border-gray-300 hover:border-brand-400 hover:bg-gray-50'}`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept={ALLOWED_UPLOAD_TYPES.join(',')}
            className="hidden"
            onChange={(e) => e.target.files[0] && handleFileSelect(e.target.files[0])}
          />
          {file ? (
            <div>
              {preview ? (
                <img src={preview} alt="Preview" className="max-h-48 mx-auto rounded-lg mb-3 object-contain" />
              ) : (
                <div className="text-4xl mb-3">📄</div>
              )}
              <p className="text-sm font-medium text-gray-700">{file.name}</p>
              <p className="text-xs text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              <button
                onClick={(e) => { e.stopPropagation(); setFile(null); setPreview(null) }}
                className="text-xs text-red-500 hover:text-red-700 mt-2"
              >
                Remove
              </button>
            </div>
          ) : (
            <div>
              <div className="text-5xl mb-4">📁</div>
              <p className="text-gray-600 font-medium mb-1">Drop your file here, or click to browse</p>
              <p className="text-xs text-gray-400">Supports JPG, PNG, WebP, PDF · Max {MAX_FILE_SIZE_MB} MB</p>
            </div>
          )}
        </div>

        {uploading && (
          <div className="mb-4">
            <ProgressBar value={progress} max={100} showPercent label={progress < 90 ? 'Uploading…' : 'Extracting answers with AI…'} />
          </div>
        )}

        {error && <p className="text-red-600 text-sm mb-4">{error}</p>}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="btn-primary w-full"
        >
          {uploading ? <Spinner size="sm" className="mx-auto" /> : '🤖 Upload & Extract Answers →'}
        </button>
      </div>
    </div>
  )
}
