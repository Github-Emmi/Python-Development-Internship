import { useState } from 'react'

interface CardProps {
  className?: string
  children: React.ReactNode
}

export function Card({ className = '', children }: CardProps) {
  return (
    <div className={`bg-slate-700 rounded-lg border border-slate-600 p-6 card-shadow ${className}`}>
      {children}
    </div>
  )
}

export function CardHeader({ className = '', children }: CardProps) {
  return <div className={`mb-4 ${className}`}>{children}</div>
}

export function CardTitle({ className = '', children }: CardProps) {
  return <h2 className={`text-2xl font-bold text-white ${className}`}>{children}</h2>
}

export function CardDescription({ className = '', children }: CardProps) {
  return <p className={`text-gray-400 text-sm ${className}`}>{children}</p>
}

export function CardContent({ className = '', children }: CardProps) {
  return <div className={`${className}`}>{children}</div>
}

export function CardFooter({ className = '', children }: CardProps) {
  return <div className={`mt-6 flex justify-end space-x-4 ${className}`}>{children}</div>
}
