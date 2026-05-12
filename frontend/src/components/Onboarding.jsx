import { useState } from 'react'
import { uploadCSV } from '../api'

export default function Onboarding({ onComplete }) {
  const [userFile, setUserFile] = useState(null)
  const [weightFile, setWeightFile] = useState(null)
  const [dosesFile, setDosesFile] = useState(null)

  async function onSubmit() {
    if (!userFile || !weightFile) {
      alert('Please select at least user.csv and weight_log.csv')
      return
    }
    try {
      await uploadCSV('upload/user', userFile)
      await uploadCSV('upload/weight-logs', weightFile)
      if (dosesFile) await uploadCSV('upload/medication-doses', dosesFile)
      onComplete()
    } catch (err) {
      alert('Upload failed: ' + err.message)
    }
  }


  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '0.5rem' }}>Welcome to Weight Tracker</h1>
      <p style={{ color: '#9ca3af', marginBottom: '2rem' }}>Upload your data to get started</p>
      
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="userFile" style={{ display: 'block', marginBottom: '0.25rem', color: '#d1d5db' }}>User data (user.csv)</label>
        <input type="file" id="userFile" accept=".csv" onChange={e => setUserFile(e.target.files[0])} />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="weightFile" style={{ display: 'block', marginBottom: '0.25rem', color: '#d1d5db' }}>Weight log (weight_log.csv)</label>
        <input type="file" id="weightFile" accept=".csv" onChange={e => setWeightFile(e.target.files[0])} />
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <label htmlFor="dosesFile" style={{ display: 'block', marginBottom: '0.25rem', color: '#d1d5db' }}>Medication doses (medication_doses.csv)</label>
        <input type="file" id="dosesFile" accept=".csv" onChange={e => setDosesFile(e.target.files[0])} />
      </div>

      <button onClick={onSubmit}>Upload & Get Started</button>




    </div>
  )
}