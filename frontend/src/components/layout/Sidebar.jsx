/**
 * Sidebar Navigation Component
 */
import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, Users, PieChart, AlertTriangle,
  Lightbulb, FileText, ChevronLeft, ChevronRight, Brain
} from 'lucide-react'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/customers', icon: Users, label: 'Customers' },
  { to: '/segmentation', icon: PieChart, label: 'Segmentation' },
  { to: '/churn', icon: AlertTriangle, label: 'Churn Prediction' },
  { to: '/recommendations', icon: Lightbulb, label: 'Recommendations' },
  { to: '/reports', icon: FileText, label: 'Reports' },
]

export default function Sidebar({ isOpen, onToggle }) {
  return (
    <aside className={`fixed left-0 top-0 h-full bg-gray-900 text-white transition-all duration-300 z-30 ${isOpen ? 'w-64' : 'w-16'}`}>
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-gray-700">
        <Brain className="w-8 h-8 text-primary-400 flex-shrink-0" />
        {isOpen && (
          <div className="overflow-hidden">
            <h1 className="text-sm font-bold text-white leading-tight">Customer</h1>
            <h1 className="text-sm font-bold text-primary-400 leading-tight">Intelligence</h1>
          </div>
        )}
      </div>

      {/* Navigation Links */}
      <nav className="mt-4 px-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-3 rounded-lg mb-1 transition-colors ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`
            }
          >
            <item.icon className="w-5 h-5 flex-shrink-0" />
            {isOpen && <span className="text-sm font-medium">{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Toggle Button */}
      <button
        onClick={onToggle}
        className="absolute bottom-4 left-0 right-0 mx-auto w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors"
      >
        {isOpen ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
      </button>
    </aside>
  )
}
