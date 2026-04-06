import client from './client'

export const generateTest = (data) => client.post('/tests/generate', data).then(r => r.data)
export const getTest = (testId) => client.get(`/tests/${testId}`).then(r => r.data)
export const startTest = (testId) => client.post(`/tests/${testId}/start`).then(r => r.data)
export const submitTest = (testId, payload) => client.post(`/tests/${testId}/submit`, payload).then(r => r.data)
export const getStudentTests = (studentId) => client.get(`/tests/student/${studentId}`).then(r => r.data)
export const downloadTestPdf = (testId) =>
  client.get(`/tests/${testId}/download-pdf`, { responseType: 'blob' }).then(r => r.data)
