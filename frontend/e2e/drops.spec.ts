import { expect, test } from '@playwright/test'

// End-to-end tests: they run against the whole stack (front, API, database).

test('la liste des drops s’affiche', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: 'Les drops' })).toBeVisible()
  await expect(page.getByTestId('drop-card').first()).toBeVisible()
})
