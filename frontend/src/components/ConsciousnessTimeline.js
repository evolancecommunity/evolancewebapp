import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './ConsciousnessTimeline.css';

const ConsciousnessTimeline = () => {
  const [decision, setDecision] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeTimeline, setActiveTimeline] = useState('present');
  const navigate = useNavigate();

  const timelineStages = {
    past: {
      title: 'Past Context',
      subtitle: 'Historical patterns and influences',
      description: 'How past experiences and decisions relate to your current situation',
      color: '#ef4444'
    },
    present: {
      title: 'Present Analysis',
      subtitle: 'Current situation and options',
      description: 'Understanding the immediate context and available choices',
      color: '#6366f1'
    },
    future: {
      title: 'Future Implications',
      subtitle: 'Long-term consequences and growth',
      description: 'Projecting outcomes and personal development opportunities',
      color: '#10b981'
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!decision.trim()) return;

    setIsAnalyzing(true);
    try {
      // Simulate API call for now
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock analysis data
      setAnalysis({
        decision: decision,
        past: {
          patterns: ['You have shown similar decision-making patterns in career choices', 'Past experiences with change have been positive'],
          influences: ['Your upbringing emphasized careful consideration', 'Previous successful transitions inform this decision'],
          insights: 'Your history shows resilience and adaptability when facing major decisions.'
        },
        present: {
          context: 'You are at a crossroads in your professional development',
          options: ['Maintain current path with incremental improvements', 'Pursue new opportunities with calculated risk'],
          factors: ['Financial stability', 'Personal growth potential', 'Work-life balance'],
          insights: 'The decision requires balancing security with growth aspirations.'
        },
        future: {
          scenarios: [
            {
              path: 'Conservative approach',
              outcomes: ['Stable career progression', 'Limited growth opportunities', 'Predictable lifestyle'],
              probability: '60%'
            },
            {
              path: 'Growth-oriented approach',
              outcomes: ['Higher potential rewards', 'Increased uncertainty', 'Personal development'],
              probability: '40%'
            }
          ],
          insights: 'Both paths offer valid outcomes; the choice depends on your current priorities and risk tolerance.'
        },
        alignment: {
          values: 85,
          goals: 78,
          personality: 92
        }
      });
    } catch (error) {
      console.error('Error analyzing decision:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getAlignmentColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
    };

  const getAlignmentLabel = (score) => {
    if (score >= 80) return 'High Alignment';
    if (score >= 60) return 'Moderate Alignment';
    return 'Low Alignment';
  };

  return (
    <div className="timeline-container">
      {/* Header */}
      <header className="timeline-header">
        <div className="header-content">
          <div className="header-left">
            <button onClick={() => navigate('/dashboard')} className="back-btn">
              ← Back to Dashboard
            </button>
            <h1 className="page-title">Consciousness Timeline</h1>
            <p className="page-subtitle">Analyze decisions across time dimensions for deeper self-awareness</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="timeline-main">
        <div className="timeline-layout">
          {/* Decision Input Section */}
          <section className="decision-section">
            <div className="decision-card">
              <div className="card-header">
                <h2 className="card-title">Decision Analysis</h2>
                <p className="card-subtitle">Enter a decision you want to analyze across past, present, and future contexts</p>
              </div>
              <div className="card-content">
                <form onSubmit={handleSubmit} className="decision-form">
                  <div className="form-group">
                    <label htmlFor="decision" className="form-label">What decision are you considering?</label>
                    <textarea
                      id="decision"
                      value={decision}
                      onChange={(e) => setDecision(e.target.value)}
                      placeholder="Describe the decision you want to analyze. For example: 'Should I change careers to pursue my passion for technology?'"
                      className="decision-input"
                      rows={4}
                      required
                    />
                  </div>
                  <button 
                    type="submit" 
                    className="analyze-btn"
                    disabled={isAnalyzing || !decision.trim()}
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="spinner"></div>
                        Analyzing...
                      </>
                    ) : (
                      'Analyze Decision'
                    )}
                  </button>
                </form>
              </div>
            </div>
          </section>

          {/* Analysis Results */}
          {analysis && (
            <section className="analysis-section">
              {/* Timeline Navigation */}
              <div className="timeline-nav">
                {Object.entries(timelineStages).map(([key, stage]) => (
              <button
                    key={key}
                    onClick={() => setActiveTimeline(key)}
                    className={`timeline-nav-btn ${activeTimeline === key ? 'active' : ''}`}
                    style={{ '--accent-color': stage.color }}
              >
                    <span className="nav-title">{stage.title}</span>
                    <span className="nav-subtitle">{stage.subtitle}</span>
              </button>
                ))}
              </div>

              {/* Timeline Content */}
              <div className="timeline-content">
                {activeTimeline === 'past' && (
                  <div className="timeline-stage">
                    <div className="stage-header">
                      <h3 className="stage-title">Past Context</h3>
                      <p className="stage-description">{timelineStages.past.description}</p>
                    </div>
                    <div className="stage-content">
                      <div className="analysis-grid">
                        <div className="analysis-card">
                          <h4 className="analysis-title">Patterns</h4>
                          <ul className="analysis-list">
                            {analysis.past.patterns.map((pattern, index) => (
                              <li key={index} className="analysis-item">{pattern}</li>
                            ))}
                          </ul>
                        </div>
                        <div className="analysis-card">
                          <h4 className="analysis-title">Influences</h4>
                          <ul className="analysis-list">
                            {analysis.past.influences.map((influence, index) => (
                              <li key={index} className="analysis-item">{influence}</li>
                            ))}
                          </ul>
                        </div>
                        <div className="analysis-card full-width">
                          <h4 className="analysis-title">Key Insight</h4>
                          <p className="insight-text">{analysis.past.insights}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTimeline === 'present' && (
                  <div className="timeline-stage">
                    <div className="stage-header">
                      <h3 className="stage-title">Present Analysis</h3>
                      <p className="stage-description">{timelineStages.present.description}</p>
                    </div>
                    <div className="stage-content">
                      <div className="analysis-grid">
                        <div className="analysis-card">
                          <h4 className="analysis-title">Current Context</h4>
                          <p className="context-text">{analysis.present.context}</p>
                        </div>
                        <div className="analysis-card">
                          <h4 className="analysis-title">Available Options</h4>
                          <ul className="analysis-list">
                            {analysis.present.options.map((option, index) => (
                              <li key={index} className="analysis-item">{option}</li>
                            ))}
                          </ul>
                </div>
                        <div className="analysis-card">
                          <h4 className="analysis-title">Key Factors</h4>
                          <ul className="analysis-list">
                            {analysis.present.factors.map((factor, index) => (
                              <li key={index} className="analysis-item">{factor}</li>
                            ))}
                          </ul>
                        </div>
                        <div className="analysis-card full-width">
                          <h4 className="analysis-title">Present Insight</h4>
                          <p className="insight-text">{analysis.present.insights}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTimeline === 'future' && (
                  <div className="timeline-stage">
                    <div className="stage-header">
                      <h3 className="stage-title">Future Implications</h3>
                      <p className="stage-description">{timelineStages.future.description}</p>
                    </div>
                    <div className="stage-content">
                      <div className="scenarios-grid">
                        {analysis.future.scenarios.map((scenario, index) => (
                          <div key={index} className="scenario-card">
                            <div className="scenario-header">
                              <h4 className="scenario-title">{scenario.path}</h4>
                              <span className="probability">{scenario.probability} probability</span>
                            </div>
                            <div className="scenario-outcomes">
                              <h5 className="outcomes-title">Potential Outcomes:</h5>
                              <ul className="outcomes-list">
                                {scenario.outcomes.map((outcome, outcomeIndex) => (
                                  <li key={outcomeIndex} className="outcome-item">{outcome}</li>
                                ))}
                              </ul>
                </div>
                          </div>
                        ))}
                        <div className="analysis-card full-width">
                          <h4 className="analysis-title">Future Insight</h4>
                          <p className="insight-text">{analysis.future.insights}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Alignment Summary */}
              <div className="alignment-section">
                <h3 className="alignment-title">Decision Alignment</h3>
                <div className="alignment-grid">
                  <div className="alignment-item">
                    <div className="alignment-header">
                      <span className="alignment-label">Values Alignment</span>
                      <span className="alignment-score">{analysis.alignment.values}%</span>
            </div>
                    <div className="alignment-bar">
                      <div 
                        className="alignment-fill"
                        style={{ 
                          width: `${analysis.alignment.values}%`,
                          backgroundColor: getAlignmentColor(analysis.alignment.values)
                        }}
                      ></div>
              </div>
                    <span className="alignment-status">{getAlignmentLabel(analysis.alignment.values)}</span>
                  </div>
                  <div className="alignment-item">
                    <div className="alignment-header">
                      <span className="alignment-label">Goals Alignment</span>
                      <span className="alignment-score">{analysis.alignment.goals}%</span>
                </div>
                    <div className="alignment-bar">
                      <div 
                        className="alignment-fill"
                        style={{ 
                          width: `${analysis.alignment.goals}%`,
                          backgroundColor: getAlignmentColor(analysis.alignment.goals)
                        }}
                          ></div>
                        </div>
                    <span className="alignment-status">{getAlignmentLabel(analysis.alignment.goals)}</span>
                      </div>
                  <div className="alignment-item">
                    <div className="alignment-header">
                      <span className="alignment-label">Personality Fit</span>
                      <span className="alignment-score">{analysis.alignment.personality}%</span>
                      </div>
                    <div className="alignment-bar">
                      <div 
                        className="alignment-fill"
                        style={{ 
                          width: `${analysis.alignment.personality}%`,
                          backgroundColor: getAlignmentColor(analysis.alignment.personality)
                        }}
                      ></div>
                    </div>
                    <span className="alignment-status">{getAlignmentLabel(analysis.alignment.personality)}</span>
                  </div>
                </div>
            </div>
            </section>
          )}
        </div>
      </main>
    </div>
  );
};

export default ConsciousnessTimeline;
