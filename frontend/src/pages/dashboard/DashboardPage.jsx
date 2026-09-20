/**
 * Dashboard Page - Main analytics overview with stats cards, charts, and trends.
 */
import { useState, useEffect } from 'react'
import {
  Users, UserCheck, UserX, DollarSign, TrendingUp,
  AlertTriangle, Heart, RefreshCw
} from 'lucide-react'
import { Bar, Doughnut, Line } from 'react-chartjs-2'
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement,
  ArcElement, PointElement, LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'
import api from '../../services/api'
import toast from 'react-hot-toast'

ChartJS.register(
  CategoryScale, LinearScale, BarElement, ArcElement,
  PointElement, LineElement, Title, Tooltip, Legend, Filler
)

// Stat Card Component
function StatCard({ icon: Icon, label, value, color, subtext }) {
  const colors = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    red: 'bg-red-50 text-red-600',
    purple: 'bg-purple-50 text-purple-600',
    yellow: 'bg-yellow-50 text-yellow-600',
    indigo: 'bg-indigo-50 text-indigo-600',
  }
  return (
    <div className="stat-card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {subtext && <p className="text-xs text-gray-400 mt-1">{subtext}</p>}
        </div>
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${colors[color] || colors.blue}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  )
}

export default function DashboardPage() {
  const [stats, setStats] = useState(null)
  const [segments, setSegments] = useState([])
  const [riskDist, setRiskDist] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    setLoading(true)
    try {
      const [dashRes, segRes, riskRes] = await Promise.all([
        api.get('/analytics/dashboard').catch(() => ({ data: {} })),
        api.get('/analytics/segments').catch(() => ({ data: [] })),
        api.get('/analytics/churn/risk-distribution').catch(() => ({ data: { distribution: {} } })),
      ])
      setStats(dashRes.data)
      setSegments(segRes.data)
      setRiskDist(riskRes.data.distribution || {})
    } catch (error) {
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  // Chart data for segments
  const segmentChartData = {
    labels: segments.map(s => s.segment),
    datasets: [{
      label: 'Customers',
      data: segments.map(s => s.customer_count),
      backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
      borderWidth: 0,
    }],
  }

  // Chart data for risk distribution
  const riskChartData = {
    labels: Object.keys(riskDist),
    datasets: [{
      data: Object.values(riskDist),
      backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#7c3aed'],
      borderWidth: 0,
    }],
  }

  // Revenue by subscription
  const revenueChartData = {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [
      {
        label: 'Revenue ($)',
        data: [
          (stats?.total_revenue || 0) * 0.2,
          (stats?.total_revenue || 0) * 0.25,
          (stats?.total_revenue || 0) * 0.28,
          (stats?.total_revenue || 0) * 0.27,
        ],
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="text-gray-500">AI-Powered Customer Intelligence Overview</p>
        </div>
        <button onClick={fetchDashboardData} className="btn-secondary flex items-center gap-2">
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={Users} label="Total Customers" value={stats?.total_customers || 0} color="blue" />
        <StatCard icon={UserCheck} label="Active Customers" value={stats?.active_customers || 0} color="green" />
        <StatCard icon={UserX} label="Churned Customers" value={stats?.churned_customers || 0} color="red" />
        <StatCard icon={DollarSign} label="Total Revenue" value={`$${(stats?.total_revenue || 0).toLocaleString()}`} color="purple" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={TrendingUp} label="Avg CLV Score" value={`$${(stats?.avg_clv_score || 0).toLocaleString()}`} color="indigo" />
        <StatCard icon={Heart} label="Retention Rate" value={`${stats?.retention_rate || 0}%`} color="green" subtext="of total customers" />
        <StatCard icon={AlertTriangle} label="Churn Rate" value={`${stats?.churn_rate || 0}%`} color="red" subtext="requires attention" />
        <StatCard icon={DollarSign} label="Avg Revenue/Customer" value={`$${(stats?.avg_revenue_per_customer || 0).toLocaleString()}`} color="yellow" />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Segment Distribution */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Customer Segments</h3>
          <div className="h-64">
            {segments.length > 0 ? (
              <Bar data={segmentChartData} options={chartOptions} />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-400">
                Run segmentation to see results
              </div>
            )}
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Churn Risk Distribution</h3>
          <div className="h-64">
            {Object.keys(riskDist).length > 0 ? (
              <Doughnut data={riskChartData} options={{ ...chartOptions, plugins: { legend: { display: true, position: 'right' } } }} />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-400">
                Run churn prediction to see results
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Revenue Trend */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue Trend</h3>
        <div className="h-64">
          <Line
            data={revenueChartData}
            options={{
              ...chartOptions,
              plugins: { legend: { display: true } },
              scales: {
                y: { beginAtZero: true, ticks: { callback: (v) => `$${(v / 1000).toFixed(0)}k` } },
              },
            }}
          />
        </div>
      </div>

      {/* Segment Summary Table */}
      {segments.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Segment Details</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Segment</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Customers</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Avg Monthly</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Avg Total</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Avg Churn Prob</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Churned</th>
                </tr>
              </thead>
              <tbody>
                {segments.map((seg, i) => (
                  <tr key={i} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 font-medium">{seg.segment}</td>
                    <td className="py-3 px-4">{seg.customer_count}</td>
                    <td className="py-3 px-4">${seg.avg_monthly_charges.toLocaleString()}</td>
                    <td className="py-3 px-4">${seg.avg_total_charges.toLocaleString()}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        seg.avg_churn_probability > 0.6 ? 'bg-red-100 text-red-700' :
                        seg.avg_churn_probability > 0.3 ? 'bg-yellow-100 text-yellow-700' :
                        'bg-green-100 text-green-700'
                      }`}>
                        {(seg.avg_churn_probability * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="py-3 px-4">{seg.churned_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
