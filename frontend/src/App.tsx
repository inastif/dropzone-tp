import { BrowserRouter, Link, Route, Routes } from 'react-router'
import { DropDetailPage } from './pages/DropDetailPage'
import { DropListPage } from './pages/DropListPage'

export function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <header className="topbar">
        <Link to="/" className="logo">
          Drop<span>Zone</span>
        </Link>
        <span className="tagline">Sneakers en édition limitée</span>
      </header>
      <main className="container">
        <Routes>
          <Route path="/" element={<DropListPage />} />
          <Route path="/drops/:id" element={<DropDetailPage />} />
          <Route path="*" element={<p>Page introuvable.</p>} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}
