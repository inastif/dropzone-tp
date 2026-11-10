import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { describe, expect, it } from 'vitest'
import type { Drop } from '../api'
import { makeDrop } from '../test/fixtures'
import { DropCard } from './DropCard'

// DropCard contains a link: it needs a router.
function renderCard(drop: Drop) {
  return render(
    <MemoryRouter>
      <DropCard drop={drop} />
    </MemoryRouter>,
  )
}

describe('DropCard', () => {
  it('shows the product, the price and the remaining stock', () => {
    renderCard(makeDrop({ id: 3, price_cents: 18000, remaining: 42, stock: 100 }))

    expect(screen.getByRole('link', { name: 'Air Max 1 « Laval »' })).toHaveAttribute(
      'href',
      '/drops/3',
    )
    expect(screen.getByText(/180,00\s€/)).toBeInTheDocument()
    expect(screen.getByText('42 / 100 paires restantes')).toBeInTheDocument()
  })

  it.each([
    ['live', 'En vente'],
    ['sold_out', 'Épuisé'],
    ['upcoming', 'À venir'],
  ] as const)('shows the label of the %s status', (status, label) => {
    renderCard(makeDrop({ status, opens_at: '2100-01-01T09:00:00Z' }))

    expect(screen.getByText(label)).toBeInTheDocument()
  })
})
