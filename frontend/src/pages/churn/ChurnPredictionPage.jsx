/**
 * Churn Prediction Page - Input features and get churn predictions.
 */
import { useState } from 'react'
import { AlertTriangle, Zap, TrendingDown, Info } from 'lucide-react'
import api from '../../services/api'
import toast from 'react-hot-toast'

export default function ChurnPredictionPage() {
  const [form, setForm] = useState({
    tenure_months: 12, monthly_charges: 65.0, total_charges: 780.0,
    complaints: 2, support_tickets: 5, usage_frequency: 8,
    payment_delay_days: 3, contract_type: 'Month-to-Month',
  })
  const [prediction, setPrediction] = useState(null)
  const [batchResult, setBatchResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: ['contract_type'].includes(name) ? value : parseFloat(value) || 0 }))
  }

  const predictChurn = async () => {
    setLoading(true)
    setPrediction(null)
    try {
      const res = await api.post('/churn/predict', form)
      setPrediction(res.data)
      toast.success('Prediction complete!')
    } catch (error) {
      toast.error('Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  const runBatchPrediction = async () => {
    setLoading(true)
    try {
      const res = await api.post('/churn/predict/batch')
      setBatchResult(res.data)
      toast.success(`Batch prediction complete: ${res.data.churn_count} at risk`)
    } catch (error) {
      toast.error('Batch prediction failed')
    } finally {
      setLoading(false)
    }
  }

  const riskStyle = (level) => ({
    Low: { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-700', icon: 'text-green-500' },
    Medium: { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-700', icon: 'text-yellow-500' },
    High: { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700', icon: 'text-orange-500' },
    Critical: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', icon: 'text-red-500' },
  }[level] || { bg: 'bg-gray-50', border: 'border-gray-200', text: 'text-gray-700', icon: 'text-gray-500' })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Churn Prediction</h1>
        <p className="text-gray-500">Predict customer churn using ML models (Logistic Regression, Random Forest, XGBoost)</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Info className="w-5 h-5 text-primary-500" /> Input Features
          </h3>
          <div className="grid grid-cols-2 gap-4">
            {[
              { name: 'tenure_months', label: 'Tenure (months)', min: 0, max: 72 },
              { name: 'monthly_charges', label: 'Monthly Charges ($)', min: 0, max: 200, step: 0.01 },
              { name: 'total_charges', label: 'Total Charges ($)', min: 0, max: 10000, step: 0.01 },
              { name: 'complaints', label: 'Complaints', min: 0, max: 20 },
              { name: 'support_tickets', label: 'Support Tickets', min: 0, max: 30 },
              { name: 'usage_frequency', label: 'Usage Frequency', min: 0, max: 30 },
              { name: 'payment_delay_days', label: 'Payment Delay (days)', min: 0, max: 60 },
            ].map(field => (
              <div key={field.name}>
                <label className="label">{field.label}</label>
                <input
                  type="number" name={field.name} value={form[field.name]}
                  onChange={handleChange}
                  min={field.min} max={field.max} step={field.step || 1}
                  className="input-field"
                />
              </div>
            ))}
            <div>
              <label className="label">Contract Type</label>
              <select name="contract_type" value={form.contract_type} onChange={handleChange} className="input-field">
                <option>Month-to-Month</option>
                <option>One Year</option>
                <option>Two Year</option>
              </select>
            </div>
          </div>

          <div className="flex gap-3 mt-6">
            <button onClick={predictChurn} disabled={loading} className="btn-primary flex items-center gap-2">
              <Zap className="w-4 h-4" /> {loading ? 'Predicting...' : 'Predict Churn'}
            </button>
            <button onClick={runBatchPrediction} disabled={loading} className="btn-secondary flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" /> Batch Predict All
            </button>
          </div>
        </div>

        {/* Prediction Result */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <TrendingDown className="w-5 h-5 text-red-500" /> Prediction Result
          </h3>

          {prediction ? (
            <div className={`p-6 rounded-xl border-2 ${riskStyle(prediction.risk_level).bg} ${riskStyle(prediction.risk_level).border}`}>
              <div className="text-center mb-4">
                <div className={`text-5xl font-bold ${riskStyle(prediction.risk_level).text}`}>
                  {(prediction.churn_probability * 100).toFixed(1)}%
                </div>
                <p className="text-sm text-gray-600 mt-1">Churn Probability</p>
              </div>

              <div className="flex items-center justify-center gap-4 mb-4">
                <span className={`px-4 py-2 rounded-full text-lg font-semibold ${riskStyle(prediction.risk_level).bg} ${riskStyle(prediction.risk_level).text}`}>
                  {prediction.risk_level} Risk
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-white/80 p-3 rounded-lg">
                  <p className="text-gray-500">Model Used</p>
                  <p className="font-semibold">{prediction.model_used}</p>
                </div>
                <div className="bg-white/80 p-3 rounded-lg">
                  <p className="text-gray-500">Prediction</p>
                  <p className={`font-semibold ${prediction.predicted_churn ? 'text-red-600' : 'text-green-600'}`}>
                    {prediction.predicted_churn ? 'Will Churn' : 'Will Stay'}
                  </p>
                </div>
              </div>

              {/* Feature Importance */}
              {prediction.feature_importance && Object.keys(prediction.feature_importance).length > 0 && (
                <div className="mt-4 bg-white/80 p-3 rounded-lg">
                  <p className="text-sm font-medium text-gray-600 mb-2">Feature Importance</p>
                  {Object.entries(prediction.feature_importance)
                    .sort(([,a], [,b]) => b - a)
                    .map(([feature, importance]) => (
                      <div key={feature} className="flex items-center gap-2 mb-1">
                        <span className="text-xs text-gray-600 w-32 truncate">{feature}</span>
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div className="bg-primary-500 rounded-full h-2" style={{ width: `${importance * 100}%` }}></div>
                        </div>
                        <span className="text-xs font-mono text-gray-500 w-12">{(importance * 100).toFixed(1)}%</span>
                      </div>
                    ))
                  }
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-64 text-gray-400">
              <AlertTriangle className="w-12 h-12 mb-3" />
              <p>Enter customer features and click Predict</p>
            </div>
          )}
        </div>
      </div>

      {/* Batch Results */}
      {batchResult && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">
            Batch Prediction Results - {batchResult.total_predicted} Customers
          </h3>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="stat-card text-center">
              <p className="text-sm text-gray-500">At Risk (Churn)</p>
              <p className="text-2xl font-bold text-red-600">{batchResult.churn_count}</p>
            </div>
            <div className="stat-card text-center">
              <p className="text-sm text-gray-500">Safe (No Churn)</p>
              <p className="text-2xl font-bold text-green-600">{batchResult.no_churn_count}</p>
            </div>
            <div className="stat-card text-center">
              <p className="text-sm text-gray-500">Model</p>
              <p className="text-lg font-bold text-primary-600">{batchResult.model_name}</p>
            </div>
          </div>

          <div className="overflow-x-auto max-h-96">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-gray-50">
                <tr>
                  <th className="text-left py-2 px-3 font-medium text-gray-600">Customer ID</th>
                  <th className="text-left py-2 px-3 font-medium text-gray-600">Probability</th>
                  <th className="text-left py-2 px-3 font-medium text-gray-600">Risk Level</th>
                  <th className="text-left py-2 px-3 font-medium text-gray-600">Prediction</th>
                </tr>
              </thead>
              <tbody>
                {batchResult.predictions.slice(0, 50).map((p, i) => (
                  <tr key={i} className="border-t border-gray-100 hover:bg-gray-50">
                    <td className="py-2 px-3 font-mono text-xs">#{p.customer_id}</td>
                    <td className="py-2 px-3">{(p.churn_probability * 100).toFixed(1)}%</td>
                    <td className="py-2 px-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${riskStyle(p.risk_level).bg} ${riskStyle(p.risk_level).text}`}>
                        {p.risk_level}
                      </span>
                    </td>
                    <td className="py-2 px-3">
                      <span className={p.predicted_churn ? 'text-red-600 font-medium' : 'text-green-600'}>
                        {p.predicted_churn ? 'Churn' : 'Stay'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {batchResult.predictions.length > 50 && (
            <p className="text-sm text-gray-400 text-center mt-2">Showing 50 of {batchResult.predictions.length}</p>
          )}
        </div>
      )}
    </div>
  )
}
