/**
 * Header Component - User info, search, and notifications.
 */
import { useAuth } from '../../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import { Menu, LogOut, Bell, User } from 'lucide-react'

export default function Header({ onMenuToggle }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between sticky top-0 z-20">
      <button onClick={onMenuToggle} className="p-2 hover:bg-gray-100 rounded-lg">
        <Menu className="w-5 h-5 text-gray-600" />
      </button>

      <div className="flex items-center gap-4">
        <button className="p-2 hover:bg-gray-100 rounded-lg relative">
          <Bell className="w-5 h-5 text-gray-600" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        <div className="flex items-center gap-3 border-l pl-4">
          <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
            <User className="w-4 h-4 text-primary-600" />
          </div>
          <div className="text-sm">
            <p className="font-medium text-gray-800">{user?.full_name || 'User'}</p>
            <p className="text-gray-500 text-xs capitalize">{user?.role || 'manager'}</p>
          </div>
          <button
            onClick={handleLogout}
            className="p-2 hover:bg-gray-100 rounded-lg text-gray-500 hover:text-red-600"
            title="Logout"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  )
}
