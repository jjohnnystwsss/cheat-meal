import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const CUISINES = [
  { value: 'all', label: '全部' },
  { value: 'fast_food', label: '速食' },
  { value: 'taiwanese', label: '台式' },
  { value: 'japanese', label: '日式' },
  { value: 'convenience_store', label: '超商' },
  { value: 'western', label: '西式' },
]

const EXCLUDE_OPTIONS = [
  { value: 'beef', label: '不吃牛' },
  { value: 'pork', label: '不吃豬' },
  { value: 'spicy', label: '不吃辣' },
  { value: 'fish', label: '不吃魚' },
]

const ROLE_LABEL = { main: '主食', side: '配餐', drink: '飲料', dessert: '甜點' }

function ComboCard({ combo, index }) {
  return (
    <div className="card">
      <div className="card-header">
        <span className="card-index">{index + 1}</span>
        <h3 className="card-title">{combo.name}</h3>
      </div>

      <ul className="item-list">
        {combo.items.map(item => (
          <li key={item.id} className="item-row">
            <span className="role-badge">{ROLE_LABEL[item.meal_role] ?? item.meal_role}</span>
            <span className="item-name">{item.name}</span>
            <span className="item-cal">{item.calories} kcal</span>
          </li>
        ))}
      </ul>

      <div className="card-footer">
        <div className="stats">
          <div className="stat">
            <span className="stat-val">{combo.total_calories}</span>
            <span className="stat-unit">kcal</span>
          </div>
          <div className="stat">
            <span className="stat-val">NT$ {combo.total_price}</span>
            <span className="stat-unit">預估價格</span>
          </div>
        </div>
        <p className="reason">{combo.reason}</p>
      </div>
    </div>
  )
}

export default function App() {
  const [calories, setCalories] = useState(1200)
  const [cuisine, setCuisine] = useState('all')
  const [excludeTags, setExcludeTags] = useState([])
  const [includeDrink, setIncludeDrink] = useState(true)
  const [includeDessert, setIncludeDessert] = useState(true)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const toggleTag = tag =>
    setExcludeTags(prev => prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag])

  const submit = async (e) => {
    e?.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API_URL}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_calories: calories,
          cuisine,
          exclude_tags: excludeTags,
          include_drink: includeDrink,
          include_dessert: includeDessert,
        }),
      })
      if (!res.ok) throw new Error()
      const data = await res.json()
      setResults(data.recommendations)
    } catch {
      setError('無法連線到後端，請確認 backend 是否已啟動（port 8000）')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Cheat Meal Picker</h1>
        <p>輸入今天的熱量額度，快速得到最爽的 cheat meal 建議</p>
      </header>

      <main>
        <form className="form-card" onSubmit={submit}>
          {/* Calories */}
          <div className="field">
            <label className="field-label">目標熱量</label>
            <div className="cal-row">
              <input
                type="range" min="500" max="3000" step="50"
                value={calories}
                onChange={e => setCalories(Number(e.target.value))}
                className="slider"
              />
              <div className="cal-display">
                <input
                  type="number" min="500" max="3000"
                  value={calories}
                  onChange={e => setCalories(Number(e.target.value))}
                  className="cal-input"
                />
                <span className="cal-unit">kcal</span>
              </div>
            </div>
          </div>

          {/* Cuisine */}
          <div className="field">
            <label className="field-label">餐點類型</label>
            <div className="pill-group">
              {CUISINES.map(c => (
                <button
                  type="button" key={c.value}
                  className={`pill ${cuisine === c.value ? 'pill-active' : ''}`}
                  onClick={() => setCuisine(c.value)}
                >{c.label}</button>
              ))}
            </div>
          </div>

          {/* Exclude */}
          <div className="field">
            <label className="field-label">飲食限制</label>
            <div className="check-group">
              {EXCLUDE_OPTIONS.map(opt => (
                <label key={opt.value} className="check-label">
                  <input
                    type="checkbox"
                    checked={excludeTags.includes(opt.value)}
                    onChange={() => toggleTag(opt.value)}
                  />
                  {opt.label}
                </label>
              ))}
            </div>
          </div>

          {/* Toggles */}
          <div className="field toggles-row">
            <label className="toggle-label">
              <input type="checkbox" checked={includeDrink} onChange={e => setIncludeDrink(e.target.checked)} />
              包含飲料
            </label>
            <label className="toggle-label">
              <input type="checkbox" checked={includeDessert} onChange={e => setIncludeDessert(e.target.checked)} />
              包含甜點
            </label>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? '產生中…' : '幫我選！'}
          </button>
        </form>

        {error && <div className="error-box">{error}</div>}

        {results && (
          <section className="results">
            <div className="results-header">
              <h2>推薦組合</h2>
              <button className="btn-outline" onClick={submit} disabled={loading}>
                重新推薦
              </button>
            </div>
            {results.length === 0
              ? <p className="empty">找不到符合條件的組合，試試放寬限制</p>
              : <div className="card-list">
                  {results.map((combo, i) => <ComboCard key={i} combo={combo} index={i} />)}
                </div>
            }
          </section>
        )}
      </main>
    </div>
  )
}
