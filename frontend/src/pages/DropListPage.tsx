import { useEffect, useState } from 'react'
import { listDrops, type Drop, type DropStatus } from '../api'
import { DropCard } from '../components/DropCard'

const FILTERS: { label: string; value?: DropStatus }[] = [
  { label: 'Tous' },
  { label: 'En vente', value: 'live' },
  { label: 'À venir', value: 'upcoming' },
  { label: 'Épuisés', value: 'sold_out' },
]

const REFRESH_INTERVAL_MS = 10_000

export function DropListPage() {
  const [filter, setFilter] = useState<DropStatus | undefined>()
  const [drops, setDrops] = useState<Drop[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    const load = () =>
      listDrops(filter)
        .then((data) => {
          if (active) {
            setDrops(data)
            setError(null)
          }
        })
        .catch((err: Error) => active && setError(err.message))
    load()
    // Stock moves fast during a drop: refresh the list regularly.
    const timer = setInterval(load, REFRESH_INTERVAL_MS)
    return () => {
      active = false
      clearInterval(timer)
    }
  }, [filter])

  return (
    <section>
      <h1>Les drops</h1>
      <nav className="filters" aria-label="Filtrer par statut">
        {FILTERS.map(({ label, value }) => (
          <button
            key={label}
            type="button"
            className="filter"
            aria-pressed={filter === value}
            onClick={() => setFilter(value)}
          >
            {label}
          </button>
        ))}
      </nav>
      {error && (
        <p role="alert" className="alert">
          {error}
        </p>
      )}
      {drops === null && !error && <p>Chargement…</p>}
      {drops?.length === 0 && <p>Aucun drop pour le moment.</p>}
      <div className="grid">
        {drops?.map((drop) => (
          <DropCard key={drop.id} drop={drop} />
        ))}
      </div>
    </section>
  )
}
