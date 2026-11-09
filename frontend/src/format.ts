const priceFormat = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })

/** Prices travel in cents (integers): 18000 is displayed as « 180,00 € ». */
export function formatPrice(cents: number): string {
  return priceFormat.format(cents / 100)
}

const dateFormat = new Intl.DateTimeFormat('fr-FR', {
  dateStyle: 'long',
  timeStyle: 'short',
  timeZone: 'Europe/Paris',
})

export function formatDate(iso: string): string {
  return dateFormat.format(new Date(iso))
}
