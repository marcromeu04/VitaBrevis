import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import PrivateRoute from './components/PrivateRoute'

// Layouts
import DashboardLayout from './components/layouts/DashboardLayout'

// Pages - Auth
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'

// Pages - Dashboard
import Dashboard from './pages/dashboard/Dashboard'
import PatientList from './pages/patients/PatientList'
import PatientDetail from './pages/patients/PatientDetail'
import Profile from './pages/profile/Profile'

// Pages - Módulos
import BiomarkersPage from './pages/biomarkers/BiomarkersPage'
import GeneticPage from './pages/genetic/GeneticPage'
import MicrobiomePage from './pages/microbiome/MicrobiomePage'
import ReportsPage from './pages/reports/ReportsPage'

// Pages - Not Found
import NotFound from './pages/NotFound'

function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rutas privadas */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <DashboardLayout />
            </PrivateRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="patients" element={<PatientList />} />
          <Route path="patients/:id" element={<PatientDetail />} />
          <Route path="biomarkers" element={<BiomarkersPage />} />
          <Route path="genetic" element={<GeneticPage />} />
          <Route path="microbiome" element={<MicrobiomePage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="profile" element={<Profile />} />
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AuthProvider>
  )
}

export default App
