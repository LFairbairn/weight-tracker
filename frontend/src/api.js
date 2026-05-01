const BASE = '/api'

export async function getUser() {
  const res = await fetch(`${BASE}/users/me`)
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
