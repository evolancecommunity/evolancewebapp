import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import axios from 'axios';

const CrisisAlert = ({ show = false, onClose }) => {
  const { API } = useContext(AuthContext);
  const [resources, setResources] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (show) {
      fetchCrisisResources();
    }
  }, [show]);

  const fetchCrisisResources = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/ai/crisis/resources`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setResources(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching crisis resources:', err);
      setError('Failed to load crisis resources');
      // Set default resources
      setResources({
        crisis_lifeline: {
          name: "988 Suicide & Crisis Lifeline",
          phone: "988",
          text: "Text HOME to 988",
          website: "https://988lifeline.org"
        },
        crisis_text_line: {
          name: "Crisis Text Line",
          text: "Text HOME to 741741",
          website: "https://www.crisistextline.org"
        },
        emergency: {
          message: "If you're in immediate danger, please call 911 or go to your nearest emergency room.",
          phone: "911"
        },
        disclaimer: "Evolance is a growth tool, not a replacement for professional mental health care. If you're experiencing a crisis, please reach out to the resources above or a mental health professional."
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCall = (phoneNumber) => {
    window.open(`tel:${phoneNumber}`, '_self');
  };

  const handleText = (textNumber) => {
    window.open(`sms:${textNumber}`, '_self');
  };

  const handleWebsite = (url) => {
    window.open(url, '_blank');
  };

  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black bg-opacity-75 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="relative bg-gradient-to-br from-red-900 via-red-800 to-orange-800 rounded-2xl p-8 max-w-md w-full spiritual-glow border-2 border-red-400">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-white hover:text-red-200 transition-colors duration-200"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Header */}
        <div className="text-center mb-6">
          <div className="text-4xl mb-4">🆘</div>
          <h2 className="text-2xl font-bold text-white mb-2">Crisis Support</h2>
          <p className="text-red-200 text-sm">
            You're not alone. Help is available 24/7.
          </p>
        </div>

        {loading ? (
          <div className="text-center">
            <div className="chakra-loading w-12 h-12 mx-auto mb-4"></div>
            <p className="text-white">Loading crisis resources...</p>
          </div>
        ) : error ? (
          <div className="text-center">
            <p className="text-red-300 mb-4">{error}</p>
            <button
              onClick={fetchCrisisResources}
              className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
            >
              Try Again
            </button>
          </div>
        ) : resources ? (
          <div className="space-y-6">
            {/* Emergency Alert */}
            <div className="bg-red-600 bg-opacity-30 border border-red-400 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <span className="text-2xl mr-2">🚨</span>
                <h3 className="text-white font-semibold">Emergency</h3>
              </div>
              <p className="text-red-100 text-sm mb-3">
                {resources.emergency.message}
              </p>
              <button
                onClick={() => handleCall(resources.emergency.phone)}
                className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                Call {resources.emergency.phone}
              </button>
            </div>

            {/* Crisis Lifeline */}
            <div className="bg-white bg-opacity-10 rounded-lg p-4">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-2">💜</span>
                <h3 className="text-white font-semibold">{resources.crisis_lifeline.name}</h3>
              </div>
              <div className="space-y-3">
                <button
                  onClick={() => handleCall(resources.crisis_lifeline.phone)}
                  className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 flex items-center justify-center"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  Call {resources.crisis_lifeline.phone}
                </button>
                <button
                  onClick={() => handleText(resources.crisis_lifeline.text.split(' ')[1])}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 flex items-center justify-center"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  {resources.crisis_lifeline.text}
                </button>
                <button
                  onClick={() => handleWebsite(resources.crisis_lifeline.website)}
                  className="w-full bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 flex items-center justify-center"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  Visit Website
                </button>
              </div>
            </div>

            {/* Crisis Text Line */}
            <div className="bg-white bg-opacity-10 rounded-lg p-4">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-2">💬</span>
                <h3 className="text-white font-semibold">{resources.crisis_text_line.name}</h3>
              </div>
              <div className="space-y-3">
                <button
                  onClick={() => handleText(resources.crisis_text_line.text.split(' ')[1])}
                  className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 flex items-center justify-center"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  {resources.crisis_text_line.text}
                </button>
                <button
                  onClick={() => handleWebsite(resources.crisis_text_line.website)}
                  className="w-full bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 flex items-center justify-center"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  Visit Website
                </button>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="bg-yellow-600 bg-opacity-20 border border-yellow-400 rounded-lg p-4">
              <p className="text-yellow-100 text-sm leading-relaxed">
                {resources.disclaimer}
              </p>
            </div>
          </div>
        ) : null}

        {/* Close Button */}
        <div className="text-center mt-6">
          <button
            onClick={onClose}
            className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white font-medium py-2 px-6 rounded-lg transition-all duration-200"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default CrisisAlert; 