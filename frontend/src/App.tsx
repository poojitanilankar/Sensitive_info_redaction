
import './App.css'

function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">S</div>
          <div>
            <h2>SENTINEL</h2>
            <span>INFORMATION SHIELD</span>
          </div>
        </div>

        <p className="menu-label">WORKSPACE</p>
        <nav>
          <a className="active" href="#dashboard">▦ Dashboard</a>
          <a href="#scanner">⌕ Document Scanner</a>
          <a href="#results">▤ Detection Results</a>
          <a href="#redaction">◈ Redaction Center</a>
        </nav>

        <div className="sidebar-bottom">
          <span className="status-dot"></span>
          LOCAL PROCESSING ACTIVE
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div>
            <p className="eyebrow">SECURE WORKSPACE / OVERVIEW</p>
            <h1>Security Dashboard</h1>
          </div>
          <div className="secure-badge">🔒 100% Local Processing</div>
        </header>

        <section className="welcome">
          <div>
            <p className="eyebrow">WELCOME TO SENTINEL</p>
            <h2>Protect your sensitive information.</h2>
            <p>Scan documents, identify sensitive data, and redact it securely.</p>
          </div>
          <div className="shield-art">⬡</div>
        </section>

        <section className="stats">
          <div className="stat-card">
            <span>DOCUMENTS SCANNED</span>
            <h2>0</h2>
            <p>Total documents processed</p>
          </div>
          <div className="stat-card">
            <span>SENSITIVE ITEMS FOUND</span>
            <h2>0</h2>
            <p>Across all documents</p>
          </div>
          <div className="stat-card">
            <span>DOCUMENTS PROTECTED</span>
            <h2>0</h2>
            <p>Successfully redacted</p>
          </div>
        </section>

        <section className="scanner" id="scanner">
          <div className="section-heading">
            <div>
              <p className="eyebrow">GET STARTED</p>
              <h2>Document Scanner</h2>
            </div>
            <span className="file-tag">PDF · DOCX · TXT · JPG · PNG</span>
          </div>

          <label className="upload-area">
            <div className="upload-icon">↑</div>
            <h3>Upload a document</h3>
            <p>Choose a file to scan for sensitive information.</p>
            <span className="upload-button">Choose File</span>
            <input
              type="file"
              accept=".pdf,.docx,.txt,.jpg,.jpeg,.png"
              hidden
              onChange={(event) => {
                const file = event.target.files?.[0]
                if (file) alert(`Selected: ${file.name}`)
              }}
            />
          </label>
        </section>

        <footer>
          <span>SENTINEL © 2026</span>
          <span>PRIVACY FIRST · SECURITY ALWAYS</span>
        </footer>
      </main>
    </div>
  )
}

export default App
