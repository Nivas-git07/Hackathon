import { useEffect } from 'react'
import '../style.css'
import '../command.css'
import '../modules.css'
import '../simple.css'

const LEGACY_SCRIPT_ID = 'ecomind-application'

export default function App() {
  useEffect(() => {
    window.__ECOMIND_API_URL__ = (import.meta.env.VITE_API_URL?.trim() || 'http://127.0.0.1:8000').replace(/\/$/, '')

    if (document.getElementById(LEGACY_SCRIPT_ID)) return
    const script = document.createElement('script')
    script.id = LEGACY_SCRIPT_ID
    script.src = '/app.js'
    script.async = true
    document.body.appendChild(script)

    return () => {
      script.remove()
    }
  }, [])

  return (
    <div id="app" aria-live="polite">
      <div className="boot">Starting EcoMind…</div>
    </div>
  )
}
