import { useState } from 'react'
import './App.css'
import { generateResearchReport } from './api'


const exampleQueries = [
  'Analyze the electric vehicle market in India in 2025',
  'Analyze the AI market in India in 2025',
  'Analyze the renewable energy market in India',
]


const pipelineStages = [
  {
    icon: '◈',
    title: 'RAG Memory',
    description: 'Retrieving relevant historical intelligence',
  },
  {
    icon: '◇',
    title: 'Planner',
    description: 'Breaking the research question into tasks',
  },
  {
    icon: '⌕',
    title: 'Research Agents',
    description: 'Market, company and trend research',
  },
  {
    icon: '✓',
    title: 'Critic',
    description: 'Validating research evidence',
  },
  {
    icon: '◆',
    title: 'Analyst',
    description: 'Deriving strategic insights',
  },
  {
    icon: '▣',
    title: 'Report',
    description: 'Generating final intelligence',
  },
]


function ReportList({ items, emptyMessage }) {
  if (!items || items.length === 0) {
    return (
      <div className="empty-section">
        {emptyMessage}
      </div>
    )
  }

  return (
    <ul className="report-list">
      {items.map((item, index) => (
        <li key={index}>
          <span className="bullet">•</span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}


function App() {
  const [query, setQuery] = useState('')
  const [report, setReport] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)


  const handleSubmit = async (event) => {
    event.preventDefault()

    const trimmedQuery = query.trim()

    if (trimmedQuery.length < 3) {
      setError('Please enter a research question with at least 3 characters.')
      setReport(null)
      return
    }

    setIsLoading(true)
    setError('')
    setReport(null)
    setCopied(false)

    try {
      const data = await generateResearchReport(trimmedQuery)

      console.log('Research response:', data)

      if (!data || !data.report) {
        throw new Error('No report returned from the backend.')
      }

      setReport(data.report)
    } catch (err) {
      console.error('Research request failed:', err)

      setError(
        err.message ||
        'Unable to generate the research report. Please try again.'
      )
    } finally {
      setIsLoading(false)
    }
  }


  const handleExampleQuery = (example) => {
    setQuery(example)
    setError('')
  }


  const handleNewResearch = () => {
    setReport(null)
    setError('')
    setCopied(false)

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }


  const handleCopyReport = async () => {
    if (!report) return

    const reportText = `
${report.title}

EXECUTIVE SUMMARY
${report.executive_summary}

MARKET ANALYSIS
${(report.market_analysis || []).map(item => `• ${item}`).join('\n')}

COMPETITIVE LANDSCAPE
${(report.competitive_landscape || []).map(item => `• ${item}`).join('\n')}

TREND ANALYSIS
${(report.trend_analysis || []).map(item => `• ${item}`).join('\n')}

GROWTH DRIVERS
${(report.growth_drivers || []).map(item => `• ${item}`).join('\n')}

RISKS
${(report.risks || []).map(item => `• ${item}`).join('\n')}

OPPORTUNITIES
${(report.opportunities || []).map(item => `• ${item}`).join('\n')}

STRATEGIC OUTLOOK
${report.strategic_outlook}
`.trim()

    try {
      await navigator.clipboard.writeText(reportText)

      setCopied(true)

      setTimeout(() => {
        setCopied(false)
      }, 2000)
    } catch (err) {
      console.error('Copy failed:', err)
    }
  }


  return (
    <div className="app">

      {/* ================================= */}
      {/* NAVBAR                            */}
      {/* ================================= */}

      <header className="navbar">

        <div className="brand">

          <div className="brand-icon">
            MI
          </div>

          <div className="brand-text">
            <strong>Market Intelligence</strong>
            <span>Autonomous Research Platform</span>
          </div>

        </div>


        <div className="system-status">

          <span className="status-dot"></span>

          <span>
            System Online
          </span>

        </div>

      </header>


      {/* ================================= */}
      {/* MAIN CONTENT                      */}
      {/* ================================= */}

      <main className="main-container">

        {!report && !isLoading && (

          <section className="landing-section">

            {/* HERO */}

            <div className="hero">

              <div className="hero-badge">

                <span className="badge-pulse"></span>

                Autonomous Multi-Agent Intelligence

              </div>


              <h1>

                Turn Market Questions Into

                <span className="gradient-text">
                  Actionable Intelligence
                </span>

              </h1>


              <p className="hero-description">

                Research markets, companies, and emerging trends with
                autonomous AI agents, evidence validation, strategic
                analysis, and persistent RAG-powered memory.

              </p>

            </div>


            {/* QUERY BOX */}

            <form
              className="research-box"
              onSubmit={handleSubmit}
            >

              <div className="research-box-top">

                <div className="input-label">
                  RESEARCH QUESTION
                </div>

                <div className="input-status">
                  AI-powered
                </div>

              </div>


              <textarea
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="What market would you like to investigate?"
                rows={5}
                disabled={isLoading}
              />


              <div className="research-box-bottom">

                <div className="query-hint">

                  <span className="hint-icon">
                    ↳
                  </span>

                  Ask about a market, company, industry, or trend.

                </div>


                <button
                  className="generate-button"
                  type="submit"
                  disabled={isLoading}
                >

                  <span>
                    Generate Intelligence
                  </span>

                  <span className="button-arrow">
                    →
                  </span>

                </button>

              </div>

            </form>


            {/* EXAMPLE QUERIES */}

            <div className="examples">

              <div className="examples-title">
                TRY AN EXAMPLE
              </div>


              <div className="example-list">

                {exampleQueries.map((example, index) => (

                  <button
                    key={index}
                    className="example-chip"
                    onClick={() => handleExampleQuery(example)}
                    type="button"
                  >

                    {example}

                  </button>

                ))}

              </div>

            </div>


            {/* CAPABILITIES */}

            <div className="capabilities">

              <div className="capability-card">

                <div className="capability-icon">
                  ⌕
                </div>

                <div>
                  <h3>
                    Autonomous Research
                  </h3>

                  <p>
                    Specialized agents independently gather market,
                    company and trend intelligence.
                  </p>
                </div>

              </div>


              <div className="capability-card">

                <div className="capability-icon">
                  ✓
                </div>

                <div>
                  <h3>
                    Evidence Validation
                  </h3>

                  <p>
                    A dedicated critic agent evaluates relevance,
                    evidence quality and source reliability.
                  </p>
                </div>

              </div>


              <div className="capability-card">

                <div className="capability-icon">
                  ◈
                </div>

                <div>
                  <h3>
                    Persistent RAG Memory
                  </h3>

                  <p>
                    Previous intelligence is stored and retrieved
                    to provide useful historical context.
                  </p>
                </div>

              </div>

            </div>

          </section>

        )}


        {/* ================================= */}
        {/* ERROR                             */}
        {/* ================================= */}

        {error && !isLoading && (

          <div className="error-box">

            <div className="error-icon">
              !
            </div>

            <div>
              <strong>
                Research failed
              </strong>

              <p>
                {error}
              </p>
            </div>

          </div>

        )}


        {/* ================================= */}
        {/* LOADING                           */}
        {/* ================================= */}

        {isLoading && (

          <section className="loading-section">

            <div className="loading-header">

              <div className="loading-orb">
                <div className="loading-ring"></div>
                <span>AI</span>
              </div>


              <div>

                <div className="section-eyebrow">
                  AUTONOMOUS RESEARCH
                </div>

                <h2>
                  Generating Market Intelligence
                </h2>

                <p>
                  Multiple AI agents are researching, validating,
                  analyzing, and synthesizing your request.
                </p>

              </div>

            </div>


            <div className="loading-pipeline">

              {pipelineStages.map((stage, index) => (

                <div
                  className="loading-stage"
                  key={stage.title}
                >

                  <div className="stage-number">
                    0{index + 1}
                  </div>


                  <div className="stage-icon">
                    {stage.icon}
                  </div>


                  <div className="stage-content">

                    <strong>
                      {stage.title}
                    </strong>

                    <span>
                      {stage.description}
                    </span>

                  </div>


                  <div className="stage-indicator">
                    <span></span>
                  </div>

                </div>

              ))}

            </div>


            <div className="loading-note">

              <span className="loading-note-dot"></span>

              This process may take a little while because the system
              performs live research and evidence validation.

            </div>

          </section>

        )}


        {/* ================================= */}
        {/* REPORT                            */}
        {/* ================================= */}

        {report && (

          <section className="report-section">


            {/* REPORT TOP BAR */}

            <div className="report-toolbar">

              <button
                className="toolbar-button"
                onClick={handleNewResearch}
              >
                ← New Research
              </button>


              <div className="toolbar-actions">

                <button
                  className="toolbar-button"
                  onClick={handleCopyReport}
                >

                  {copied ? '✓ Copied' : 'Copy Report'}

                </button>


                <button
                  className="toolbar-button primary-toolbar-button"
                  onClick={() => window.print()}
                >
                  Print Report
                </button>

              </div>

            </div>


            {/* RESEARCH PIPELINE */}

            <div className="pipeline-card">

              <div className="pipeline-header">

                <div>

                  <div className="section-eyebrow">
                    RESEARCH PIPELINE
                  </div>

                  <h3>
                    Autonomous intelligence workflow
                  </h3>

                </div>


                <div className="complete-badge">

                  <span>
                    ✓
                  </span>

                  Pipeline Complete

                </div>

              </div>


              <div className="pipeline-track">

                {pipelineStages.map((stage, index) => (

                  <div
                    className="pipeline-item"
                    key={stage.title}
                  >

                    <div className="pipeline-item-icon">
                      {stage.icon}
                    </div>

                    <strong>
                      {stage.title}
                    </strong>

                    <span>
                      Complete
                    </span>

                    {index < pipelineStages.length - 1 && (

                      <div className="pipeline-connector">
                        →
                      </div>

                    )}

                  </div>

                ))}

              </div>

            </div>


            {/* REPORT HEADER */}

            <article className="report-hero">

              <div className="report-eyebrow">
                GENERATED INTELLIGENCE
              </div>


              <h1>
                {report.title}
              </h1>


              <div className="report-divider"></div>


              <p>
                {report.executive_summary}
              </p>

            </article>


            {/* REPORT GRID */}

            <div className="report-grid">


              {/* MARKET */}

              <article className="report-card market-card">

                <div className="card-header">

                  <div className="card-icon">
                    ◉
                  </div>

                  <div>
                    <span>
                      01
                    </span>

                    <h2>
                      Market Analysis
                    </h2>
                  </div>

                </div>


                <ReportList
                  items={report.market_analysis}
                  emptyMessage="No market analysis was returned."
                />

              </article>


              {/* COMPETITIVE */}

              <article className="report-card competitive-card">

                <div className="card-header">

                  <div className="card-icon">
                    ◆
                  </div>

                  <div>
                    <span>
                      02
                    </span>

                    <h2>
                      Competitive Landscape
                    </h2>
                  </div>

                </div>


                <ReportList
                  items={report.competitive_landscape}
                  emptyMessage="No competitive intelligence was returned."
                />

              </article>


              {/* TRENDS */}

              <article className="report-card trend-card">

                <div className="card-header">

                  <div className="card-icon">
                    ↗
                  </div>

                  <div>
                    <span>
                      03
                    </span>

                    <h2>
                      Trend Analysis
                    </h2>
                  </div>

                </div>


                <ReportList
                  items={report.trend_analysis}
                  emptyMessage="No trend analysis was returned."
                />

              </article>


              {/* GROWTH */}

              <article className="report-card growth-card">

                <div className="card-header">

                  <div className="card-icon">
                    ↑
                  </div>

                  <div>
                    <span>
                      04
                    </span>

                    <h2>
                      Growth Drivers
                    </h2>

                  </div>

                </div>


                <ReportList
                  items={report.growth_drivers}
                  emptyMessage="No growth drivers were identified."
                />

              </article>


              {/* RISKS */}

              <article className="report-card risk-card">

                <div className="card-header">

                  <div className="card-icon">
                    !
                  </div>

                  <div>
                    <span>
                      05
                    </span>

                    <h2>
                      Risks
                    </h2>

                  </div>

                </div>


                <ReportList
                  items={report.risks}
                  emptyMessage="No major risks were identified."
                />

              </article>


              {/* OPPORTUNITIES */}

              <article className="report-card opportunity-card">

                <div className="card-header">

                  <div className="card-icon">
                    ✦
                  </div>

                  <div>
                    <span>
                      06
                    </span>

                    <h2>
                      Opportunities
                    </h2>

                  </div>

                </div>


                <ReportList
                  items={report.opportunities}
                  emptyMessage="No specific opportunities were identified."
                />

              </article>

            </div>


            {/* STRATEGIC OUTLOOK */}

            <article className="strategic-card">

              <div className="strategic-header">

                <div className="strategic-icon">
                  ◎
                </div>

                <div>

                  <div className="section-eyebrow">
                    FORWARD-LOOKING ASSESSMENT
                  </div>

                  <h2>
                    Strategic Outlook
                  </h2>

                </div>

              </div>


              <p>
                {report.strategic_outlook}
              </p>

            </article>


            {/* REPORT FOOTER */}

            <div className="report-footer">

              <div>

                <span className="footer-label">
                  GENERATED BY
                </span>

                <strong>
                  Autonomous Multi-Agent Market Intelligence System
                </strong>

              </div>


              <div className="footer-agents">

                <span>Planner</span>
                <span>Research Agents</span>
                <span>Critic</span>
                <span>Analyst</span>
                <span>RAG</span>

              </div>

            </div>

          </section>

        )}

      </main>


      {/* ================================= */}
      {/* FOOTER                            */}
      {/* ================================= */}

      <footer className="app-footer">

        <div>
          Autonomous Multi-Agent Market Intelligence System
        </div>

        <div>
          LangGraph · RAG · Web Research · Evidence Validation
        </div>

      </footer>

    </div>
  )
}


export default App