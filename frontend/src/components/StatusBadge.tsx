import type { DropStatus } from '../api'

const LABELS: Record<DropStatus, string> = {
  upcoming: 'À venir',
  live: 'En vente',
  sold_out: 'Épuisé',
}

export function StatusBadge({ status }: { status: DropStatus }) {
  return <span className={`badge badge--${status}`}>{LABELS[status]}</span>
}
