import { FileText, Download, Calendar, Filter } from 'lucide-react'

const ReportsPage = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Informes</h1>
          <p className="text-gray-600 mt-1">
            Informes descriptivos y exportación de datos
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <FileText className="w-5 h-5 mr-2" />
          Generar Informe
        </button>
      </div>

      {/* Filtros */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="label">Tipo de Informe</label>
            <select className="input">
              <option>Todos los tipos</option>
              <option>Informe Mensual</option>
              <option>Informe Trimestral</option>
              <option>Informe Anual</option>
              <option>Informe Personalizado</option>
            </select>
          </div>
          <div>
            <label className="label">Desde</label>
            <input type="date" className="input" />
          </div>
          <div>
            <label className="label">Hasta</label>
            <input type="date" className="input" />
          </div>
        </div>
      </div>

      {/* Tipos de informes disponibles */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          {
            title: 'Informe Mensual',
            description: 'Resumen de biomarcadores y tendencias del último mes',
            icon: '📊',
          },
          {
            title: 'Informe Trimestral',
            description: 'Análisis completo de 3 meses con comparativas',
            icon: '📈',
          },
          {
            title: 'Informe Anual',
            description: 'Vista completa del año con evolución',
            icon: '📅',
          },
          {
            title: 'Informe de Composición Corporal',
            description: 'Evolución de peso, masa muscular y grasa',
            icon: '💪',
          },
          {
            title: 'Informe Genético',
            description: 'Resumen descriptivo de datos genéticos',
            icon: '🧬',
          },
          {
            title: 'Informe Personalizado',
            description: 'Crea un informe con los datos que elijas',
            icon: '⚙️',
          },
        ].map((report) => (
          <div key={report.title} className="card hover:shadow-md transition-shadow">
            <div className="text-4xl mb-3">{report.icon}</div>
            <h3 className="font-bold text-gray-900 mb-2">{report.title}</h3>
            <p className="text-sm text-gray-600 mb-4">{report.description}</p>
            <button className="btn btn-secondary w-full flex items-center justify-center">
              <FileText className="w-4 h-4 mr-2" />
              Generar
            </button>
          </div>
        ))}
      </div>

      {/* Historial de informes */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Informes Generados
        </h2>

        <div className="text-center py-12 text-gray-500">
          <FileText className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-lg font-medium">No hay informes generados aún</p>
          <p className="text-sm mt-2 mb-4">
            Genera tu primer informe para visualizar datos del paciente
          </p>
          <button className="btn btn-secondary flex items-center mx-auto">
            <FileText className="w-5 h-5 mr-2" />
            Generar Primer Informe
          </button>
        </div>
      </div>

      {/* Características de los informes */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Características de los Informes
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { icon: '📄', text: 'Exportación en PDF de alta calidad' },
            { icon: '📊', text: 'Gráficas automáticas de tendencias' },
            { icon: '🔒', text: 'Cifrado y cumplimiento GDPR' },
            { icon: '📧', text: 'Envío automático por email' },
            { icon: '🎨', text: 'Personalización con logo de clínica' },
            { icon: '⚖️', text: 'Solo descriptivos, sin interpretación médica' },
          ].map((feature, index) => (
            <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <span className="text-2xl">{feature.icon}</span>
              <span className="text-sm text-gray-700">{feature.text}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Disclaimer legal */}
      <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-sm text-yellow-800">
          <strong>Importante:</strong> Los informes generados son puramente descriptivos y
          muestran datos numéricos y tendencias. NO incluyen diagnósticos, interpretaciones
          médicas ni recomendaciones terapéuticas. El profesional sanitario debe interpretar
          los datos según su criterio clínico.
        </p>
      </div>
    </div>
  )
}

export default ReportsPage
