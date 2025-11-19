import { Activity, Plus, TrendingUp, TrendingDown } from 'lucide-react'

const BiomarkersPage = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Biomarcadores</h1>
          <p className="text-gray-600 mt-1">
            Biomarcadores clásicos y avanzados de longevidad
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Plus className="w-5 h-5 mr-2" />
          Nuevo Biomarcador
        </button>
      </div>

      {/* Categorías de biomarcadores */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-gray-900">Glucosa</h3>
            <Activity className="w-8 h-8 text-primary-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900">95 mg/dL</p>
          <p className="text-sm text-gray-600 mt-1">Rango óptimo: 70-100</p>
          <div className="mt-3 flex items-center text-success-600 text-sm">
            <TrendingDown className="w-4 h-4 mr-1" />
            -5% desde último mes
          </div>
        </div>

        <div className="card hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-gray-900">Colesterol Total</h3>
            <Activity className="w-8 h-8 text-warning-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900">185 mg/dL</p>
          <p className="text-sm text-gray-600 mt-1">Rango óptimo: &lt;200</p>
          <div className="mt-3 flex items-center text-warning-600 text-sm">
            <TrendingUp className="w-4 h-4 mr-1" />
            +3% desde último mes
          </div>
        </div>

        <div className="card hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-gray-900">Edad Epigenética</h3>
            <Activity className="w-8 h-8 text-secondary-600" />
          </div>
          <p className="text-2xl font-bold text-gray-900">38 años</p>
          <p className="text-sm text-gray-600 mt-1">Edad cronológica: 42</p>
          <div className="mt-3 flex items-center text-success-600 text-sm">
            <TrendingDown className="w-4 h-4 mr-1" />
            -2 años desde último test
          </div>
        </div>
      </div>

      {/* Tabla de biomarcadores */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Historial de Biomarcadores
        </h2>
        <div className="text-center py-12 text-gray-500">
          <Activity className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-lg font-medium">Funcionalidad en desarrollo</p>
          <p className="text-sm mt-2">
            Aquí se mostrará el historial completo de biomarcadores
          </p>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Nota:</strong> Los biomarcadores se muestran solo con fines informativos.
          La interpretación debe ser realizada por profesionales médicos cualificados.
        </p>
      </div>
    </div>
  )
}

export default BiomarkersPage
