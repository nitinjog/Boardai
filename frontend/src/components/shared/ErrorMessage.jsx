export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="rounded-xl bg-red-50 border border-red-200 p-6 text-center max-w-md mx-auto mt-8">
      <div className="text-3xl mb-3">⚠️</div>
      <p className="text-red-700 font-medium mb-1">Something went wrong</p>
      <p className="text-red-600 text-sm mb-4">{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="btn-primary text-sm">
          Try Again
        </button>
      )}
    </div>
  )
}
