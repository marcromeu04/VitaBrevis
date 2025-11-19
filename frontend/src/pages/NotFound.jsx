import { Link } from 'react-router-dom'
import { Home } from 'lucide-react'

const NotFound = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-9xl font-bold text-primary-600">404</h1>
        <p className="text-2xl font-semibold text-gray-900 mt-4">Página no encontrada</p>
        <p className="text-gray-600 mt-2">La página que buscas no existe.</p>
        <Link to="/dashboard" className="btn btn-primary mt-6 inline-flex items-center">
          <Home className="w-5 h-5 mr-2" />
          Volver al Dashboard
        </Link>
      </div>
    </div>
  )
}

export default NotFound
