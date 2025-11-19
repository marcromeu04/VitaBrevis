import { Dna, Upload, FileText, AlertTriangle } from 'lucide-react'

const GeneticPage = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Datos Genéticos</h1>
          <p className="text-gray-600 mt-1">
            Visualización de informes genéticos (solo datos, sin interpretación)
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Upload className="w-5 h-5 mr-2" />
          Subir Informe Genético
        </button>
      </div>

      {/* Advertencia legal importante */}
      <div className="p-4 bg-red-50 border-2 border-red-300 rounded-lg">
        <div className="flex items-start">
          <AlertTriangle className="w-6 h-6 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-bold text-red-900 mb-1">AVISO LEGAL IMPORTANTE</p>
            <p className="text-sm text-red-800">
              Esta plataforma <strong>SOLO VISUALIZA</strong> datos genéticos proporcionados por laboratorios.
              NO interpreta variantes, NO calcula riesgos de enfermedad, y NO genera recomendaciones.
              La interpretación debe ser realizada EXCLUSIVAMENTE por profesionales médicos especializados.
            </p>
          </div>
        </div>
      </div>

      {/* Informes genéticos */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Informes Genéticos</h2>

        <div className="text-center py-12 text-gray-500">
          <Dna className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-lg font-medium">No hay informes genéticos cargados</p>
          <p className="text-sm mt-2 mb-4">
            Sube informes de laboratorios autorizados (23andMe, AncestryDNA, etc.)
          </p>
          <button className="btn btn-secondary flex items-center mx-auto">
            <Upload className="w-5 h-5 mr-2" />
            Subir Primer Informe
          </button>
        </div>
      </div>

      {/* Categorías genéticas (ejemplo de cómo se mostrará) */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Categorías de Datos Genéticos
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { name: 'Metabolismo', icon: '🔥', description: 'Metabolismo de nutrientes y energía' },
            { name: 'Vitaminas', icon: '💊', description: 'Absorción y procesamiento de vitaminas' },
            { name: 'Inflamación', icon: '🔴', description: 'Respuesta inflamatoria' },
            { name: 'Detoxificación', icon: '🧪', description: 'Capacidad de detoxificación' },
            { name: 'Antioxidantes', icon: '🛡️', description: 'Capacidad antioxidante' },
            { name: 'Otros', icon: '📊', description: 'Otros marcadores genéticos' },
          ].map((category) => (
            <div key={category.name} className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer">
              <div className="text-3xl mb-2">{category.icon}</div>
              <h3 className="font-bold text-gray-900">{category.name}</h3>
              <p className="text-sm text-gray-600 mt-1">{category.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Información adicional */}
      <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-sm text-yellow-800">
          <strong>Consentimiento requerido:</strong> El almacenamiento de datos genéticos requiere
          consentimiento específico según la Ley 14/2007 de Investigación Biomédica (España).
        </p>
      </div>
    </div>
  )
}

export default GeneticPage
