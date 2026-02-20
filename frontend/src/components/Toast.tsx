import { useState, useEffect } from 'react'

interface ToastMessage {
  id: string
  message: string
  type: 'success' | 'error' | 'info'
  duration?: number
}

let toastId = 0

export function useToast() {
  const [toasts, setToasts] = useState<ToastMessage[]>([])

  const addToast = (message: string, type: 'success' | 'error' | 'info' = 'info', duration = 3000) => {
    const id = String(toastId++)
    const toast: ToastMessage = { id, message, type, duration }
    
    setToasts(prev => [...prev, toast])
    
    if (duration) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
    
    return id
  }

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }

  return { toasts, addToast, removeToast }
}

interface ToastContainerProps {
  toasts: ToastMessage[]
  removeToast: (id: string) => void
}

export function ToastContainer({ toasts, removeToast }: ToastContainerProps) {
  return (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      {toasts.map(toast => (
        <div
          key={toast.id}
          className={`
            px-4 py-3 rounded-lg text-white font-medium max-w-sm
            ${toast.type === 'success' && 'bg-green-600'}
            ${toast.type === 'error' && 'bg-red-600'}
            ${toast.type === 'info' && 'bg-blue-600'}
            animate-in fade-in slide-in-from-right-2
          `}
        >
          <div className="flex justify-between items-center">
            <span>{toast.message}</span>
            <button
              onClick={() => removeToast(toast.id)}
              className="ml-2 font-bold hover:opacity-75"
            >
              ×
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
