import { Microscope, Upload, PieChart, BarChart3 } from 'lucide-react'

const MicrobiomePage = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Microbioma</h1>
          <p className="text-gray-600 mt-1">
            Análisis de microbiota intestinal
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Upload className="w-5 h-5 mr-2" />
          Subir Análisis
        </button>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">Diversidad Alfa</h3>
            <PieChart className="w-5 h-5 text-primary-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">7.2</p>
          <p className="text-xs text-gray-500 mt-1">Índice Shannon</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">Firmicutes</h3>
            <BarChart3 className="w-5 h-5 text-success-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">65%</p>
          <p className="text-xs text-gray-500 mt-1">Abundancia relativa</p>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">Bacteroidetes</h3>
            <BarChart3 className="w-5 h-5 text-secondary-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">28%</p>
          <p className="text-xs text-gray-500 mt-1">Abundancia relativa</p>
        </div>
      </div>

      {/* Análisis del microbioma */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Historial de Análisis
        </h2>

        <div className="text-center py-12 text-gray-500">
          <Microscope className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-lg font-medium">No hay análisis de microbioma disponibles</p>
          <p className="text-sm mt-2 mb-4">
            Sube informes de laboratorios especializados (Viome, Thorne, BiomeFx, etc.)
          </p>
          <button className="btn btn-secondary flex items-center mx-auto">
            <Upload className="w-5 h-5 mr-2" />
            Subir Análisis
          </button>
        </div>
      </div>

      {/* Información sobre el microbioma */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Principales Phyla Bacterianos
        </h2>
        <div className="space-y-3">
          {[
            { name: 'Firmicutes', percentage: 65, color: 'bg-green-500' },
            { name: 'Bacteroidetes', percentage: 28, color: 'bg-blue-500' },
            { name: 'Proteobacteria', percentage: 4, color: 'bg-yellow-500' },
            { name: 'Actinobacteria', percentage: 2, color: 'bg-purple-500' },
            { name: 'Otros', percentage: 1, color: 'bg-gray-500' },
          ].map((phylum) => (
            <div key={phylum.name}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">{phylum.name}</span>
                <span className="text-sm text-gray-600">{phylum.percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`${phylum.color} h-2 rounded-full transition-all duration-300`}
                  style={{ width: `${phylum.percentage}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Nota:</strong> Los datos del microbioma son solo informativos.
          Esta plataforma muestra únicamente los resultados proporcionados por el laboratorio.
          NO se generan interpretaciones ni recomendaciones terapéuticas.
        </p>
      </div>
    </div>
  )
}

export default MicrobiomePage
