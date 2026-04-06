export default function ProgressBar({ value, max = 100, label, color = 'brand', showPercent = false }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100))
  const colors = {
    brand: 'bg-brand-600',
    green: 'bg-green-500',
    yellow: 'bg-yellow-400',
    red: 'bg-red-500',
  }
  return (
    <div className="w-full">
      {(label || showPercent) && (
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          {label && <span>{label}</span>}
          {showPercent && <span>{pct.toFixed(0)}%</span>}
        </div>
      )}
      <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
        <div
          className={`h-2 rounded-full transition-all duration-500 ${colors[color] || colors.brand}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
