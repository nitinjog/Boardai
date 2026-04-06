import { useEffect, useRef, useState, useCallback } from 'react'

export function useTimer(initialSeconds, onExpire) {
  const [timeRemaining, setTimeRemaining] = useState(null)
  const onExpireRef = useRef(onExpire)

  // Keep onExpire ref current without restarting the timer
  useEffect(() => { onExpireRef.current = onExpire }, [onExpire])

  // Initialise as soon as duration arrives from API
  useEffect(() => {
    if (initialSeconds > 0) {
      setTimeRemaining(initialSeconds)
    }
  }, [initialSeconds])

  // Countdown — use setTimeout so each tick is self-contained
  useEffect(() => {
    if (timeRemaining === null || timeRemaining <= 0) {
      if (timeRemaining === 0) onExpireRef.current?.()
      return
    }
    const id = setTimeout(() => setTimeRemaining((t) => Math.max(0, t - 1)), 1000)
    return () => clearTimeout(id)
  }, [timeRemaining])

  const format = useCallback((secs) => {
    if (secs === null) return '--:--'
    const h = Math.floor(secs / 3600)
    const m = Math.floor((secs % 3600) / 60)
    const s = secs % 60
    if (h > 0) return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
  }, [])

  return {
    timeRemaining,
    formattedTime: format(timeRemaining),
    isWarning: timeRemaining !== null && initialSeconds > 0 && timeRemaining < initialSeconds * 0.2,
    isExpired: timeRemaining !== null && timeRemaining <= 0,
    percentRemaining:
      initialSeconds > 0 && timeRemaining !== null
        ? Math.max(0, (timeRemaining / initialSeconds) * 100)
        : 100,
  }
}
