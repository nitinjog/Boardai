import Spinner from '../ui/Spinner'

export default function LoadingOverlay({ message = 'Please wait…' }) {
  return (
    <div className="fixed inset-0 bg-white/80 backdrop-blur-sm z-50 flex flex-col items-center justify-center gap-4">
      <Spinner size="lg" />
      <p className="text-gray-600 font-medium animate-pulse">{message}</p>
    </div>
  )
}
