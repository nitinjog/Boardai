import { useEffect, useRef, useCallback } from 'react'
import useTestStore from '../store/useTestStore'

export function useTimer(initialSeconds, onExpire) {
  const { timeRemaining, setTimeRemaining } = useTestStore()
  const intervalRef = useRef(null)

  // Initialise when duration becomes available (API may load after mount)
  useEffect(() => {
    if (timeRemaining === null && initialSeconds > 0) {
      setTimeRemaining(initialSeconds)
    }
  }, [initialSeconds]) // eslint-disable-line

  useEffect(() => {
    if (timeRemaining === null) return
    if (timeRemaining <= 0) {
      onExpire?.()
      return
    }
    intervalRef.current = setInterval(() => {
      setTimeRemaining(Math.max(0, timeRemaining - 1))
    }, 1000)
    return () => clearInterval(intervalRef.current)
  }, [timeRemaining]) // eslint-disable-line

  const format = useCallback((secs) => {
    if (secs === null) return '--:--'
    const h = Math.floor(secs / 3600)
    const m = Math.floor((secs % 3600) / 60)
    const s = secs % 60
    if (h > 0) return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
  }, [])

  const isWarning = timeRemaining !== null && timeRemaining < initialSeconds * 0.2
  const isExpired = timeRemaining !== null && timeRemaining <= 0

  return {
    timeRemaining,
    formattedTime: format(timeRemaining),
    isWarning,
    isExpired,
    percentRemaining: initialSeconds > 0 ? Math.max(0, (timeRemaining / initialSeconds) * 100) : 0,
  }
}
