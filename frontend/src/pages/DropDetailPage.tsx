import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router'
import { getDrop, placeOrder, type Drop } from '../api'
import { Countdown } from '../components/Countdown'
import { StatusBadge } from '../components/StatusBadge'
import { formatDate, formatPrice } from '../format'

const BUTTON_LABELS = {
  live: 'Commander',
  upcoming: 'Pas encore ouvert',
  sold_out: 'Épuisé',
} as const

export function DropDetailPage() {
  const id = Number(useParams().id)
  const [drop, setDrop] = useState<Drop | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)
  const [ordering, setOrdering] = useState(false)

  const load = useCallback(
    () =>
      getDrop(id)
        .then(setDrop)
        .catch((err: Error) => setError(err.message)),
    [id],
  )

  useEffect(() => {
    load()
  }, [load])

  async function order() {
    setOrdering(true)
    setError(null)
    setMessage(null)
    try {
      const created = await placeOrder(id)
      setDrop(created.drop)
      setMessage(
        `Commande n° ${created.id} confirmée : une paire de ${created.drop.product} vous est réservée.`,
      )
    } catch (err) {
      setError((err as Error).message)
      await load()
    } finally {
      setOrdering(false)
    }
  }

  return (
    <section className="detail">
      <Link to="/" className="back">
        ← Tous les drops
      </Link>
      {error && (
        <p role="alert" className="alert">
          {error}
        </p>
      )}
      {message && (
        <p role="status" className="success">
          {message}
        </p>
      )}
      {drop && (
        <>
          <StatusBadge status={drop.status} />
          <h1>{drop.product}</h1>
          {drop.description && <p className="detail__description">{drop.description}</p>}
          <dl className="detail__facts">
            <dt>Prix</dt>
            <dd>{formatPrice(drop.price_cents)}</dd>
            <dt>Ouverture</dt>
            <dd>{formatDate(drop.opens_at)}</dd>
            <dt>Stock</dt>
            <dd data-testid="remaining">
              {drop.remaining} / {drop.stock} paires restantes
            </dd>
          </dl>
          {drop.status === 'upcoming' && <Countdown opensAt={drop.opens_at} />}
          <button
            type="button"
            className="order"
            onClick={order}
            disabled={drop.status !== 'live' || ordering}
          >
            {ordering ? 'Commande en cours…' : BUTTON_LABELS[drop.status]}
          </button>
        </>
      )}
    </section>
  )
}
