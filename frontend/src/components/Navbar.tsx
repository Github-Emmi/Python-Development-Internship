import { useNavigate } from 'react-router-dom'

interface NavbarProps {
  onLogout: () => void
}

export function Navbar({ onLogout }: NavbarProps) {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    onLogout()
    navigate('/login')
  }

  return (
    <nav className="bg-slate-800 border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div 
            className="flex items-center cursor-pointer"
            onClick={() => navigate('/dashboard')}
          >
            <span className="text-2xl font-bold gradient-text">EmmiDev</span>
          </div>
          
          <div className="flex items-center space-x-6">
            <button
              onClick={() => navigate('/dashboard')}
              className="text-gray-300 hover:text-white transition-colors px-3 py-2"
            >
              Dashboard
            </button>
            <button
              onClick={() => navigate('/products')}
              className="text-gray-300 hover:text-white transition-colors px-3 py-2"
            >
              Products
            </button>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
