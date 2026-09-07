import { useState } from 'react'
import {
  LineChart, 
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  Legend,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts'
import './App.css'

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [parsedQuery, setParsedQuery] = useState(null);
  const [loading, setLoading] = useState(false);
  const [resultCount, setResultCount] = useState(20);
  const [currentPage, setCurrentPage] = useState(1);
  const [feedback, setFeedback] = useState(null);
  const [activeView, setActiveView] = useState("search");
  const [metrics, setMetrics] = useState(null);

  const latencyData = (metrics?.latency_history ?? []).map((latency, index) => ({
    query: index + 1,
    latency: latency
  }));

  const intentData = [
    {
      intent: "Browsing",
      searches: metrics?.browsing_queries ?? 0
    },
    {
      intent: "Researching",
      searches: metrics?.researching_queries ?? 0
    },
    {
      intent: "High-intent Inquiry",
      searches: metrics?.high_intent_queries ?? 0
    }
  ]

  const satisfactionData = [
    { name: "Helpful", value: metrics?.positive_feedback ?? 0 },
    { name: "Not Helpful", value: metrics?.negative_feedback ?? 0 }
  ]

  const handleSearch = async () => {
    if (!query.trim()) return

    setCurrentPage(1);
    setFeedback(null);
    setLoading(true);

    try {
      // Parse the search query 
      const parseResponse = await fetch("http://localhost:8000/parse-query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const parsedData = await parseResponse.json();

      // Perform the NLP search
      const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          query,
          top_k: resultCount, 
        }),
      });

      const data = await response.json();

      setResults(data.results);

      setParsedQuery({
        parsed_query: parsedData.parsed_query,
        intent: data.intent,
        confidence: data.confidence,
        search_strategy: data.search_strategy
      })
    }
    catch (error) {
      console.error("Search error:", error);
    } finally {
      setLoading(false);
    }
  }

  const loadMetrics = async () => {
    try {
      const response = await fetch("http://localhost:8000/metrics");
      const data = await response.json();

      setMetrics(data);
    } catch (error) {
      console.error("Metrics error:", error);
    }
  };

  const submitFeedback = async (rating) => {
    const previousRating = feedback;

    // Clicking the currently selected button removes the feedback
    if (previousRating === rating) {
      setFeedback(null);

      try {
        await fetch("http://localhost:8000/feedback", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            rating: null,
            previous_rating: previousRating
          })
        });
      } catch (error) {
        console.error("Feedback error:", error);
      }

      return;
    }

    // Otherwise, set the new rating
    setFeedback(rating);

    try {
      await fetch("http://localhost:8000/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          rating: rating,
          previous_rating: previousRating
        })
      });
    } catch (error) {
      console.error("Feedback error:", error);
    }
  };

  const handleReset = () => {
    setQuery("");
    setResults([]);
    setParsedQuery(null);
    setLoading(false);
    setResultCount(20);
    setCurrentPage(1);
    setFeedback(null);
  }

  const cardsPerPage = 10;

  const totalPages = Math.ceil(results.length / cardsPerPage);
  
  const startIndex = (currentPage - 1) * cardsPerPage;

  const currentResults = results.slice(
    startIndex,
    startIndex + cardsPerPage
  );

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-title">
          🏠 Real Estate NLP Recommendation System
        </div>

        <div className="nav-links">
          <button onClick={() => setActiveView("search")}>
            Search
          </button>
          <button onClick={() => {
            setActiveView("metrics");
            loadMetrics();
            }}
          >
            Metrics
          </button>
        </div>
      </nav>
      {activeView === "search" && (
        <>
        <header className="hero-section">
          <h1>Find Your Perfect Home</h1>

          <p className="subtitle">
            Describe the home you're looking for, and let our NLP system find the best matches.
          </p>

          <div className="search-area">
            <input
              className="search-input"
              type="text"
              placeholder="e.g. 3 bedrooms in Irvine under $700k"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  handleSearch();
                }
              }}
            />

            <button
              className='search-button'
              onClick={handleSearch}
              disabled={loading}
            >
              {loading ? "Searching..." : "Search"}
            </button>

            <button
              className="reset-button"
              onClick={handleReset}
            >
              Reset
            </button>
          </div>
          <div className="result-count-control">
            <label htmlFor="result-count">
              Results to show: <strong>{resultCount}</strong>
            </label>

            <input
              id="result-count"
              type="range"
              min="10"
              max="50"
              step="10"
              value={resultCount}
              onChange={(event) => setResultCount(Number(event.target.value))}
            />
          </div>
        </header>

        {parsedQuery && (
          <>
          <section className="query-analysis">
          <div className="query-intent">
          <span className="query-label">Query Intent</span>
          <strong>{parsedQuery.intent
            .replace(/_/g, " ")
            .replace(/\b\w/g, (letter) => letter.toUpperCase())}
          </strong>
          </div>
            <div className="query-confidence">
              <span className="query-label">Confidence</span>
              <strong>
                {(parsedQuery.confidence * 100).toFixed(2)}%
              </strong>
            </div>

            <div className="query-strategy">
              <span className="query-label">Search Strategy</span>
              <strong>
                {parsedQuery.search_strategy === "hybrid"
                ? "semantic + keyword"
                : parsedQuery.search_strategy.toLowerCase()}
              </strong>
            </div>
          </section>

          <section className="parsed-query">
            <h2>What information was understood:</h2>

            <div className="filter-container">
              {Object.entries(parsedQuery.parsed_query).map(
                ([key, value]) => (
                  <div className="filter-chip" key={key}>
                    <strong>
                      {key
                        .replace(/_/g, " ")
                        .replace(/\b\w/g, (letter) => 
                        letter.toUpperCase()
                      )}
                    </strong>

                    <span>
                      {typeof value === "boolean"
                        ? value ? "Yes" : "No"
                        : String(value)}
                    </span>
                  </div>
                )
              )}
            </div>
          </section>
          </>
        )}

        {results.length > 0 && (
          <section className="results-section">
            <div className="results-header">
              <h2>Recommended Listings</h2>
              <span>{results.length} results</span>
            </div>

            <div className="results-container">
              {currentResults.map((result, index) => (
                <div className="listing-card" key={index}>
                  <div className="listing-number">
                    #{startIndex + index + 1}
                  </div>

                  <div className="listing-id">
                    Listing ID: {result.listing_id}
                  </div>

                  <p className="listing-address">
                    {result.address}, {result.city}, CA, {result.zip}
                  </p>

                  <div className="listing-details">
                    <span>{result.bedrooms} beds</span>
                    <span>{result.bathrooms} baths</span>
                    <span>${result.price?.toLocaleString()}</span>
                    <span>{result.sqft?.toLocaleString()} sqft</span>
                  </div>

                  <p className="listing-summary">
                    {result.summary}
                  </p>

                  <details className="original-remark">
                    <summary>Original Listing Description</summary>
                    <p>{result.remark}</p>
                  </details>

                  <div className="similarity-score">
                    Semantic Match:{" "}
                    <strong>
                      {(result.score * 100).toFixed(2)}%
                    </strong>
                  </div>

                  <div className="compliance-status">
                    {result.compliance.can_publish ? (
                      result.compliance.compliant ? (
                        <span className="compliant">
                          ✓ Fair Housing Compliant
                        </span>
                      ) : (
                        <span className="review">
                          ⚠ Review Recommended
                        </span>
                      )
                    ) : (
                      <span className="blocked">
                        ✕ Publication Blocked
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
            {totalPages > 1 && (
              <div className="pagination">
                <button
                  onClick={() => setCurrentPage(currentPage - 1)}
                  disabled={currentPage === 1}
                >
                  ←
                </button>

                {Array.from({ length: totalPages }, (_, index) => (
                  <button
                    key={index + 1}
                    className={currentPage === index + 1 ? "active-page" : ""}
                    onClick={() => setCurrentPage(index + 1)}
                  >
                    {index + 1}
                  </button>
                ))}

                <button
                  onClick={() => setCurrentPage(currentPage + 1)}
                  disabled={currentPage === totalPages}
                >
                  →
                </button>
              </div>
            )}
              <div className="feedback">
                <p>How useful were these results?</p>

                <button
                  onClick={() => submitFeedback("positive")}
                  className={feedback === "positive" ? "selected" : ""}
                >
                  👍 Helpful
                </button>

                <button
                  onClick={() => submitFeedback("negative")}
                  className={feedback === "negative" ? "selected" : ""}
                >
                  👎 Not Helpful
                </button>
              </div>
          </section>
        )}

        {parsedQuery && results.length === 0 && !loading && (
          <div className="no-results">
            No listings found.
          </div>
        )}
      </> 
      )}
      {activeView === "metrics" && (
        <section className="metrics-page">
          <h1>Metrics Dashboard</h1>
          <p>Monitor search performance and user feedback.</p>

          <div className="metrics-cards">
            <div className="metric-card">
              <span>Total Queries</span>
              <strong>{metrics?.total_queries ?? 0}</strong>
            </div>

            <div className="metric-card">
              <span>Average Latency</span>
              <strong>
                {metrics?.average_latency === null
                  ? <em>Not enough data</em>
                  : `${metrics?.average_latency.toFixed(2)} sec`}
              </strong>
            </div>

            <div className="metric-card">
              <span>Satisfaction Rate</span>
              <strong>
                {metrics?.satisfaction_rate === null
                  ? <em>Not enough data</em>
                  : `${metrics?.satisfaction_rate.toFixed(1)}%`}
              </strong>
            </div>
          </div>

            <div className="metrics-charts">

              <div className="chart-card latency-chart">

                <h2>Search Latency Over Queries</h2>

                {metrics && metrics.latency_history.length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={latencyData}>
                      <CartesianGrid strokeDasharray="3 3" />

                      <XAxis
                        dataKey="query"
                        label={{
                          value: "Query",
                          position: "insideBottom",
                          offset: -5
                        }}
                      />

                      <YAxis
                        label={{
                          value: "Latency (seconds)",
                          angle: -90,
                          position: "insideLeft"
                        }}
                      />

                      <Tooltip />

                      <Line
                        type="monotone"
                        dataKey="latency"
                        stroke="#5f7892"
                        strokeWidth={2}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="not-enough-data">
                    <em>Not enough data</em>
                  </div>
                )}

              </div>

            <div className="chart-row">

              <div className="chart-card">
                <h2>Query Intent Usage</h2>

                {metrics &&
                metrics.browsing_queries +
                metrics.researching_queries +
                metrics.high_intent_queries > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart 
                      data={intentData}
                      layout="vertical"
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" />
                      <YAxis
                        type="category"
                        dataKey="intent"
                        width={130}
                      />
                      <Tooltip />
                      <Bar
                        dataKey="searches"
                        fill="#5f7892"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="not-enough-data">
                    <em>Not enough data</em>
                  </div>
                )}
              </div>

              <div className="chart-card">
                <h2>User Satisfaction</h2>

                {metrics &&
                metrics.positive_feedback + metrics.negative_feedback > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={satisfactionData}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={100}
                        label
                      >
                        <Cell fill="#5f7892" />
                        <Cell fill="#c8d0d8" />
                      </Pie>

                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="not-enough-data">
                    <em>Not enough data</em>
                  </div>
                )}
              </div>

            </div>
            <div className="detailed-metrics">
                <h2>Detailed Metrics</h2>

                <table className="metrics-table">
                  <thead>
                    <tr>
                      <th>Metrics</th>
                      <th>Values</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Total Queries</td>
                      <td>{metrics?.total_queries ?? 0}</td>
                    </tr>

                    <tr>
                      <td>Average Latency</td>
                      <td>
                        {metrics?.average_latency === null
                          ? <em>Not enough data</em>
                          : `${metrics?.average_latency.toFixed(2)} sec`}
                      </td>
                    </tr>

                    <tr>
                      <td>Browsing Queries</td>
                      <td>{metrics?.browsing_queries ?? 0}</td>
                    </tr>

                    <tr>
                      <td>Researching Queries</td>
                      <td>{metrics?.researching_queries ?? 0}</td>
                    </tr>

                    <tr>
                      <td>High-intent Queries</td>
                      <td>{metrics?.high_intent_queries ?? 0}</td>
                    </tr>

                    <tr>
                      <td>Positive Feedback</td>
                      <td>{metrics?.positive_feedback ?? 0}</td>
                    </tr>

                    <tr>
                      <td>Negative Feedback</td>
                      <td>{metrics?.negative_feedback ?? 0}</td>
                    </tr>

                    <tr>
                      <td>Satisfaction Rate</td>
                      <td>
                        {metrics?.satisfaction_rate === null
                          ? <em>Not enough data</em>
                          : `${metrics?.satisfaction_rate.toFixed(1)}%`}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
          </div>

        </section>
      )}
    </div>
  )
}
export default App