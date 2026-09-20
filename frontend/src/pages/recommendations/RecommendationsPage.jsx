/**
 * Recommendations Page - AI-powered retention and engagement recommendations.
 */
import { useState, useEffect } from 'react'
import { Lightbulb, Sparkles, Tag, Gift, Target, RefreshCw, CheckCircle, Clock, XCircle } from 'lucide-react'
import api from '../../services/api'
import toast from 'react-hot-toast'

const TYPE_ICONS = {
  Retention: Target,
  Discount: Tag,
  Loyalty: Gift,
  Upsell: Sparkles,
  'Cross-sell': Sparkles,
  'Win-back': RefreshCw,
}

const PRIORITY_COLORS = {
  Low: 'bg-blue-50 text-blue-700 border-blue-200',
  Medium: 'bg-yellow-50 text-yellow-700 border-yellow-200',
  High: 'bg-orange-50 text-orange-700 border-orange-200',
  Urgent: 'bg-red-50 text-red-700 border-red-200',
}

const STATUS_ICONS = {
  Pending: Clock,
  Shown: CheckCircle,
  Accepted: CheckCircle,
  Rejected: XCircle,
}

export default function RecommendationsPage() {
  const [customerId, setCustomerId] = useState('')
  const [recommendations, setRecommendations] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const res = await api.get('/recommendations/stats')
      setStats(res.data)
    } catch (e) {}
  }

  const generateRecommendations = async () => {
    if (!customerId) {
      toast.error('Enter a customer ID')
      return
    }
    setLoading(true)
    try {
      const res = await api.post(`/recommendations/generate/${customerId}`)
      setRecommendations(res.data)
      toast.success(`Generated ${res.data.length} recommendations!`)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate')
    } finally {
      setLoading(false)
    }
  }

  const updateStatus = async (recId, status) => {
    try {
      await api.put(`/recommendations/${recId}/status?new_status=${status}`)
      setRecommendations(prev => prev.map(r => r.id === recId ? { ...r, status } : r))
      toast.success(`Recommendation marked as ${status}`)
    } catch (error) {
      toast.error('Failed to update')
    }
  }

  const bulkGenerate = async () => {
    setLoading(true)
    try {
      const res = await api.post('/recommendations/bulk-generate')
      toast.success(res.data.message)
      fetchStats()
    } catch (error) {
      toast.error('Failed to generate in bulk')
    } finally {
      setLoading(false)
    }
  }

  const recStats = stats?.recommendation_stats || {}

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">AI Recommendations</h1>
        <p className="text-gray-500">Personalized retention strategies, discount suggestions, and loyalty programs</p>
      </div>

      {/* Controls */}
      <div className="card flex flex-wrap items-end gap-4">
        <div className="flex-1 min-w-[200px]">
          <label className="label">Customer ID</label>
          <input
            value={customerId} onChange={(e) => setCustomerId(e.target.value)}
            className="input-field" placeholder="Enter customer ID (e.g., 1)"
          />
        </div>
        <button onClick={generateRecommendations} disabled={loading} className="btn-primary flex items-center gap-2">
          <Lightbulb className="w-4 h-4" /> {loading ? 'Generating...' : 'Generate Recommendations'}
        </button>
        <button onClick={bulkGenerate} disabled={loading} className="btn-secondary flex items-center gap-2">
          <Sparkles className="w-4 h-4" /> Bulk Generate for All
        </button>
      </div>

      {/* Stats Summary */}
      {Object.keys(recStats).length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {Object.entries(recStats).map(([type, data]) => {
            const Icon = TYPE_ICONS[type] || Lightbulb
            return (
              <div key={type} className="stat-card text-center">
                <Icon className="w-6 h-6 mx-auto text-primary-500 mb-2" />
                <p className="text-xs text-gray-500">{type}</p>
                <p className="text-xl font-bold">{data.total}</p>
              </div>
            )
          })}
        </div>
      )}

      {/* Recommendations List */}
      {recommendations.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Generated Recommendations ({recommendations.length})</h3>
          {recommendations.map((rec) => {
            const Icon = TYPE_ICONS[rec.recommendation_type] || Lightbulb
            const StatusIcon = STATUS_ICONS[rec.status] || Clock

            return (
              <div key={rec.id} className={`card border-l-4 ${PRIORITY_COLORS[rec.priority]?.split(' ')[2] || 'border-gray-200'}`}>
                <div className="flex items-start justify-between">
                  <div className="flex gap-4">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${PRIORITY_COLORS[rec.priority]?.split(' ')[0] || 'bg-gray-50'}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-semibold text-gray-900">{rec.recommendation_type}</span>
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${PRIORITY_COLORS[rec.priority] || ''}`}>
                          {rec.priority}
                        </span>
                      </div>
                      <p className="text-gray-700">{rec.recommendation_text}</p>
                      <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                        {rec.discount_percentage && <span>🏷️ {rec.discount_percentage}% discount</span>}
                        {rec.loyalty_points && <span>⭐ {rec.loyalty_points} loyalty points</span>}
                        <span>Confidence: {(rec.confidence_score * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <StatusIcon className="w-4 h-4 text-gray-400" />
                    <select
                      value={rec.status}
                      onChange={(e) => updateStatus(rec.id, e.target.value)}
                      className="text-xs border rounded px-2 py-1"
                    >
                      <option>Pending</option>
                      <option>Shown</option>
                      <option>Accepted</option>
                      <option>Rejected</option>
                    </select>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {recommendations.length === 0 && !loading && (
        <div className="card text-center py-12 text-gray-400">
          <Lightbulb className="w-12 h-12 mx-auto mb-3" />
          <p>Enter a customer ID and click Generate to get AI recommendations</p>
        </div>
      )}
    </div>
  )
}
