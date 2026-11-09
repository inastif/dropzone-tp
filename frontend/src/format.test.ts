import { describe, expect, it } from 'vitest'
import { formatPrice } from './format'

// Intl uses narrow no-break spaces: compare with plain spaces.
const plain = (text: string) => text.replace(/\s/g, ' ')

describe('formatPrice', () => {
  it('formats cents as euros', () => {
    expect(plain(formatPrice(18000))).toBe('180,00 €')
  })

  it('keeps the cents', () => {
    expect(plain(formatPrice(1999))).toBe('19,99 €')
  })

  it('groups thousands', () => {
    expect(plain(formatPrice(123456))).toBe('1 234,56 €')
  })
})
