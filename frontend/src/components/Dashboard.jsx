import { useEffect, useState } from 'react'
import { getWeightLogs, getMedications, getMedicationDoses, getUser, getStats, resetData } from '../api'
import WeightChart from './WeightChart'
import Onboarding from './Onboarding'

export default function Dashboard() {
  const [user, setUser] = useState(null)
  const [weightLogs, setWeightLogs] = useState([])
  const [doses, setDoses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [statsData, setStatsData] = useState(null)
  const [showTrend, setShowTrend] = useState(true)
  const [showWeight, setShowWeight] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const userData = await getUser()
        setUser(userData)

        if (!userData) return

        const logs = await getWeightLogs()
        setWeightLogs(logs)

        const medications = await getMedications()
        if (medications.length > 0) {
          const allDoses = []
          for (const med of medications) {
            const doses = await getMedicationDoses(med.id)
            doses.forEach(dose => allDoses.push({ ...dose, medication_name: med.name }))
          }
          setDoses(allDoses)
        }

        const s = await getStats()
        setStatsData(s)

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
  const stats = user && latestLog && firstLog && statsData ? (() => {
    const totalChange = latestLog.weight_kg - firstLog.weight_kg
    const pctLost = (totalChange / firstLog.weight_kg) * 100
    const heightM = user.height / 100
    const bmi = latestLog.weight_kg / (heightM * heightM)
    const toGoal = latestLog.weight_kg - user.target_weight

    const firstDate = new Date(firstLog.date)
    const lastDate = new Date(latestLog.date)
    const weeks = (lastDate - firstDate) / (1000 * 60 * 60 * 24 * 7)
    const weeklyAvg = totalChange / weeks
    const weeksToGoal = toGoal / Math.abs(statsData.dose_periods.at(-1).slope_kg_per_week)
    const projectedGoalDate = new Date(lastDate.getTime() + weeksToGoal * 7 * 24 * 60 * 60 * 1000)

    return { totalChange, pctLost, bmi, toGoal, weeklyAvg, projectedGoalDate }
  })() : null

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Weight Tracker</h1>
        <button
          onClick={async () => { await resetData(); window.location.reload() }}
          style={{
            background: '#374151',
            color: '#9ca3af',
            border: 'none',
            borderRadius: '0.375rem',
            padding: '0.375rem 0.75rem',
            cursor: 'pointer',
            fontSize: '0.75rem',
          }}
        >
          Reset data
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: '#ef4444' }}>Error: {error}</p>}

      {!loading && !error && (
        <>
          {!user && <Onboarding onComplete={() => window.location.reload()} />}
          {user && latestLog && (<>
            <div style={{ marginBottom: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {firstLog && <Stat label="Start date" value={new Date(firstLog.date).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })} />}
              {firstLog && <Stat label="Starting weight" value={`${firstLog.weight_kg} kg`} />}
              <Stat label="Latest weight" value={`${latestLog.weight_kg} kg`} />
              {user && <Stat label="Goal weight" value={`${user.target_weight} kg`} />}
              {stats && <>
                <Stat label="Total change" value={`${stats.totalChange.toFixed(1)} kg`} />
                <Stat label="% lost" value={`${Math.abs(stats.pctLost).toFixed(1)}%`} />
                <Stat label="Current BMI" value={stats.bmi.toFixed(1)} />
                <Stat label="Weekly avg" value={`${stats.weeklyAvg.toFixed(2)} kg`} />
                <Stat label="To goal" value={`${stats.toGoal.toFixed(1)} kg`} />
              </>}
              {statsData && (
                <Stat
                  label={`Rate on ${statsData.dose_periods.at(-1).dose}mg`}
                  value={`${statsData.dose_periods.at(-1).slope_kg_per_week} kg/wk`}
                />
              )}
              {stats && (
                <Stat label="Projected goal" value={stats.projectedGoalDate.toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric'})} />
              )}
            </div>

          <div style={{
            background: '#1f2937',
            borderRadius: '0.75rem',
            padding: '1.5rem',
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <div>
                <h2 style={{ margin: 0, fontSize: '1rem', color: '#d1d5db' }}>Weight over time</h2>
                <p style={{ margin: '0.25rem 0 0', fontSize: '0.75rem', color: '#6b7280' }}>
                  Weight loss medication dose changes shown as orange markers
                </p>
                {doses.length > 0 && (
                  <p style={{ margin: '0.25rem 0 0', fontSize: '0.7rem', color: '#4b5563' }}>
                    {[...new Set(doses.map(d => d.medication_name))].map(name => `${name[0]} = ${name}`).join('  ·  ')}
                  </p>
                )}
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <button
                  onClick={() => setShowTrend(t => !t)}
                  style={{
                    background: showTrend ? '#6366f1' : '#374151',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '0.375rem',
                    padding: '0.375rem 0.75rem',
                    cursor: 'pointer',
                    fontSize: '0.75rem',
                  }}
                >
                  {showTrend ? 'Hide trend lines' : 'Show trend lines'}
                </button>
                <button
                  onClick={() => setShowWeight(t => !t)}
                  style={{
                    background: showWeight ? '#6366f1' : '#374151',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '0.375rem',
                    padding: '0.375rem 0.75rem',
                    cursor: 'pointer',
                    fontSize: '0.75rem',
                  }}
                >
                  {showWeight ? 'Hide weight line' : 'Show weight line'}
                </button>
              </div>
            </div>
            <WeightChart
              weightLogs={weightLogs}
              doses={doses}
              dosePeriods={statsData?.dose_periods}
              showTrend={showTrend}
              showWeight={showWeight}
            />
          </div>
          </>)}
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
