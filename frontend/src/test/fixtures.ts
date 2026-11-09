import type { Drop } from '../api'

export function makeDrop(overrides: Partial<Drop> = {}): Drop {
  return {
    id: 1,
    product: 'Air Max 1 « Laval »',
    description: 'Édition locale',
    price_cents: 18000,
    stock: 100,
    remaining: 42,
    opens_at: '2026-01-01T09:00:00Z',
    status: 'live',
    ...overrides,
  }
}
