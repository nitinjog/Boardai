import client from './client'

export const startDiagnostic = (studentId, subject) =>
  client.post('/diagnostics/start', { student_id: studentId, subject }).then(r => r.data)

export const submitDiagnostic = (sessionId, responses) =>
  client.post('/diagnostics/submit', { session_id: sessionId, responses }).then(r => r.data)

export const getDiagnosticHistory = (studentId) =>
  client.get(`/diagnostics/student/${studentId}`).then(r => r.data)
