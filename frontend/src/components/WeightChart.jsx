import ReactApexChart from 'react-apexcharts'

export default function WeightChart({ weightLogs, doses }) {
  // Build the weight data series — ApexCharts wants [timestamp, value] pairs
  const weightData = weightLogs
    .filter(log => log.weight_kg !== null)
    .map(log => ({
      x: new Date(log.date).getTime(),
      y: log.weight_kg,
    }))

  // Build dose change annotations — vertical lines on the chart
  const annotations = doses.map(dose => ({
    x: new Date(dose.date_changed).getTime(),
    borderColor: '#f97316',
    strokeDashArray: 4,
    label: {
      text: `${dose.dose}${dose.unit}`,
      style: { color: '#fff', background: '#f97316' },
      position: 'top',
    },
  }))

  const options = {
    chart: {
      type: 'line',
      background: 'transparent',
      toolbar: { show: false },
    },
    theme: { mode: 'dark' },
    stroke: { curve: 'smooth', width: 2 },
    markers: { size: 3 },
    xaxis: {
      type: 'datetime',
      labels: { datetimeUTC: false },
    },
    yaxis: {
      title: { text: 'Weight (kg)' },
      decimalsInFloat: 1,
    },
    annotations: { xaxis: annotations },
    tooltip: {
      x: { format: 'dd MMM yyyy' },
    },
    colors: ['#6366f1'],
  }

  const series = [{ name: 'Weight (kg)', data: weightData }]

  if (weightData.length === 0) {
    return <p style={{ color: '#9ca3af' }}>No weight data yet.</p>
  }

  return (
    <ReactApexChart
      options={options}
      series={series}
      type="line"
      height={400}
    />
  )
}
