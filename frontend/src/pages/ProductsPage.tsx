import { useState, useEffect } from 'react'
import { productService, Product } from '../lib/services'
import { Button } from '../components/Button'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '../components/Card'
import { useToast, ToastContainer } from '../components/Toast'

export function ProductsPage() {
  const { toasts, addToast, removeToast } = useToast()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    category: '',
  })

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    setLoading(true)
    try {
      const response = await productService.getProducts(0, 20)
      setProducts(response.data)
    } catch (error: any) {
      addToast('Failed to fetch products', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (editingId) {
        await productService.updateProduct(editingId, {
          name: formData.name,
          price: parseFloat(formData.price),
          category: formData.category,
        })
        addToast('Product updated successfully', 'success')
      } else {
        await productService.createProduct(
          formData.name,
          parseFloat(formData.price),
          formData.category
        )
        addToast('Product created successfully', 'success')
      }
      
      setFormData({ name: '', price: '', category: '' })
      setEditingId(null)
      setShowForm(false)
      await fetchProducts()
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Operation failed'
      addToast(message, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return

    try {
      await productService.deleteProduct(id)
      addToast('Product deleted successfully', 'success')
      await fetchProducts()
    } catch (error: any) {
      addToast('Failed to delete product', 'error')
    }
  }

  const handleEdit = (product: Product) => {
    setFormData({
      name: product.name,
      price: product.price.toString(),
      category: product.category,
    })
    setEditingId(product.id)
    setShowForm(true)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-white">Products</h1>
        <Button 
          onClick={() => {
            setShowForm(!showForm)
            setEditingId(null)
            setFormData({ name: '', price: '', category: '' })
          }}
        >
          {showForm && !editingId ? 'Cancel' : 'Add Product'}
        </Button>
      </div>

      {showForm && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>{editingId ? 'Edit Product' : 'Create New Product'}</CardTitle>
          </CardHeader>
          
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Product Name
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-slate-600 border border-slate-500 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Product name"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Price
                  </label>
                  <input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    required
                    step="0.01"
                    min="0"
                    className="w-full px-4 py-2 bg-slate-600 border border-slate-500 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="0.00"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Category
                  </label>
                  <select
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 bg-slate-600 border border-slate-500 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Select category</option>
                    <option value="Electronics">Electronics</option>
                    <option value="Accessories">Accessories</option>
                    <option value="Books">Books</option>
                    <option value="Clothing">Clothing</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <Button 
                type="submit" 
                className="w-full" 
                disabled={loading}
              >
                {loading ? 'Saving...' : editingId ? 'Update Product' : 'Create Product'}
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      {loading && !showForm ? (
        <div className="text-center py-8">
          <p className="text-gray-400">Loading products...</p>
        </div>
      ) : products.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-400">No products yet. Create one to get started!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map(product => (
            <Card key={product.id} className="hover-lift">
              <CardHeader>
                <CardTitle className="text-xl">{product.name}</CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-2">
                <div className="text-sm text-gray-400">Category: {product.category}</div>
                <div className="text-2xl font-bold text-green-400">
                  ${product.price.toFixed(2)}
                </div>
              </CardContent>

              <CardFooter className="justify-start gap-2">
                <Button
                  size="sm"
                  onClick={() => handleEdit(product)}
                  variant="secondary"
                >
                  Edit
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => handleDelete(product.id || product._id || '')}
                >
                  Delete
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </div>
  )
}
