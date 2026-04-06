import client from './client'

export const createStudent = (data) => client.post('/students', data).then(r => r.data)
export const getStudent = (id) => client.get(`/students/${id}`).then(r => r.data)
