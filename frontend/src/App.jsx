
import { useState } from "react";
import {
  LayoutDashboard,
  BriefcaseBusiness,
  FileUp,
  Users,
  Settings,
  Search,
  Bell,
  ArrowUpRight,
  FileText,
  UserCheck,
  Target,
  ChartNoAxesCombined,
  Sparkles,
  Menu,
  X,
  CheckCircle2,
} from "lucide-react";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import { matchResumes } from "./api";
import "./App.css";

const trendData = [
  { month: "Jan", candidates: 25 },
  { month: "Feb", candidates: 38 },
  { month: "Mar", candidates: 32 },
  { month: "Apr", candidates: 55 },
  { month: "May", candidates: 48 },
  { month: "Jun", candidates: 70 },
];

const sourceData = [
  { name: "Job Portals", value: 45 },
  { name: "LinkedIn", value: 30 },
  { name: "Referrals", value: 25 },
];

const COLORS = ["#2563eb", "#7c3aed", "#06b6d4"];


function Sidebar({ active, setActive, menuOpen, setMenuOpen }) {
  const navigation = [
    { name: "Dashboard", icon: LayoutDashboard },
    { name: "Resume Matching", icon: FileUp },
    { name: "Candidates", icon: Users },
  ];

  return (
    <>
      {menuOpen && (
        <div
          className="mobile-overlay"
          onClick={() => setMenuOpen(false)}
        />
      )}

      <aside className={`sidebar ${menuOpen ? "sidebar-open" : ""}`}>
        <div className="sidebar-header">
          <div className="brand-icon">
            <Sparkles size={23} />
          </div>

          <div>
            <h2>TalentAI</h2>
            <span>Recruitment Platform</span>
          </div>

          <button
            className="mobile-close"
            onClick={() => setMenuOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <div className="sidebar-section">
          <p className="sidebar-label">WORKSPACE</p>

          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`nav-item ${
                  active === item.name ? "active" : ""
                }`}
                onClick={() => {
                  setActive(item.name);
                  setMenuOpen(false);
                }}
              >
                <Icon size={19} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </div>

        <div className="sidebar-bottom">
          <button
            className={`nav-item ${
              active === "Settings" ? "active" : ""
            }`}
            onClick={() => {
              setActive("Settings");
              setMenuOpen(false);
            }}
          >
            <Settings size={19} />
            <span>Settings</span>
          </button>

          <div className="profile-card">
            <div className="profile-avatar">HR</div>
            <div>
              <strong>Recruiter</strong>
              <span>Administrator</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

function StatCard({ title, value, subtitle, icon: Icon }) {
  return (
    <div className="stat-card">
      <div className="stat-card-top">
        <span>{title}</span>
        <div className="stat-icon">
          <Icon size={21} />
        </div>
      </div>

      <h2>{value}</h2>
      <p>
        <span className="positive">
          <ArrowUpRight size={15} />
          {subtitle}
        </span>
      </p>
    </div>
  );
}

function CandidateTable({ results }) {
  if (!results.length) {
    return (
      <div className="empty-state">
        <Users size={35} />
        <h3>No candidates analyzed yet</h3>
        <p>Upload resumes to see ranked candidates here.</p>
      </div>
    );
  }

  return (
    <div className="table-wrapper">
      <table className="candidate-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Candidate</th>
            <th>Match Score</th>
            <th>Matched Skills</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {results.map((candidate) => (
            <tr key={candidate.rank}>
              <td>#{candidate.rank}</td>
              <td>
                <strong>{candidate.candidate_name}</strong>
              </td>
              <td>
                <span className="score-badge">
                  {candidate.overall_score}%
                </span>
              </td>
              <td>
                {candidate.matched_skills.join(", ") || "None"}
              </td>
              <td>
                <span className="status-badge">
                  <CheckCircle2 size={14} />
                  Analyzed
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


function Dashboard({ results, filteredResults }) {
  const averageScore = results.length
    ? (
        results.reduce(
          (total, candidate) =>
            total + Number(candidate.overall_score || 0),
          0
        ) / results.length
      ).toFixed(1)
    : "0";

  const topCandidates = results.filter(
    (candidate) => Number(candidate.overall_score) >= 70
  ).length;

  // Actual candidate match scores
  const candidateScoreData = results.slice(0, 8).map(
    (candidate, index) => ({
      candidate:
        candidate.candidate_name || `Candidate ${index + 1}`,
      score: Number(candidate.overall_score || 0)
    })
  );

  // Actual match score distribution
  const scoreDistribution = [
    {
      name: "Strong Match (70%+)",
      value: results.filter(
        (c) => Number(c.overall_score) >= 70
      ).length
    },
    {
      name: "Moderate Match (40–69%)",
      value: results.filter(
        (c) =>
          Number(c.overall_score) >= 40 &&
          Number(c.overall_score) < 70
      ).length
    },
    {
      name: "Low Match (Below 40%)",
      value: results.filter(
        (c) => Number(c.overall_score) < 40
      ).length
    }
  ];

  return (
    <>
      <div className="page-heading">
        <div>
          <h1>Dashboard</h1>
          <p>Overview of your recruitment activities.</p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Candidates"
          value={results.length}
          subtitle="Analyzed resumes"
          icon={Users}
        />

        <StatCard
          title="Average Match Score"
          value={`${averageScore}%`}
          subtitle="Candidate matching"
          icon={Target}
        />

        <StatCard
          title="Top Candidates"
          value={topCandidates}
          subtitle="70% or above"
          icon={UserCheck}
        />

        <StatCard
          title="Resumes Analyzed"
          value={results.length}
          subtitle="Successfully processed"
          icon={FileText}
        />
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <div className="section-heading">
            <h3>Candidate Match Scores</h3>
            <span>Latest analysis</span>
          </div>

          {results.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={candidateScoreData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />
                <XAxis dataKey="candidate" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="score"
                  stroke="#2563eb"
                  fill="#dbeafe"
                  strokeWidth={3}
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <p>No candidate data available. Upload resumes to view scores.</p>
          )}
        </div>

        <div className="chart-card">
          <div className="section-heading">
            <h3>Match Score Distribution</h3>
            <span>Candidate categories</span>
          </div>

          {results.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={scoreDistribution}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={85}
                  label
                >
                  {scoreDistribution.map((entry, index) => (
                    <Cell
                      key={entry.name}
                      fill={COLORS[index]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p>No candidate data available.</p>
          )}
        </div>
      </div>

      <div className="content-card">
        <div className="section-heading">
          <div>
            <h3>Ranked Candidates</h3>
            <p>Results from your latest resume analysis.</p>
          </div>
        </div>

        <CandidateTable results={filteredResults} />
      </div>
    </>
  );
}

function ResumeMatching({ onResults }) {
  const [jobDescription, setJobDescription] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleMatching = async () => {
    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    if (files.length === 0) {
      setError("Please upload at least one resume.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const data = await matchResumes(jobDescription, files);

      onResults(data.ranked_candidates || []);

      setSuccess(
        `Successfully analyzed ${data.successful_matches} resume(s).`
      );
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page-heading">
        <div>
          <h1>AI Resume Matching</h1>
          <p>Compare candidate resumes against your job requirements.</p>
        </div>
      </div>

      <div className="content-card matching-card">
        <div className="form-section">
          <h3>
            <BriefcaseBusiness size={20} />
            Job Description
          </h3>

          <p>
            Enter the role requirements, required skills and
            qualifications.
          </p>

          <textarea
            className="job-description-input"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Example: We are looking for a Python developer with experience in React, FastAPI, SQL and Machine Learning..."
            rows={9}
          />
        </div>

        <div className="form-section">
          <h3>
            <FileUp size={20} />
            Upload Candidate Resumes
          </h3>

          <p>Supported formats: PDF and DOCX.</p>

          <label className="upload-box">
            <FileUp size={34} />
            <strong>Click to upload resumes</strong>
            <span>Select multiple PDF or DOCX files</span>

            <input
              type="file"
              accept=".pdf,.docx"
              multiple
              onChange={(e) => {
                setFiles(Array.from(e.target.files || []));
                setError("");
                setSuccess("");
              }}
            />
          </label>

          <p className="file-count">
            {files.length} resume(s) selected
          </p>

          {files.length > 0 && (
            <div className="selected-files">
              {files.map((file, index) => (
                <div key={`${file.name}-${index}`}>
                  <FileText size={16} />
                  <span>{file.name}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}

        <button
          className="primary-button"
          onClick={handleMatching}
          disabled={loading}
        >
          <Sparkles size={18} />
          {loading ? "Analyzing Resumes..." : "Analyze & Rank Candidates"}
        </button>
      </div>
    </>
  );
}

function CandidateResults({ results }) {
  return (
    <>
      <div className="page-heading">
        <div>
          <h1>Ranked Candidates</h1>
          <p>View candidate profiles and matching analysis.</p>
        </div>
      </div>

      <div className="content-card">
        <CandidateTable results={results} />

        {results.map((candidate) => (
          <div className="candidate-detail" key={candidate.rank}>
            <h3>
              #{candidate.rank} {candidate.candidate_name}
            </h3>

            <p>
              <strong>Email:</strong>{" "}
              {candidate.email || "Not found"}
            </p>

            <p>
              <strong>Phone:</strong>{" "}
              {candidate.phone || "Not found"}
            </p>

            <p>
              <strong>Experience:</strong>{" "}
              {candidate.experience || "Not specified"}
            </p>
            <p>
              <strong>Required Experience:</strong>{" "}
              {candidate.required_experience === "Not specified"
              ? "Not specified"
              : `${candidate.required_experience} years`}
            </p>
            <p>
              <strong>Candidate Experience:</strong>{" "}
              {candidate.candidate_experience} years
            </p>
            <p>
              <strong>Experience Match:</strong>{" "}
              {candidate.experience_score}%
            </p>
            <p>
              <strong>Required Qualification:</strong>{" "}
              {Array.isArray(candidate.required_qualification)
              ? candidate.required_qualification.join(", ")
              : candidate.required_qualification}
            </p>
            <p>
              <strong>Candidate Qualification:</strong>{" "}
              {Array.isArray(candidate.candidate_qualification)
              ? candidate.candidate_qualification.join(", ")
              : candidate.candidate_qualification}
            </p>
            <p>
              <strong>Qualification Match:</strong>{" "}
              {candidate.qualification_score}%
            </p>

            <p>
              <strong>Overall Match:</strong>{" "}
              {candidate.overall_score}%
            </p>

            <p>
              <strong>Semantic Score:</strong>{" "}
              {candidate.semantic_score}%
            </p>

            <p>
              <strong>Skill Score:</strong>{" "}
              {candidate.skill_score}%
            </p>

            <p>
              <strong>Matched Skills:</strong>{" "}
              {candidate.matched_skills?.join(", ") || "None"}
            </p>

            <p>
              <strong>Missing Skills:</strong>{" "}
              {candidate.missing_skills?.join(", ") || "None"}
            </p>
            <div className="candidate-explanation">
              <h4>AI Match Explanation</h4>
              <ul>
                {candidate.explanations?.map((explanation, index) => (
                  <li key={index}>{explanation}</li>
                ))}
              </ul>
            </div>
          </div>
          
        ))}
      </div>
    </>
  );
}


function App() {
  const [active, setActive] = useState("Dashboard");
  const [menuOpen, setMenuOpen] = useState(false);
  const [results, setResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredResults = results.filter((candidate) => {
  const query = searchQuery.toLowerCase();

  return (
    (candidate.candidate_name || "").toLowerCase().includes(query) ||
    (candidate.email || "").toLowerCase().includes(query) ||
    (candidate.filename || "").toLowerCase().includes(query)
  );
 });

  return (
    <div className="app-layout">
      <Sidebar
        active={active}
        setActive={setActive}
        menuOpen={menuOpen}
        setMenuOpen={setMenuOpen}
      />

      <main className="main-content">
        <header className="topbar">
          <button
            className="mobile-menu-button"
            onClick={() => setMenuOpen(true)}
          >
            <Menu size={22} />
          </button>

          <div className="search-box">
            <Search size={18} />
            <input
              type="text"
              placeholder="Search candidates..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="topbar-right">
            <button className="notification-button">
              <Bell size={20} />
            </button>

            <div className="topbar-profile">
              <div className="profile-avatar">HR</div>
              <span>Recruiter</span>
            </div>
          </div>
        </header>

        <div className="page-content">
          {active === "Dashboard" ? (
            <Dashboard results={results} 
            filteredResults={filteredResults}
          />
          ) : active === "Resume Matching" ? (
          <ResumeMatching onResults={setResults} />
          ) : active === "Candidates" ? (
          <CandidateResults results={filteredResults} />
          ) : (
          <div className="content-card">
            <h2>{active}</h2>
            <p>This section is coming soon.</p>
           </div>
          )}

        </div>
      </main>
    </div>
  );
}

export default App;
