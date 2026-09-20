/**
 * Customer List Page - Search, filter, and manage all customers.
 */
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Search, Edit2, Trash2, Eye, ChevronLeft, ChevronRight } from 'lucide-react'
import api from '../../services/api'
import toast from 'react-hot-toast'

export default function CustomerListPage() {
  const [customers, setCustomers] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editCustomer, setEditCustomer] = useState(null)
  const [form, setForm] = useState({
    first_name: '', last_name: '', email: '', phone: '',
    subscription_type: 'Basic', monthly_charges: 0, tenure_months: 0,
    usage_frequency: 0, support_tickets: 0, complaints: 0, payment_delay_days: 0,
  })

  useEffect(() => {
    fetchCustomers()
  }, [page, search, statusFilter])

  const fetchCustomers = async () => {
    setLoading(true)
    try {
      const params = { page, per_page: 15 }
      if (search) params.search = search
      if (statusFilter) params.status_filter = statusFilter
      const res = await api.get('/customers', { params })
      setCustomers(res.data.customers)
      setTotal(res.data.total)
      setTotalPages(res.data.total_pages)
    } catch (error) {
      toast.error('Failed to load customers')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      if (editCustomer) {
        await api.put(`/customers/${editCustomer.id}`, form)
        toast.success('Customer updated')
      } else {
        await api.post('/customers', form)
        toast.success('Customer created')
      }
      setShowModal(false)
      setEditCustomer(null)
      setForm({ first_name: '', last_name: '', email: '', phone: '', subscription_type: 'Basic', monthly_charges: 0, tenure_months: 0, usage_frequency: 0, support_tickets: 0, complaints: 0, payment_delay_days: 0 })
      fetchCustomers()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure?')) return
    try {
      await api.delete(`/customers/${id}`)
      toast.success('Customer deleted')
      fetchCustomers()
    } catch (error) {
      toast.error('Failed to delete')
    }
  }

  const openEdit = (customer) => {
    setEditCustomer(customer)
    setForm({
      first_name: customer.first_name, last_name: customer.last_name,
      email: customer.email || '', phone: customer.phone || '',
      subscription_type: customer.subscription_type, monthly_charges: customer.monthly_charges,
      tenure_months: customer.tenure_months, usage_frequency: customer.usage_frequency,
      support_tickets: customer.support_tickets, complaints: customer.complaints,
      payment_delay_days: customer.payment_delay_days,
    })
    setShowModal(true)
  }

  const openNew = () => {
    setEditCustomer(null)
    setForm({ first_name: '', last_name: '', email: '', phone: '', subscription_type: 'Basic', monthly_charges: 0, tenure_months: 0, usage_frequency: 0, support_tickets: 0, complaints: 0, payment_delay_days: 0 })
    setShowModal(true)
  }

  const riskColor = (level) => ({
    Low: 'bg-green-100 text-green-700',
    Medium: 'bg-yellow-100 text-yellow-700',
    High: 'bg-orange-100 text-orange-700',
    Critical: 'bg-red-100 text-red-700',
  }[level] || 'bg-gray-100 text-gray-700')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Customers</h1>
          <p className="text-gray-500">{total} total customers</p>
        </div>
        <button onClick={openNew} className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" /> Add Customer
        </button>
      </div>

      {/* Search & Filters */}
      <div className="card flex flex-wrap gap-4 items-center">
        <div className="flex-1 min-w-[200px] relative">
          <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
          <input
            value={search} onChange={(e) => { setSearch(e.target.value); setPage(1) }}
            className="input-field pl-10" placeholder="Search customers..."
          />
        </div>
        <select value={statusFilter} onChange={(e) => { setStatusFilter(e.target.value); setPage(1) }} className="input-field w-auto">
          <option value="">All Status</option>
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
          <option value="Churned">Churned</option>
        </select>
      </div>

      {/* Customer Table */}
      <div className="card overflow-hidden p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Customer</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">ID</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Subscription</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Monthly</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Segment</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Risk</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Status</th>
                <th className="text-right py-3 px-4 font-medium text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="8" className="py-12 text-center text-gray-400">Loading...</td></tr>
              ) : customers.length === 0 ? (
                <tr><td colSpan="8" className="py-12 text-center text-gray-400">No customers found</td></tr>
              ) : customers.map((c) => (
                <tr key={c.id} className="border-t border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <Link to={`/customers/${c.id}`} className="font-medium text-primary-600 hover:text-primary-700">
                      {c.first_name} {c.last_name}
                    </Link>
                    <p className="text-xs text-gray-500">{c.email}</p>
                  </td>
                  <td className="py-3 px-4 text-gray-500 text-xs font-mono">{c.customer_id}</td>
                  <td className="py-3 px-4">{c.subscription_type}</td>
                  <td className="py-3 px-4">${c.monthly_charges}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs">{c.segment}</span>
                  </td>
                  <td className="py-3 px-4">
                    {c.risk_level && <span className={`px-2 py-1 rounded-full text-xs font-medium ${riskColor(c.risk_level)}`}>{c.risk_level}</span>}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      c.status === 'Active' ? 'bg-green-100 text-green-700' :
                      c.status === 'Churned' ? 'bg-red-100 text-red-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>{c.status}</span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex justify-end gap-1">
                      <Link to={`/customers/${c.id}`} className="p-1.5 hover:bg-gray-100 rounded"><Eye className="w-4 h-4 text-gray-500" /></Link>
                      <button onClick={() => openEdit(c)} className="p-1.5 hover:bg-gray-100 rounded"><Edit2 className="w-4 h-4 text-gray-500" /></button>
                      <button onClick={() => handleDelete(c.id)} className="p-1.5 hover:bg-red-50 rounded"><Trash2 className="w-4 h-4 text-red-500" /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between px-4 py-3 border-t">
          <p className="text-sm text-gray-500">Page {page} of {totalPages}</p>
          <div className="flex gap-2">
            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary text-sm py-1 px-3 disabled:opacity-50">
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages} className="btn-secondary text-sm py-1 px-3 disabled:opacity-50">
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Add/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-lg font-semibold mb-4">{editCustomer ? 'Edit Customer' : 'Add Customer'}</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">First Name</label>
                  <input value={form.first_name} onChange={(e) => setForm({...form, first_name: e.target.value})} className="input-field" />
                </div>
                <div>
                  <label className="label">Last Name</label>
                  <input value={form.last_name} onChange={(e) => setForm({...form, last_name: e.target.value})} className="input-field" />
                </div>
                <div>
                  <label className="label">Email</label>
                  <input value={form.email} onChange={(e) => setForm({...form, email: e.target.value})} className="input-field" />
                </div>
                <div>
                  <label className="label">Phone</label>
                  <input value={form.phone} onChange={(e) => setForm({...form, phone: e.target.value})} className="input-field" />
                </div>
                <div>
                  <label className="label">Subscription</label>
                  <select value={form.subscription_type} onChange={(e) => setForm({...form, subscription_type: e.target.value})} className="input-field">
                    <option>Basic</option><option>Standard</option><option>Premium</option><option>Enterprise</option>
                  </select>
                </div>
                <div>
                  <label className="label">Monthly Charges ($)</label>
                  <input type="number" value={form.monthly_charges} onChange={(e) => setForm({...form, monthly_charges: parseFloat(e.target.value) || 0})} className="input-field" />
                </div>
                <div>
                  <label className="label">Tenure (months)</label>
                  <input type="number" value={form.tenure_months} onChange={(e) => setForm({...form, tenure_months: parseInt(e.target.value) || 0})} className="input-field" />
                </div>
                <div>
                  <label className="label">Usage Frequency</label>
                  <input type="number" value={form.usage_frequency} onChange={(e) => setForm({...form, usage_frequency: parseInt(e.target.value) || 0})} className="input-field" />
                </div>
                <div>
                  <label className="label">Support Tickets</label>
                  <input type="number" value={form.support_tickets} onChange={(e) => setForm({...form, support_tickets: parseInt(e.target.value) || 0})} className="input-field" />
                </div>
                <div>
                  <label className="label">Complaints</label>
                  <input type="number" value={form.complaints} onChange={(e) => setForm({...form, complaints: parseInt(e.target.value) || 0})} className="input-field" />
                </div>
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <button onClick={() => { setShowModal(false); setEditCustomer(null) }} className="btn-secondary">Cancel</button>
                <button onClick={handleSave} className="btn-primary">{editCustomer ? 'Update' : 'Create'}</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
