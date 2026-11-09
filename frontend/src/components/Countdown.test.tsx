import { act, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { Countdown } from './Countdown'

describe('Countdown', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-11-09T09:00:00Z'))
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('shows the time left before the opening', () => {
    render(<Countdown opensAt="2026-11-11T10:30:15Z" />)
    expect(screen.getByText('2 j 01 h 30 min 15 s')).toBeInTheDocument()
  })

  it('ticks every second', () => {
    render(<Countdown opensAt="2026-11-09T09:01:00Z" />)
    expect(screen.getByText('00 h 01 min 00 s')).toBeInTheDocument()
    act(() => {
      vi.advanceTimersByTime(1000)
    })
    expect(screen.getByText('00 h 00 min 59 s')).toBeInTheDocument()
  })

  it('never shows a negative time once the drop is open', () => {
    render(<Countdown opensAt="2026-11-09T09:00:02Z" />)
    act(() => {
      vi.advanceTimersByTime(5000)
    })
    expect(screen.getByText("C'est ouvert !")).toBeInTheDocument()
  })
})
