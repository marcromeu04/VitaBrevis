import { Users, Activity, Dna, TrendingUp } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

const StatCard = ({ title, value, icon: Icon, trend, color }) => (
  <div className="card">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-600">{title}</p>
        <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
        {trend && (
          <p className="text-sm text-success-600 mt-1 flex items-center">
            <TrendingUp className="w-4 h-4 mr-1" />
            {trend}
          </p>
        )}
      </div>
      <div className={`p-3 rounded-lg ${color}`}>
        <Icon className="w-8 h-8 text-white" />
      </div>
    </div>
  </div>
)

const Dashboard = () => {
  const { user } = useAuth()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Bienvenido, {user?.first_name}
        </h1>
        <p className="text-gray-600 mt-1">
          Panel de control de la clínica de longevidad
        </p>
      </div>

      {/* Estadísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Pacientes Activos"
          value="127"
          icon={Users}
          trend="+12% este mes"
          color="bg-primary-600"
        />
        <StatCard
          title="Biomarcadores Registrados"
          value="2,341"
          icon={Activity}
          trend="+8% este mes"
          color="bg-success-600"
        />
        <StatCard
          title="Datos Genéticos"
          value="45"
          icon={Dna}
          color="bg-secondary-600"
        />
        <StatCard
          title="Tasa de Mejora"
          value="87%"
          icon={TrendingUp}
          trend="+3% este mes"
          color="bg-warning-600"
        />
      </div>

      {/* Contenido principal */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Actividad reciente */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Actividad Reciente</h2>
          <div className="space-y-3">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">Nuevo registro de biomarcadores</p>
                  <p className="text-xs text-gray-500">Hace 2 horas</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Próximas citas */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Próximas Revisiones</h2>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-900">Paciente #{i}234</p>
                  <p className="text-xs text-gray-500">Revisión trimestral</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">15 Ene</p>
                  <p className="text-xs text-gray-500">10:00 AM</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Disclaimer legal */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Recordatorio:</strong> Esta plataforma solo visualiza datos clínicos.
          Todas las decisiones terapéuticas deben ser tomadas por profesionales médicos cualificados.
        </p>
      </div>
    </div>
  )
}

export default Dashboard
