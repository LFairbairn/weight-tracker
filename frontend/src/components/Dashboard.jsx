import { useEffect, useState } from 'react'
import { getWeightLogs, getMedications, getMedicationDoses } from '../api'
import WeightChart from './WeightChart'

export default function Dashboard() {
  const [weightLogs, setWeightLogs] = useState([])
  const [doses, setDoses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const logs = await getWeightLogs()
        setWeightLogs(logs)

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
            <div style={{ marginBottom: '2rem', display: 'flex', gap: '2rem' }}>
              <Stat label="Latest weight" value={`${latestLog.weight_kg} kg`} />
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
