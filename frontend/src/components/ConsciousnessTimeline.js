import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ConsciousnessTimeline = () => {
  const [decision, setDecision] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [timelineData, setTimelineData] = useState(null);
  const [previousDecisions, setPreviousDecisions] = useState([]);
  const [loading, setLoading] = useState(true);

  const { user, API } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetchPreviousDecisions();
  }, []);

  const fetchPreviousDecisions = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      const response = await axios.get(`${API}/consciousness/decisions`, { headers });
      setPreviousDecisions(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching previous decisions:', error);
      setLoading(false);
    }
  };

  const analyzeDecision = async () => {
    if (!decision.trim()) return;
    
    setIsAnalyzing(true);
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      const response = await axios.post(`${API}/consciousness/analyze-decision`, {
        decision: decision.trim()
      }, { headers });
      
      setTimelineData(response.data);
    } catch (error) {
      console.error('Error analyzing decision:', error);
      // Set demo data for now
      setTimelineData({
        decision: decision.trim(),
        past_analysis: {
          title: "How this decision relates to your past",
          description: "Based on your semantic network, this decision connects to patterns from your earlier experiences. You've shown resilience in similar situations and have grown from past challenges.",
          emotional_state: "reflective",
          key_insights: [
            "Your past experiences with change have made you more adaptable",
            "You've learned to trust your intuition in uncertain situations",
            "Previous challenges have built your emotional resilience"
          ],
          confidence_level: 75,
          color: "from-red-500 to-pink-500"
        },
        present_analysis: {
          title: "Your current state and readiness",
          description: "Your semantic network shows you're in a period of growth and self-discovery. You have the emotional tools and self-awareness needed to make this decision with clarity.",
          emotional_state: "contemplative",
          key_insights: [
            "You're currently in a phase of increased self-awareness",
            "Your emotional clarity is at a good level for decision-making",
            "You have strong support systems in place"
          ],
          confidence_level: 82,
          color: "from-blue-500 to-cyan-500"
        },
        future_analysis: {
          title: "Potential impact on your future self",
          description: "This decision aligns well with your long-term growth trajectory. It will likely strengthen your authentic identity and contribute to your emotional fulfillment.",
          emotional_state: "hopeful",
          key_insights: [
            "This choice supports your authentic self-expression",
            "It will likely increase your emotional fulfillment",
            "The decision aligns with your core values and identity"
          ],
          confidence_level: 88,
          color: "from-green-500 to-emerald-500"
        },
        ai_recommendation: "Based on your semantic network, this decision appears to be well-aligned with your authentic self and growth trajectory. Trust your intuition while remaining open to the learning opportunities this choice will bring."
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetAnalysis = () => {
    setDecision('');
    setTimelineData(null);
  };

  const TimelineCard = ({ data, title, emoji, position }) => {
    const positionClasses = {
      left: 'transform -translate-x-4',
      center: 'transform translate-x-0 scale-110 z-10',
      right: 'transform translate-x-4'
    };

    return (
      <div className={`relative ${positionClasses[position]} transition-all duration-500`}>
        {/* Glow Effect */}
        <div className={`absolute inset-0 bg-gradient-to-r ${data.color} rounded-3xl opacity-20 blur-2xl`}></div>
        
        {/* Main Card */}
        <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 hover:border-white/30 transition-all duration-500 min-h-[400px]">
          <div className="text-center mb-6">
            <div className="text-4xl mb-3">{emoji}</div>
            <h3 className="text-2xl font-bold text-white mb-2">{title}</h3>
            <p className="text-purple-200 text-sm">{data.emotional_state}</p>
          </div>

          <div className="mb-6">
            <p className="text-purple-200 leading-relaxed mb-4">{data.description}</p>
            
            <div className="space-y-3">
              {data.key_insights.map((insight, index) => (
                <div key={index} className="flex items-start">
                  <div className="w-2 h-2 bg-purple-300 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <p className="text-white text-sm leading-relaxed">{insight}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-auto">
            <div className="flex justify-between items-center mb-2">
              <span className="text-purple-200 text-sm">Alignment Level</span>
              <span className="text-white font-bold">{data.confidence_level}%</span>
            </div>
            <div className="w-full bg-white/20 rounded-full h-3 overflow-hidden">
              <div 
                className={`h-3 rounded-full bg-gradient-to-r ${data.color} transition-all duration-1000 ease-out shadow-lg`}
                style={{ width: `${data.confidence_level}%` }}
              ></div>
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="w-20 h-20 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mx-auto mb-6"></div>
            <div className="absolute inset-0 w-20 h-20 border-4 border-transparent border-t-pink-400 rounded-full animate-spin mx-auto" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
          </div>
          <p className="text-white text-xl font-medium">Loading your consciousness timeline...</p>
          <p className="text-purple-200 text-sm mt-2">Preparing your decision analysis</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-400 rounded-full opacity-10 blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-pink-400 rounded-full opacity-10 blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/3 right-1/4 w-64 h-64 bg-indigo-400 rounded-full opacity-10 blur-3xl animate-pulse delay-500"></div>
        <div className="absolute bottom-1/3 left-1/4 w-80 h-80 bg-cyan-400 rounded-full opacity-10 blur-3xl animate-pulse delay-1500"></div>
      </div>

      {/* Header */}
      <header className="relative z-20 bg-white/10 backdrop-blur-xl border-b border-white/20 sticky top-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center text-purple-200 hover:text-white transition-colors duration-200 group"
            >
              <svg className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Dashboard
            </button>

            <div className="text-center">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
                Consciousness Timeline
              </h1>
              <p className="text-purple-200 text-sm">Visualize decisions across your timeline</p>
            </div>

            <div className="w-20"></div> {/* Spacer for centering */}
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {!timelineData ? (
          /* Decision Input Section */
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-5xl font-bold text-white mb-6">What decision are you contemplating?</h2>
              <p className="text-xl text-purple-200 max-w-3xl mx-auto leading-relaxed">
                Write down a decision you want to make, and Evolance will help you visualize how it connects to your past, 
                present, and future based on your unique semantic network and emotional patterns.
              </p>
            </div>

            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
              <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-12 border border-white/20 hover:border-white/30 transition-all duration-500">
                <div className="mb-8">
                  <label className="block text-white text-lg font-semibold mb-4">Your Decision</label>
                  <textarea
                    value={decision}
                    onChange={(e) => setDecision(e.target.value)}
                    placeholder="Describe the decision you're facing... For example: 'Should I change careers?' or 'Should I move to a new city?' or 'Should I end this relationship?'"
                    className="w-full px-6 py-8 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent resize-none text-lg leading-relaxed"
                    rows="6"
                    disabled={isAnalyzing}
                  />
                </div>

                <div className="flex justify-center">
                  <button
                    onClick={analyzeDecision}
                    disabled={!decision.trim() || isAnalyzing}
                    className={`px-12 py-4 rounded-2xl font-semibold text-lg transition-all duration-300 transform ${
                      !decision.trim() || isAnalyzing
                        ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white hover:scale-105 shadow-lg'
                    }`}
                  >
                    {isAnalyzing ? (
                      <div className="flex items-center">
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-3"></div>
                        Analyzing your decision...
                      </div>
                    ) : (
                      'Visualize Across Timeline'
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Previous Decisions */}
            {previousDecisions.length > 0 && (
              <div className="mt-16">
                <h3 className="text-2xl font-bold text-white mb-8 text-center">Previous Decisions</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {previousDecisions.slice(0, 6).map((prevDecision) => (
                    <div
                      key={prevDecision.id}
                      className="group bg-white/5 rounded-2xl p-6 hover:bg-white/10 transition-all duration-300 border border-white/10 hover:border-white/20 cursor-pointer transform hover:scale-105"
                      onClick={() => setTimelineData(prevDecision)}
                    >
                      <h4 className="text-lg font-semibold text-white mb-3">{prevDecision.decision_title}</h4>
                      <p className="text-purple-200 text-sm mb-4 line-clamp-3">{prevDecision.decision_description}</p>
                      <div className="flex justify-between items-center">
                        <span className="text-purple-300 text-sm">
                          {new Date(prevDecision.created_at).toLocaleDateString()}
                        </span>
                        <span className="text-white text-sm font-medium">
                          {prevDecision.present_self?.confidence_level || 75}% alignment
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Timeline Visualization */
          <div>
            <div className="text-center mb-12">
              <button
                onClick={resetAnalysis}
                className="inline-flex items-center text-purple-200 hover:text-white transition-colors duration-200 mb-6 group"
              >
                <svg className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Analyze Another Decision
              </button>
              
              <h2 className="text-4xl font-bold text-white mb-4">Your Decision Timeline</h2>
              <p className="text-xl text-purple-200 max-w-3xl mx-auto leading-relaxed">
                "{timelineData.decision}"
              </p>
            </div>

            {/* Timeline Cards */}
            <div className="flex justify-center items-center space-x-8 mb-12 overflow-x-auto pb-8">
              <TimelineCard 
                data={timelineData.past_analysis}
                title="The Past"
                emoji="🕰️"
                position="left"
              />
              <TimelineCard 
                data={timelineData.present_analysis}
                title="The Present"
                emoji="✨"
                position="center"
              />
              <TimelineCard 
                data={timelineData.future_analysis}
                title="The Future"
                emoji="🌟"
                position="right"
              />
            </div>

            {/* AI Recommendation */}
            <div className="group relative max-w-4xl mx-auto">
              <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
              <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 hover:border-white/30 transition-all duration-500">
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mr-4 shadow-lg flex-shrink-0">
                    <span className="text-white font-bold text-xl">E</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white mb-3">Evolance's Insight</h3>
                    <p className="text-purple-200 leading-relaxed text-lg">{timelineData.ai_recommendation}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-center space-x-6 mt-12">
              <button
                onClick={() => navigate('/chat', { state: { context: 'decision-discussion', decision: timelineData.decision } })}
                className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                Discuss with Evolance
              </button>
              
              <button
                onClick={() => {
                  // Save decision to history
                  setPreviousDecisions([timelineData, ...previousDecisions]);
                  resetAnalysis();
                }}
                className="px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                Save Decision
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default ConsciousnessTimeline;
