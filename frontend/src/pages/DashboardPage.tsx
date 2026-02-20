import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { productService, Product } from '../lib/services'
import { Button } from '../components/Button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/Card'
import { useToast, ToastContainer } from '../components/Toast'

export function DashboardPage() {
  const { toasts, addToast, removeToast } = useToast()
  const navigate = useNavigate()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalValue: 0,
    avgPrice: 0,
  })

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const response = await productService.getProducts(0, 5)
      const products = response.data
      setProducts(products)

      // Calculate stats
      const totalProducts = products.length
      const totalValue = products.reduce((sum, p) => sum + p.price, 0)
      const avgPrice = totalProducts > 0 ? totalValue / totalProducts : 0

      setStats({
        totalProducts,
        totalValue,
        avgPrice,
      })
    } catch (error: any) {
      addToast('Failed to load dashboard data', 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-4xl font-bold text-white mb-8">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="hover-lift">
          <CardContent className="text-center py-6">
            <div className="text-3xl font-bold text-blue-400">{stats.totalProducts}</div>
            <div className="text-gray-400 mt-2">Total Products</div>
          </CardContent>
        </Card>

        <Card className="hover-lift">
          <CardContent className="text-center py-6">
            <div className="text-3xl font-bold text-green-400">
              ${stats.totalValue.toFixed(2)}
            </div>
            <div className="text-gray-400 mt-2">Total Value</div>
          </CardContent>
        </Card>

        <Card className="hover-lift">
          <CardContent className="text-center py-6">
            <div className="text-3xl font-bold text-purple-400">
              ${stats.avgPrice.toFixed(2)}
            </div>
            <div className="text-gray-400 mt-2">Average Price</div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Products */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Products</CardTitle>
          <CardDescription>Your 5 most recently added products</CardDescription>
        </CardHeader>
        
        <CardContent>
          {loading ? (
            <div className="text-center py-8">
              <p className="text-gray-400">Loading...</p>
            </div>
          ) : products.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-400 mb-4">No products yet</p>
              <Button onClick={() => navigate('/products')}>
                Create Your First Product
              </Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-600">
                    <th className="px-4 py-3 text-left text-gray-300 font-medium">Name</th>
                    <th className="px-4 py-3 text-left text-gray-300 font-medium">Category</th>
                    <th className="px-4 py-3 text-left text-gray-300 font-medium">Price</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map(product => (
                    <tr key={product.id} className="border-b border-slate-600 hover:bg-slate-600 transition-colors">
                      <td className="px-4 py-3 text-white">{product.name}</td>
                      <td className="px-4 py-3 text-gray-400">{product.category}</td>
                      <td className="px-4 py-3 text-green-400 font-medium">
                        ${product.price.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>

        <div className="p-6 border-t border-slate-600">
          <Button 
            onClick={() => navigate('/products')}
            className="w-full"
          >
            View All Products
          </Button>
        </div>
      </Card>

      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </div>
  )
}
