export type DropStatus = 'upcoming' | 'live' | 'sold_out'

export interface Drop {
  id: number
  product: string
  description: string
  price_cents: number
  stock: number
  remaining: number
  opens_at: string
  status: DropStatus
}

export interface Order {
  id: number
  drop_id: number
  created_at: string
  drop: Drop
}

const API_URL = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')

export class ApiError extends Error {
  readonly status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_URL}${path}`, init)
  } catch {
    throw new ApiError(0, "L'API est injoignable. Réessayez dans quelques instants.")
  }
  const body = await response.json().catch(() => null)
  if (!response.ok) {
    const detail = typeof body?.detail === 'string' ? body.detail : `Erreur ${response.status}`
    throw new ApiError(response.status, detail)
  }
  return body as T
}

export function listDrops(status?: DropStatus): Promise<Drop[]> {
  const query = status ? `?status=${status}` : ''
  return request<Drop[]>(`/drops${query}`)
}

export function getDrop(id: number): Promise<Drop> {
  return request<Drop>(`/drops/${id}`)
}

export function placeOrder(id: number): Promise<Order> {
  return request<Order>(`/drops/${id}/orders`, { method: 'POST' })
}
