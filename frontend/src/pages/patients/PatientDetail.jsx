import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import * as patientService from '../../services/patientService'

const PatientDetail = () => {
  const { id } = useParams()

  const { data: patient, isLoading } = useQuery({
    queryKey: ['patient', id],
    queryFn: () => patientService.getPatient(id),
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          {patient?.first_name} {patient?.last_name}
        </h1>
        <p className="text-gray-600 mt-1">Historia Clínica: {patient?.medical_record_number}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Información del Paciente</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Edad</p>
                <p className="text-base font-medium">{patient?.age} años</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Sexo</p>
                <p className="text-base font-medium">{patient?.sex}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Email</p>
                <p className="text-base font-medium">{patient?.email || 'No registrado'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Teléfono</p>
                <p className="text-base font-medium">{patient?.phone || 'No registrado'}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Timeline del Paciente</h2>
            <p className="text-gray-600">Próximamente: Vista cronológica de todas las pruebas y eventos</p>
          </div>
        </div>

        <div className="space-y-6">
          <div className="card">
            <h3 className="font-bold text-gray-900 mb-3">Programa de Longevidad</h3>
            <div className="space-y-2">
              <div>
                <p className="text-sm text-gray-600">Fase Actual</p>
                <span className="badge badge-info mt-1">
                  {patient?.program_phase?.replace('_', ' ')}
                </span>
              </div>
              {patient?.program_start_date && (
                <div>
                  <p className="text-sm text-gray-600">Fecha de Inicio</p>
                  <p className="text-sm font-medium">{patient.program_start_date}</p>
                </div>
              )}
            </div>
          </div>

          <div className="card">
            <h3 className="font-bold text-gray-900 mb-3">Acciones Rápidas</h3>
            <div className="space-y-2">
              <button className="w-full btn btn-primary">Añadir Biomarcador</button>
              <button className="w-full btn btn-secondary">Ver Informes</button>
              <button className="w-full btn btn-secondary">Editar Perfil</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PatientDetail
