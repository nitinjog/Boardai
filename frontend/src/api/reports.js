import client from './client'

export const getReport = (testId) => client.get(`/reports/test/${testId}`).then(r => r.data)
export const downloadReportPdf = (reportId) =>
  client.get(`/reports/${reportId}/download-pdf`, { responseType: 'blob' }).then(r => r.data)
export const getStudentHistory = (studentId) =>
  client.get(`/reports/student/${studentId}`).then(r => r.data)
