/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL of the API. Defaults to /api (same origin, proxied by nginx or Vite). */
  readonly VITE_API_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
