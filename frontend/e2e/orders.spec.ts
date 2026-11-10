import { expect, test, type APIRequestContext } from '@playwright/test'

// Each test creates its own drop through the API (proxied by nginx under /api),
// so it never depends on the demo data or on another test.
async function createDrop(request: APIRequestContext, stock: number): Promise<number> {
  const response = await request.post('/api/drops', {
    data: {
      product: `Drop E2E ${Date.now()}`,
      price_cents: 15000,
      stock,
      opens_at: new Date(Date.now() - 60_000).toISOString(),
    },
  })
  expect(response.status()).toBe(201)
  return (await response.json()).id
}

test('commander décrémente le stock', async ({ page, request }) => {
  const id = await createDrop(request, 5)
  await page.goto(`/drops/${id}`)
  await expect(page.getByTestId('remaining')).toHaveText('5 / 5 paires restantes')

  await page.getByRole('button', { name: 'Commander' }).click()

  await expect(page.getByRole('status')).toContainText('confirmée')
  await expect(page.getByTestId('remaining')).toHaveText('4 / 5 paires restantes')
})

test('un drop épuisé désactive le bouton', async ({ page, request }) => {
  const id = await createDrop(request, 1)
  const order = await request.post(`/api/drops/${id}/orders`)
  expect(order.status()).toBe(201)

  await page.goto(`/drops/${id}`)

  await expect(page.getByTestId('remaining')).toHaveText('0 / 1 paires restantes')
  await expect(page.getByRole('button', { name: 'Épuisé' })).toBeDisabled()
})
