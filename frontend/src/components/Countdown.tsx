import { useEffect, useState } from 'react'

function remainingTime(milliseconds: number): string {
  const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000))
  const days = Math.floor(totalSeconds / 86400)
  const hours = Math.floor((totalSeconds % 86400) / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = totalSeconds % 60
  const pad = (value: number) => String(value).padStart(2, '0')
  const clock = `${pad(hours)} h ${pad(minutes)} min ${pad(seconds)} s`
  return days > 0 ? `${days} j ${clock}` : clock
}

/** Time left before a drop opens, refreshed every second. */
export function Countdown({ opensAt }: { opensAt: string }) {
  const target = new Date(opensAt).getTime()
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(timer)
  }, [])

  if (now >= target) {
    return <p className="countdown countdown--open">C'est ouvert !</p>
  }
  return (
    <p className="countdown" aria-live="off">
      Ouverture dans <time dateTime={opensAt}>{remainingTime(target - now)}</time>
    </p>
  )
}
