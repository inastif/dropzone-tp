import { Link } from 'react-router'
import type { Drop } from '../api'
import { formatPrice } from '../format'
import { Countdown } from './Countdown'
import { StatusBadge } from './StatusBadge'

export function DropCard({ drop }: { drop: Drop }) {
  return (
    <article className="card" data-testid="drop-card">
      <header className="card__header">
        <StatusBadge status={drop.status} />
        <span className="card__price">{formatPrice(drop.price_cents)}</span>
      </header>
      <h2 className="card__title">
        <Link to={`/drops/${drop.id}`}>{drop.product}</Link>
      </h2>
      <p className="card__stock">
        {drop.remaining} / {drop.stock} paires restantes
      </p>
      {drop.status === 'upcoming' && <Countdown opensAt={drop.opens_at} />}
    </article>
  )
}
