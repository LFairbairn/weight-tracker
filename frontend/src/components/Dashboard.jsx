import { useEffect, useState } from 'react'
import { getWeightLogs, getMedications, getMedicationDoses, getUser } from '../api'
import WeightChart from './WeightChart'

export default function Dashboard() {
  const [user, setUser] = useState(null)
  const [weightLogs, setWeightLogs] = useState([])
  const [doses, setDoses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const logs = await getWeightLogs()
        setWeightLogs(logs)

        const userData = await getUser()
        setUser(userData)

        const medications = await getMedications()
        if (medications.length > 0) {
          const allDoses = await getMedicationDoses(medications[0].id)
          setDoses(allDoses)
        }
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const latestLog = weightLogs.at(-1)
  const firstLog = weightLogs.find(l => l.weight_kg !== null)

  // Stats — only calculated when we have the data we need
  const stats = user && latestLog && firstLog ? (() => {
    const totalChange = latestLog.weight_kg - firstLog.weight_kg
    const pctLost = (totalChange / firstLog.weight_kg) * 100
    const heightM = user.height / 100
    const bmi = latestLog.weight_kg / (heightM * heightM)
    const toGoal = latestLog.weight_kg - user.target_weight

    const firstDate = new Date(firstLog.date)
    const lastDate = new Date(latestLog.date)
    const weeks = (lastDate - firstDate) / (1000 * 60 * 60 * 24 * 7)
    const weeklyAvg = totalChange / weeks

    return { totalChange, pctLost, bmi, toGoal, weeklyAvg }
  })() : null

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '0.25rem' }}>Weight Tracker</h1>
      <p style={{ color: '#9ca3af', marginBottom: '2rem' }}>
        Wegovy dose changes shown as orange markers
      </p>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: '#ef4444' }}>Error: {error}</p>}

      {!loading && !error && (
        <>
          {latestLog && (
            <div style={{ marginBottom: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {firstLog && <Stat label="Starting weight" value={`${firstLog.weight_kg} kg`} />}
              <Stat label="Latest weight" value={`${latestLog.weight_kg} kg`} />
              {stats && <>
                <Stat label="Total change" value={`${stats.totalChange.toFixed(1)} kg`} />
                <Stat label="% lost" value={`${Math.abs(stats.pctLost).toFixed(1)}%`} />
                <Stat label="Current BMI" value={stats.bmi.toFixed(1)} />
                <Stat label="Weekly avg" value={`${stats.weeklyAvg.toFixed(2)} kg`} />
                <Stat label="To goal" value={`${stats.toGoal.toFixed(1)} kg`} />
              </>}
              <Stat label="Entries" value={weightLogs.length} />
              <Stat label="Dose changes" value={doses.length} />
            </div>
          )}

          <div style={{
            background: '#1f2937',
            borderRadius: '0.75rem',
            padding: '1.5rem',
          }}>
            <h2 style={{ marginBottom: '1rem', fontSize: '1rem', color: '#d1d5db' }}>
              Weight over time
            </h2>
            <WeightChart weightLogs={weightLogs} doses={doses} />
          </div>
        </>
      )}
    </div>
  )
}

function Stat({ label, value }) {
  return (
    <div style={{
      background: '#1f2937',
      borderRadius: '0.5rem',
      padding: '1rem 1.5rem',
      minWidth: '120px',
    }}>
      <div style={{ color: '#9ca3af', fontSize: '0.75rem', marginBottom: '0.25rem' }}>
        {label}
      </div>
      <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{value}</div>
    </div>
  )
}
