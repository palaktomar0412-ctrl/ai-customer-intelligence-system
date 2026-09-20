/**
 * Customer Profile Page - Detailed view of a single customer with charts.
 */
import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Mail, Phone, MapPin, Calendar, AlertTriangle } from 'lucide-react'
import { Bar, Line } from 'react-chartjs-2'
import api from '../../services/api'
import toast from 'react-hot-toast'

export default function CustomerProfilePage() {
  const { id } = useParams()
  const [customer, setCustomer] = useState(null)
  const [purchases, setPurchases] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCustomerData()
  }, [id])

  const fetchCustomerData = async () => {
    setLoading(true)
    try {
      const [custRes, purRes] = await Promise.all([
        api.get(`/customers/${id}`),
        api.get(`/customers/${id}/purchases`).catch(() => ({ data: [] })),
      ])
      setCustomer(custRes.data)
      setPurchases(purRes.data)
    } catch (error) {
      toast.error('Failed to load customer')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="flex items-center justify-center h-96"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  if (!customer) return <div className="text-center py-12 text-gray-500">Customer not found</div>

  const riskColor = {
    Low: 'text-green-600 bg-green-50',
    Medium: 'text-yellow-600 bg-yellow-50',
    High: 'text-orange-600 bg-orange-50',
    Critical: 'text-red-600 bg-red-50',
  }[customer.risk_level] || 'text-gray-600 bg-gray-50'

  const purchaseChartData = {
    labels: purchases.slice(0, 10).map(p => p.product_name.substring(0, 15)),
    datasets: [{
      label: 'Amount ($)',
      data: purchases.slice(0, 10).map(p => p.final_amount),
      backgroundColor: '#3b82f6',
      borderRadius: 4,
    }],
  }

  return (
    <div className="space-y-6">
      {/* Back button */}
      <Link to="/customers" className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-700">
        <ArrowLeft className="w-4 h-4" /> Back to Customers
      </Link>

      {/* Profile Header */}
      <div className="card">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-xl font-bold text-primary-600">{customer.first_name[0]}{customer.last_name[0]}</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{customer.first_name} {customer.last_name}</h1>
              <p className="text-gray-500 font-mono text-sm">{customer.customer_id}</p>
              <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                <span className="flex items-center gap-1"><Mail className="w-3 h-3" /> {customer.email}</span>
                <span className="flex items-center gap-1"><Phone className="w-3 h-3" /> {customer.phone}</span>
                <span className="flex items-center gap-1"><MapPin className="w-3 h-3" /> {customer.city}, {customer.state}</span>
              </div>
            </div>
          </div>
          <div className="text-right">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              customer.status === 'Active' ? 'bg-green-100 text-green-700' :
              customer.status === 'Churned' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'
            }`}>{customer.status}</span>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="stat-card text-center">
          <p className="text-sm text-gray-500">Monthly Charges</p>
          <p className="text-xl font-bold text-gray-900">${customer.monthly_charges}</p>
        </div>
        <div className="stat-card text-center">
          <p className="text-sm text-gray-500">Total Charges</p>
          <p className="text-xl font-bold text-gray-900">${customer.total_charges.toLocaleString()}</p>
        </div>
        <div className="stat-card text-center">
          <p className="text-sm text-gray-500">CLV Score</p>
          <p className="text-xl font-bold text-purple-600">${(customer.clv_score || 0).toLocaleString()}</p>
        </div>
        <div className="stat-card text-center">
          <p className="text-sm text-gray-500">Risk Level</p>
          <p className={`text-xl font-bold px-3 py-1 rounded-lg inline-block ${riskColor}`}>
            {customer.risk_level || 'N/A'}
          </p>
        </div>
      </div>

      {/* Details Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Customer Info */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Customer Information</h3>
          <div className="space-y-3 text-sm">
            {[
              ['Subscription', customer.subscription_type],
              ['Contract', customer.contract_type],
              ['Tenure', `${customer.tenure_months} months`],
              ['Segment', customer.segment],
              ['Usage Frequency', `${customer.usage_frequency} sessions/month`],
              ['Support Tickets', customer.support_tickets],
              ['Complaints', customer.complaints],
              ['Payment Delay', `${customer.payment_delay_days} days`],
              ['Churn Probability', customer.churn_probability ? `${(customer.churn_probability * 100).toFixed(1)}%` : 'N/A'],
              ['Acquired', customer.acquired_date],
            ].map(([label, value]) => (
              <div key={label} className="flex justify-between py-2 border-b border-gray-100">
                <span className="text-gray-500">{label}</span>
                <span className="font-medium text-gray-900">{value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Purchase History Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Purchase History</h3>
          {purchases.length > 0 ? (
            <div className="h-64">
              <Bar data={purchaseChartData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }} />
            </div>
          ) : (
            <p className="text-gray-400 text-center py-8">No purchases recorded</p>
          )}
        </div>
      </div>

      {/* Purchase Table */}
      {purchases.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Recent Purchases</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Product</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Category</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Qty</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Amount</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Payment</th>
                </tr>
              </thead>
              <tbody>
                {purchases.map((p) => (
                  <tr key={p.id} className="border-t border-gray-100">
                    <td className="py-3 px-4 font-medium">{p.product_name}</td>
                    <td className="py-3 px-4 text-gray-500">{p.product_category}</td>
                    <td className="py-3 px-4">{p.quantity}</td>
                    <td className="py-3 px-4 font-medium">${p.final_amount}</td>
                    <td className="py-3 px-4"><span className="px-2 py-1 bg-green-50 text-green-700 rounded-full text-xs">{p.payment_status}</span></td>
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
