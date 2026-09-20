/**
 * Segmentation Page - Run K-Means clustering and view segment analytics.
 */
import { useState, useEffect } from 'react'
import { Play, RefreshCw, Users } from 'lucide-react'
import { Bar, Doughnut } from 'react-chartjs-2'
import api from '../../services/api'
import toast from 'react-hot-toast'

export default function SegmentationPage() {
  const [numClusters, setNumClusters] = useState(4)
  const [result, setResult] = useState(null)
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [vizData, setVizData] = useState(null)

  useEffect(() => {
    fetchSummary()
  }, [])

  const fetchSummary = async () => {
    try {
      const [sumRes, vizRes] = await Promise.all([
        api.get('/segmentation/summary').catch(() => ({ data: { segments: {} } })),
        api.get('/segmentation/visualize-data').catch(() => ({ data: { scatter_data: [] } })),
      ])
      setSummary(sumRes.data)
      setVizData(vizRes.data)
    } catch (e) {}
  }

  const runSegmentation = async () => {
    setLoading(true)
    try {
      const res = await api.post('/segmentation/run', { num_clusters: numClusters })
      setResult(res.data)
      toast.success(`Segmentation complete! Silhouette: ${res.data.silhouette_score}`)
      fetchSummary()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Segmentation failed')
    } finally {
      setLoading(false)
    }
  }

  const segments = result?.segment_centers || []
  const distribution = result?.cluster_distribution || {}

  const distChartData = {
    labels: Object.keys(distribution),
    datasets: [{
      data: Object.values(distribution),
      backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'],
      borderWidth: 0,
    }],
  }

  const segmentDetails = summary?.segments || {}
  const segmentBarData = {
    labels: Object.keys(segmentDetails),
    datasets: [
      {
        label: 'Avg Total Charges',
        data: Object.values(segmentDetails).map(s => s.avg_total_charges),
        backgroundColor: '#3b82f6',
      },
      {
        label: 'Avg CLV',
        data: Object.values(segmentDetails).map(s => s.avg_clv_score),
        backgroundColor: '#10b981',
      },
    ],
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Customer Segmentation</h1>
        <p className="text-gray-500">K-Means clustering to identify customer groups</p>
      </div>

      {/* Controls */}
      <div className="card flex flex-wrap items-center gap-4">
        <div>
          <label className="label">Number of Clusters</label>
          <select value={numClusters} onChange={(e) => setNumClusters(parseInt(e.target.value))} className="input-field w-32">
            {[2, 3, 4, 5, 6].map(n => <option key={n} value={n}>{n} Clusters</option>)}
          </select>
        </div>
        <button onClick={runSegmentation} disabled={loading} className="btn-primary flex items-center gap-2 mt-5">
          <Play className="w-4 h-4" /> {loading ? 'Running...' : 'Run Segmentation'}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="stat-card text-center">
            <p className="text-sm text-gray-500">Total Customers</p>
            <p className="text-2xl font-bold">{result.total_customers}</p>
          </div>
          <div className="stat-card text-center">
            <p className="text-sm text-gray-500">Silhouette Score</p>
            <p className="text-2xl font-bold text-green-600">{result.silhouette_score}</p>
          </div>
          <div className="stat-card text-center">
            <p className="text-sm text-gray-500">Clusters Formed</p>
            <p className="text-2xl font-bold text-primary-600">{result.num_clusters}</p>
          </div>
        </div>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Segment Distribution</h3>
          <div className="h-64">
            {Object.keys(distribution).length > 0 ? (
              <Doughnut data={distChartData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }} />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-400">Run segmentation first</div>
            )}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Segment Comparison</h3>
          <div className="h-64">
            {Object.keys(segmentDetails).length > 0 ? (
              <Bar data={segmentBarData} options={{ responsive: true, maintainAspectRatio: false }} />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-400">Run segmentation first</div>
            )}
          </div>
        </div>
      </div>

      {/* Segment Details Table */}
      {Object.keys(segmentDetails).length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Segment Details</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Segment</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Count</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Avg Tenure</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Avg Monthly</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Avg Total</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Avg Churn</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Avg CLV</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(segmentDetails).map(([name, stats], i) => (
                  <tr key={i} className="border-t border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 font-medium">{name}</td>
                    <td className="py-3 px-4">{stats.count}</td>
                    <td className="py-3 px-4">{stats.avg_tenure_months} mo</td>
                    <td className="py-3 px-4">${stats.avg_monthly_charges}</td>
                    <td className="py-3 px-4">${stats.avg_total_charges.toLocaleString()}</td>
                    <td className="py-3 px-4">{(stats.avg_churn_probability * 100).toFixed(1)}%</td>
                    <td className="py-3 px-4">${stats.avg_clv_score.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Scatter visualization placeholder */}
      {vizData?.scatter_data?.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">
            <Users className="w-5 h-5 inline mr-2" />
            Customer Scatter (Tenure vs Monthly Charges)
          </h3>
          <div className="h-96 bg-gray-50 rounded-lg relative overflow-hidden">
            {(() => {
              const data = vizData.scatter_data
              const maxX = Math.max(...data.map(d => d.x)) || 1
              const maxY = Math.max(...data.map(d => d.y)) || 1
              const colors = { 'High Value Customers': '#3b82f6', 'Frequent Buyers': '#10b981', 'Occasional Buyers': '#f59e0b', 'At-Risk Customers': '#ef4444' }
              return data.map((d, i) => (
                <div
                  key={i}
                  className="absolute w-2 h-2 rounded-full opacity-70 hover:opacity-100 transition-opacity"
                  style={{
                    left: `${(d.x / maxX) * 95 + 2}%`,
                    bottom: `${(d.y / maxY) * 95 + 2}%`,
                    backgroundColor: colors[d.segment] || '#8b5cf6',
                  }}
                  title={`${d.segment} (Tenure: ${d.x}, Charges: $${d.y})`}
                />
              ))
            })()}
            {/* Legend */}
            <div className="absolute bottom-2 right-2 bg-white p-2 rounded-lg shadow text-xs space-y-1">
              {Object.entries({ 'High Value': '#3b82f6', 'Frequent': '#10b981', 'Occasional': '#f59e0b', 'At-Risk': '#ef4444' }).map(([label, color]) => (
                <div key={label} className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color }}></div>
                  <span>{label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
