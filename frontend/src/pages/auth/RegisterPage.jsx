/**
 * Registration Page - New user signup form.
 */
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { Brain, Mail, Lock, User, UserCheck } from 'lucide-react'
import toast from 'react-hot-toast'

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: '', email: '', password: '', full_name: '', role: 'manager'
  })
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await register(form)
      toast.success('Account created successfully!')
      navigate('/dashboard')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-primary-100">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-2xl mb-4">
            <Brain className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Create Account</h1>
          <p className="text-gray-500 mt-1">Join the intelligence platform</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Full Name</label>
              <div className="relative">
                <User className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <input name="full_name" value={form.full_name} onChange={handleChange}
                  className="input-field pl-10" placeholder="John Doe" required />
              </div>
            </div>
            <div>
              <label className="label">Username</label>
              <div className="relative">
                <UserCheck className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <input name="username" value={form.username} onChange={handleChange}
                  className="input-field pl-10" placeholder="johndoe" required />
              </div>
            </div>
            <div>
              <label className="label">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <input name="email" type="email" value={form.email} onChange={handleChange}
                  className="input-field pl-10" placeholder="john@example.com" required />
              </div>
            </div>
            <div>
              <label className="label">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <input name="password" type="password" value={form.password} onChange={handleChange}
                  className="input-field pl-10" placeholder="Min 6 characters" required minLength={6} />
              </div>
            </div>
            <div>
              <label className="label">Role</label>
              <select name="role" value={form.role} onChange={handleChange} className="input-field">
                <option value="manager">Manager</option>
                <option value="analyst">Analyst</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <button type="submit" disabled={loading} className="w-full btn-primary py-3 text-center disabled:opacity-50">
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>
          <div className="mt-4 text-center text-sm text-gray-500">
            Already have an account?{' '}
            <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">Sign In</Link>
          </div>
        </div>
      </div>
    </div>
  )
}
