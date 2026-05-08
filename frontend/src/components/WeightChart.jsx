import ReactApexChart from 'react-apexcharts'


export default function WeightChart({ weightLogs, doses, dosePeriods, showTrend }) {
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
      text: `${dose.medication_name[0]} · ${dose.dose}${dose.unit}`,
      orientation: 'vertical',
      style: { color: '#fff', background: '#f97316' },
      position: 'top',
    },
  }))

  // Build one straight trend line series per dose period
  const trendSeries = (showTrend && dosePeriods)
    ? dosePeriods.map(period => {
        const startTs = new Date(period.start_date).getTime()
        const endTs = new Date(period.end_date).getTime()
        const totalWeeks = (endTs - startTs) / (1000 * 60 * 60 * 24 * 7)
        const endWeight = period.intercept + period.slope_kg_per_week * totalWeeks
        return {
          name: `${period.dose}mg trend`,
          data: [
            { x: startTs, y: Math.round(period.intercept * 10) / 10 },
            { x: endTs, y: Math.round(endWeight * 10) / 10 },
          ],
        }
      })
    : []

  const allSeries = [
    { name: 'Weight (kg)', data: weightData },
    ...trendSeries,
  ]

  const options = {
    chart: {
      type: 'line',
      background: 'transparent',
      toolbar: { show: false },
    },
    theme: { mode: 'dark' },
    stroke: {
      curve: ['smooth', ...Array(trendSeries.length).fill('straight')],
      width: [2, ...Array(trendSeries.length).fill(2)],
      dashArray: [0, ...Array(trendSeries.length).fill(5)],
    },
    markers: {
      size: [3, ...Array(trendSeries.length).fill(0)],
    },
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
    colors: ['#6366f1', ...Array(trendSeries.length).fill('#ffffff')],
    legend: { show: trendSeries.length > 0 },
  }

  const series = allSeries

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
