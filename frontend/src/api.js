const BASE = '/api'

export async function getUser() {
  const res = await fetch(`${BASE}/users/me`)
  if(res.status === 404) return null
  if (!res.ok) throw new Error('Failed to fetch user')
  return res.json()
}

export async function getWeightLogs() {
  const res = await fetch(`${BASE}/weight-logs`)
  if (!res.ok) throw new Error('Failed to fetch weight logs')
  return res.json()
}

export async function getMedications() {
  const res = await fetch(`${BASE}/medications`)
  if (!res.ok) throw new Error('Failed to fetch medications')
  return res.json()
}

export async function getMedicationDoses(medicationId) {
  const res = await fetch(`${BASE}/medications/${medicationId}/doses`)
  if (!res.ok) throw new Error('Failed to fetch doses')
  return res.json()
}

export async function getStats() {
  const res = await fetch(`${BASE}/stats`)
  if (!res.ok) throw new Error('Failed to fetch stats')
  return res.json()
}

export async function uploadCSV(endpoint, file) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${BASE}/${endpoint}`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) throw new Error(`Upload failed: ${endpoint}`)
  return res.json()
}

export async function resetData() {
  const res = await fetch(`${BASE}/upload/reset`, { method: 'POST' })
  if (!res.ok) throw new Error('Reset failed')
  return res.json()
}
