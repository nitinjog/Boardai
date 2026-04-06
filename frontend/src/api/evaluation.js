import client from './client'

export const evaluateTest = (testId) => client.post(`/evaluation/evaluate/${testId}`).then(r => r.data)

export const uploadScan = (formData) =>
  client.post('/evaluation/upload-scan', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then(r => r.data)
