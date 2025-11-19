import { useAuth } from '../../contexts/AuthContext'

const Profile = () => {
  const { user } = useAuth()

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Mi Perfil</h1>
        <p className="text-gray-600 mt-1">Información de tu cuenta</p>
      </div>

      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Información Personal</h2>
        <div className="space-y-4">
          <div>
            <label className="label">Nombre Completo</label>
            <input
              type="text"
              defaultValue={`${user?.first_name} ${user?.last_name}`}
              className="input"
              disabled
            />
          </div>

          <div>
            <label className="label">Email</label>
            <input
              type="email"
              defaultValue={user?.email}
              className="input"
              disabled
            />
          </div>

          <div>
            <label className="label">Usuario</label>
            <input
              type="text"
              defaultValue={user?.username}
              className="input"
              disabled
            />
          </div>

          <div>
            <label className="label">Rol</label>
            <input
              type="text"
              defaultValue={user?.role}
              className="input"
              disabled
            />
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Seguridad</h2>
        <div className="space-y-4">
          <button className="btn btn-secondary">Cambiar Contraseña</button>
          <button className="btn btn-secondary">Habilitar 2FA</button>
        </div>
      </div>
    </div>
  )
}

export default Profile
