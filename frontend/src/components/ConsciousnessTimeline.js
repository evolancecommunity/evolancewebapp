<<<<<<< HEAD
import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ConsciousnessTimeline = () => {
  const [decisions, setDecisions] = useState([]);
  const [selectedDecision, setSelectedDecision] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [fulfillmentHistory, setFulfillmentHistory] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  const { user, API } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetchConsciousnessData();
  }, []);

  const fetchConsciousnessData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const [decisionsRes, fulfillmentRes, analyticsRes] = await Promise.all([
        axios.get(`${API}/consciousness/decisions`, { headers }),
        axios.get(`${API}/fulfillment/history`, { headers }),
        axios.get(`${API}/fulfillment/analytics`, { headers })
      ]);

      setDecisions(decisionsRes.data);
      setFulfillmentHistory(fulfillmentRes.data);
      setAnalytics(analyticsRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching consciousness data:', error);
      setLoading(false);
    }
  };

  const createDecision = async (decisionData) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API}/consciousness/decision`, decisionData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setShowCreateForm(false);
      fetchConsciousnessData();
    } catch (error) {
      console.error('Error creating decision:', error);
    }
  };

  const updateSelfState = async (decisionId, updatedDecision) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API}/consciousness/decision/${decisionId}`, updatedDecision, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchConsciousnessData();
    } catch (error) {
      console.error('Error updating decision:', error);
    }
  };

  const getFulfillmentColor = (level) => {
    if (level >= 80) return 'from-green-400 to-green-600';
    if (level >= 60) return 'from-yellow-400 to-yellow-600';
    if (level >= 40) return 'from-orange-400 to-orange-600';
    return 'from-red-400 to-red-600';
  };

  const SelfStateVisualization = ({ selfState, title, timeframe, position }) => {
    const positionClasses = {
      left: 'transform -translate-x-4',
      center: 'transform translate-x-0 scale-110 z-10',
      right: 'transform translate-x-4'
    };

    return (
      <div className={`relative ${positionClasses[position]} transition-all duration-500`}>
        {/* Cosmic Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-800 via-indigo-700 to-purple-900 rounded-full opacity-20 blur-xl"></div>
        
        {/* Main Container */}
        <div className="relative w-64 h-80 glass-effect rounded-2xl p-6 spiritual-glow">
          <div className="text-center mb-4">
            <h3 className="text-xl font-bold text-white mb-1">{title}</h3>
            <p className="text-purple-300 text-sm">{timeframe}</p>
          </div>

          {/* Avatar Representation */}
          <div className="relative w-20 h-20 mx-auto mb-4">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-400 to-cyan-400 rounded-full animate-pulse opacity-70"></div>
            <div className="relative w-full h-full bg-gradient-to-br from-purple-600 to-indigo-700 rounded-full flex items-center justify-center profile-glow">
              <span className="text-white text-2xl font-bold">
                {user?.full_name?.charAt(0) || 'U'}
              </span>
            </div>
            
            {/* Consciousness Level Indicator */}
            <div className="absolute -top-2 -right-2 w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center text-xs font-bold text-purple-900">
              {selfState.fulfillment_level}
            </div>
          </div>

          {/* Metrics */}
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-purple-300">Fulfillment</span>
                <span className="text-white">{selfState.fulfillment_level}%</span>
              </div>
              <div className="w-full bg-black bg-opacity-30 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(selfState.fulfillment_level)} transition-all duration-500`}
                  style={{ width: `${selfState.fulfillment_level}%` }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-purple-300">Happiness</span>
                <span className="text-white">{selfState.happiness_level}%</span>
              </div>
              <div className="w-full bg-black bg-opacity-30 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(selfState.happiness_level)} transition-all duration-500`}
                  style={{ width: `${selfState.happiness_level}%` }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-purple-300">Clarity</span>
                <span className="text-white">{selfState.clarity_level}%</span>
              </div>
              <div className="w-full bg-black bg-opacity-30 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(selfState.clarity_level)} transition-all duration-500`}
                  style={{ width: `${selfState.clarity_level}%` }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-purple-300">Confidence</span>
                <span className="text-white">{selfState.confidence_level}%</span>
              </div>
              <div className="w-full bg-black bg-opacity-30 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(selfState.confidence_level)} transition-all duration-500`}
                  style={{ width: `${selfState.confidence_level}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Characteristics */}
          <div className="mt-4">
            <div className="flex flex-wrap gap-1">
              {selfState.key_characteristics.slice(0, 3).map((trait, index) => (
                <span 
                  key={index}
                  className="px-2 py-1 bg-purple-600 bg-opacity-50 rounded-full text-xs text-purple-200"
                >
                  {trait}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Connecting Line */}
        {position !== 'right' && (
          <div className="absolute top-1/2 -right-8 w-16 h-0.5 bg-gradient-to-r from-purple-400 to-transparent opacity-50"></div>
        )}
      </div>
    );
  };

  const DecisionForm = ({ onSubmit, onCancel }) => {
    const [formData, setFormData] = useState({
      decision_title: '',
      decision_description: '',
      decision_context: '',
      decision_options: [
        { title: '', description: '', potential_outcomes: [''], confidence_score: 50 },
        { title: '', description: '', potential_outcomes: [''], confidence_score: 50 }
      ]
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      onSubmit(formData);
    };

    const addOption = () => {
      setFormData({
        ...formData,
        decision_options: [
          ...formData.decision_options,
          { title: '', description: '', potential_outcomes: [''], confidence_score: 50 }
        ]
      });
    };

    const updateOption = (index, field, value) => {
      const newOptions = [...formData.decision_options];
      newOptions[index] = { ...newOptions[index], [field]: value };
      setFormData({ ...formData, decision_options: newOptions });
    };

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="max-w-4xl w-full max-h-screen overflow-y-auto glass-effect rounded-2xl p-8 spiritual-glow">
          <h2 className="text-3xl font-bold text-white mb-6">Create Consciousness Decision</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-purple-200 text-sm font-medium mb-2">Decision Title</label>
              <input
                type="text"
                value={formData.decision_title}
                onChange={(e) => setFormData({...formData, decision_title: e.target.value})}
                className="w-full px-4 py-3 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                placeholder="What decision are you contemplating?"
                required
              />
            </div>

            <div>
              <label className="block text-purple-200 text-sm font-medium mb-2">Description</label>
              <textarea
                value={formData.decision_description}
                onChange={(e) => setFormData({...formData, decision_description: e.target.value})}
                className="w-full px-4 py-3 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                placeholder="Describe the decision in detail..."
                rows="3"
                required
              />
            </div>

            <div>
              <label className="block text-purple-200 text-sm font-medium mb-2">Context</label>
              <textarea
                value={formData.decision_context}
                onChange={(e) => setFormData({...formData, decision_context: e.target.value})}
                className="w-full px-4 py-3 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                placeholder="What's the current situation and background?"
                rows="2"
                required
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-4">
                <label className="block text-purple-200 text-sm font-medium">Decision Options</label>
                <button
                  type="button"
                  onClick={addOption}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm transition-all duration-200"
                >
                  Add Option
                </button>
              </div>
              
              {formData.decision_options.map((option, index) => (
                <div key={index} className="mb-4 p-4 bg-white bg-opacity-5 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <input
                        type="text"
                        value={option.title}
                        onChange={(e) => updateOption(index, 'title', e.target.value)}
                        className="w-full px-3 py-2 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                        placeholder={`Option ${index + 1} title`}
                        required
                      />
                    </div>
                    <div>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={option.confidence_score}
                        onChange={(e) => updateOption(index, 'confidence_score', parseInt(e.target.value))}
                        className="w-full"
                      />
                      <div className="text-center text-purple-300 text-sm">Confidence: {option.confidence_score}%</div>
                    </div>
                  </div>
                  <textarea
                    value={option.description}
                    onChange={(e) => updateOption(index, 'description', e.target.value)}
                    className="w-full mt-2 px-3 py-2 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                    placeholder="Describe this option..."
                    rows="2"
                    required
                  />
                </div>
              ))}
            </div>

            <div className="flex space-x-4">
              <button
                type="submit"
                className="flex-1 spiritual-button text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200"
              >
                Create Decision Timeline
              </button>
              <button
                type="button"
                onClick={onCancel}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="text-center">
          <div className="chakra-loading w-16 h-16 mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading consciousness timeline...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 relative overflow-hidden">
      {/* Cosmic Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-40 h-40 bg-purple-400 rounded-full opacity-10 blur-xl animate-pulse float"></div>
        <div className="absolute bottom-20 right-20 w-60 h-60 bg-indigo-400 rounded-full opacity-10 blur-xl animate-pulse delay-1000 float"></div>
        <div className="absolute top-1/3 right-1/4 w-32 h-32 bg-purple-300 rounded-full opacity-10 blur-xl animate-pulse delay-500 float"></div>
        <div className="absolute bottom-1/4 left-1/3 w-36 h-36 bg-cyan-400 rounded-full opacity-10 blur-xl animate-pulse delay-300 float"></div>
      </div>

      {/* Header */}
      <header className="relative z-20 bg-black bg-opacity-30 backdrop-filter backdrop-blur-lg border-b border-purple-300 border-opacity-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center text-purple-200 hover:text-white transition-colors duration-200"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Dashboard
            </button>

            <h1 className="text-2xl font-bold text-white">Consciousness Timeline</h1>

            <button
              onClick={() => setShowCreateForm(true)}
              className="spiritual-button text-white font-medium py-2 px-6 rounded-lg transition-all duration-200"
            >
              New Decision
            </button>
=======
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
>>>>>>> neel
          </div>
        </div>
      </header>

<<<<<<< HEAD
      <main className="relative z-10 p-6">
        <div className="max-w-7xl mx-auto">
          {/* Analytics Overview */}
          {analytics && (
            <div className="mb-12">
              <div className="text-center mb-8">
                <h2 className="text-4xl font-bold text-white mb-4">Your Consciousness Journey</h2>
                <p className="text-purple-200 text-lg">Track your inner fulfillment and spiritual growth over time</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="glass-effect rounded-2xl p-6 text-center spiritual-glow">
                  <div className="text-3xl font-bold text-white mb-2">{analytics.average_fulfillment}</div>
                  <div className="text-purple-300">Avg Fulfillment</div>
                  <div className="w-full bg-black bg-opacity-30 rounded-full h-2 mt-2">
                    <div 
                      className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(analytics.average_fulfillment)} transition-all duration-500`}
                      style={{ width: `${analytics.average_fulfillment}%` }}
                    ></div>
                  </div>
                </div>

                <div className="glass-effect rounded-2xl p-6 text-center spiritual-glow">
                  <div className="text-3xl font-bold text-white mb-2">{analytics.average_happiness}</div>
                  <div className="text-purple-300">Avg Happiness</div>
                  <div className="w-full bg-black bg-opacity-30 rounded-full h-2 mt-2">
                    <div 
                      className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(analytics.average_happiness)} transition-all duration-500`}
                      style={{ width: `${analytics.average_happiness}%` }}
                    ></div>
                  </div>
                </div>

                <div className="glass-effect rounded-2xl p-6 text-center spiritual-glow">
                  <div className="text-3xl font-bold text-white mb-2">{analytics.average_clarity}</div>
                  <div className="text-purple-300">Avg Clarity</div>
                  <div className="w-full bg-black bg-opacity-30 rounded-full h-2 mt-2">
                    <div 
                      className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(analytics.average_clarity)} transition-all duration-500`}
                      style={{ width: `${analytics.average_clarity}%` }}
                    ></div>
                  </div>
                </div>

                <div className="glass-effect rounded-2xl p-6 text-center spiritual-glow">
                  <div className="flex items-center justify-center mb-2">
                    <span className="text-2xl mr-2">
                      {analytics.trend === 'ascending' ? '📈' : analytics.trend === 'descending' ? '📉' : '➡️'}
                    </span>
                    <span className="text-2xl font-bold text-white capitalize">{analytics.trend}</span>
                  </div>
                  <div className="text-purple-300">Overall Trend</div>
                </div>
              </div>
            </div>
          )}

          {/* Decision Timeline */}
          {selectedDecision ? (
            <div className="mb-12">
              <button
                onClick={() => setSelectedDecision(null)}
                className="mb-6 flex items-center text-purple-200 hover:text-white transition-colors duration-200"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Back to Decisions
              </button>

              <div className="glass-effect rounded-2xl p-8 spiritual-glow mb-8">
                <h2 className="text-3xl font-bold text-white mb-4">{selectedDecision.decision_title}</h2>
                <p className="text-purple-200 mb-6">{selectedDecision.decision_description}</p>
                
                {/* Self States Timeline */}
                <div className="relative">
                  <div className="flex justify-center items-center space-x-8 mb-12 overflow-x-auto">
                    <SelfStateVisualization 
                      selfState={selectedDecision.past_self}
                      title="Past Self"
                      timeframe="Who you were"
                      position="left"
                    />
                    <SelfStateVisualization 
                      selfState={selectedDecision.present_self}
                      title="Present Self"
                      timeframe="Who you are"
                      position="center"
                    />
                    <SelfStateVisualization 
                      selfState={selectedDecision.future_self}
                      title="Future Self"
                      timeframe="Who you're becoming"
                      position="right"
                    />
                  </div>
                </div>

                {/* Decision Options */}
                <div className="mb-8">
                  <h3 className="text-2xl font-semibold text-white mb-4">Decision Options</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {selectedDecision.decision_options.map((option, index) => (
                      <div
                        key={index}
                        className={`p-4 rounded-lg border-2 transition-all duration-300 ${
                          selectedDecision.chosen_option_index === index
                            ? 'border-green-400 bg-green-500 bg-opacity-20'
                            : 'border-purple-300 border-opacity-30 bg-white bg-opacity-5'
                        }`}
                      >
                        <h4 className="text-lg font-semibold text-white mb-2">{option.title}</h4>
                        <p className="text-purple-200 text-sm mb-3">{option.description}</p>
                        <div className="flex justify-between items-center">
                          <span className="text-purple-300 text-sm">Confidence</span>
                          <span className="text-white text-sm font-medium">{option.confidence_score}%</span>
                        </div>
                        <div className="w-full bg-black bg-opacity-30 rounded-full h-2 mt-1">
                          <div 
                            className="h-2 rounded-full bg-gradient-to-r from-purple-400 to-cyan-400 transition-all duration-500"
                            style={{ width: `${option.confidence_score}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Insights */}
                {selectedDecision.ai_insights && selectedDecision.ai_insights.length > 0 && (
                  <div>
                    <h3 className="text-2xl font-semibold text-white mb-4">Evolance Insights</h3>
                    <div className="space-y-4">
                      {selectedDecision.ai_insights.map((insight, index) => (
                        <div key={index} className="flex items-start p-4 bg-white bg-opacity-5 rounded-lg">
                          <div className="w-8 h-8 bg-gradient-to-r from-purple-400 to-cyan-400 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                            <span className="text-white text-sm font-bold">E</span>
                          </div>
                          <p className="text-purple-200 leading-relaxed">{insight}</p>
                        </div>
                      ))}
=======
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
>>>>>>> neel
                    </div>
                  </div>
                )}
              </div>
<<<<<<< HEAD
            </div>
          ) : (
            /* Decisions List */
            <div>
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-white mb-4">Your Consciousness Decisions</h2>
                <p className="text-purple-200">Explore the evolution of your past, present, and future selves</p>
              </div>

              {decisions.length === 0 ? (
                <div className="text-center py-16">
                  <div className="w-24 h-24 bg-gradient-to-br from-purple-400 to-cyan-400 rounded-full flex items-center justify-center mx-auto mb-6 opacity-50">
                    <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-semibold text-white mb-4">Begin Your Consciousness Journey</h3>
                  <p className="text-purple-200 mb-8 max-w-md mx-auto">
                    Create your first consciousness decision to explore how your choices shape your spiritual evolution
                  </p>
                  <button
                    onClick={() => setShowCreateForm(true)}
                    className="spiritual-button text-white font-semibold py-3 px-8 rounded-lg transition-all duration-200"
                  >
                    Create Your First Decision
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {decisions.map((decision) => (
                    <div
                      key={decision.id}
                      className="glass-effect rounded-2xl p-6 spiritual-glow cursor-pointer transform hover:scale-105 transition-all duration-300"
                      onClick={() => setSelectedDecision(decision)}
                    >
                      <h3 className="text-xl font-semibold text-white mb-3">{decision.decision_title}</h3>
                      <p className="text-purple-200 text-sm mb-4 leading-relaxed">{decision.decision_description}</p>
                      
                      <div className="space-y-2 mb-4">
                        <div className="flex justify-between items-center">
                          <span className="text-purple-300 text-sm">Past → Present → Future</span>
                          <span className="text-white text-sm">
                            {decision.past_self.fulfillment_level}% → {decision.present_self.fulfillment_level}% → {decision.future_self.fulfillment_level}%
                          </span>
                        </div>
                        <div className="w-full bg-black bg-opacity-30 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(decision.future_self.fulfillment_level)} transition-all duration-500`}
                            style={{ width: `${decision.future_self.fulfillment_level}%` }}
                          ></div>
                        </div>
                      </div>

                      <div className="flex justify-between items-center">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                          decision.decision_status === 'decided' ? 'bg-green-500 text-white' :
                          decision.decision_status === 'implemented' ? 'bg-blue-500 text-white' :
                          'bg-yellow-500 text-black'
                        }`}>
                          {decision.decision_status}
                        </span>
                        <span className="text-purple-300 text-sm">
                          {new Date(decision.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      {/* Create Decision Form Modal */}
      {showCreateForm && (
        <DecisionForm
          onSubmit={createDecision}
          onCancel={() => setShowCreateForm(false)}
        />
      )}
=======

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
>>>>>>> neel
    </div>
  );
};

export default ConsciousnessTimeline;
