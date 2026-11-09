import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import * as api from '../api'
import { makeDrop } from '../test/fixtures'
import { DropDetailPage } from './DropDetailPage'

vi.mock('../api', async (importOriginal) => ({
  ...(await importOriginal<typeof import('../api')>()),
  getDrop: vi.fn(),
  placeOrder: vi.fn(),
}))

function renderPage() {
  return render(
    <MemoryRouter initialEntries={['/drops/1']}>
      <Routes>
        <Route path="/drops/:id" element={<DropDetailPage />} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('DropDetailPage', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('orders a pair and shows the new stock', async () => {
    const drop = makeDrop({ remaining: 2 })
    vi.mocked(api.getDrop).mockResolvedValue(drop)
    vi.mocked(api.placeOrder).mockResolvedValue({
      id: 7,
      drop_id: 1,
      created_at: '2026-11-09T09:00:00Z',
      drop: { ...drop, remaining: 1 },
    })
    renderPage()

    await userEvent.click(await screen.findByRole('button', { name: 'Commander' }))

    expect(api.placeOrder).toHaveBeenCalledWith(1)
    expect(await screen.findByRole('status')).toHaveTextContent('Commande n° 7 confirmée')
    expect(screen.getByTestId('remaining')).toHaveTextContent('1 / 100 paires restantes')
  })

  it('disables the button when the drop is sold out', async () => {
    vi.mocked(api.getDrop).mockResolvedValue(makeDrop({ remaining: 0, status: 'sold_out' }))
    renderPage()
    expect(await screen.findByRole('button', { name: 'Épuisé' })).toBeDisabled()
  })

  it('shows the API error when the order is refused', async () => {
    vi.mocked(api.getDrop).mockResolvedValue(makeDrop({ remaining: 1 }))
    vi.mocked(api.placeOrder).mockRejectedValue(
      new api.ApiError(409, 'Le drop 1 est épuisé'),
    )
    renderPage()

    await userEvent.click(await screen.findByRole('button', { name: 'Commander' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Le drop 1 est épuisé')
    expect(api.getDrop).toHaveBeenCalledTimes(2)
  })
})
