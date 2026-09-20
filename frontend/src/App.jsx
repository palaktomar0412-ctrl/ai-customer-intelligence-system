/**
 * Main Application Component - Routes and Layout
 */
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/layout/Layout'
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import CustomerListPage from './pages/customers/CustomerListPage'
import CustomerProfilePage from './pages/customers/CustomerProfilePage'
import SegmentationPage from './pages/segmentation/SegmentationPage'
import ChurnPredictionPage from './pages/churn/ChurnPredictionPage'
import RecommendationsPage from './pages/recommendations/RecommendationsPage'
import ReportsPage from './pages/reports/ReportsPage'

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  if (loading) return <div className="flex items-center justify-center h-screen"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  return isAuthenticated ? children : <Navigate to="/login" />
}

function PublicRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  if (loading) return null
  return isAuthenticated ? <Navigate to="/dashboard" /> : children
}

export default function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />

      {/* Protected Routes */}
      <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route index element={<Navigate to="/dashboard" />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="customers" element={<CustomerListPage />} />
        <Route path="customers/:id" element={<CustomerProfilePage />} />
        <Route path="segmentation" element={<SegmentationPage />} />
        <Route path="churn" element={<ChurnPredictionPage />} />
        <Route path="recommendations" element={<RecommendationsPage />} />
        <Route path="reports" element={<ReportsPage />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<Navigate to="/dashboard" />} />
    </Routes>
  )
}
