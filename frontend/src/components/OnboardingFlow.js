import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import axios from 'axios';

const OnboardingFlow = () => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);

  const { API } = useContext(AuthContext);

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/personality/questions`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setQuestions(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching questions:', error);
      setLoading(false);
    }
  };

  const handleOptionSelect = (optionIndex, optionText) => {
    setSelectedOption({ index: optionIndex, text: optionText });
  };

  const handleNext = () => {
    if (selectedOption !== null) {
      const newAnswer = {
        question_id: questions[currentQuestion].id,
        answer_index: selectedOption.index,
        answer_text: selectedOption.text
      };

      const updatedAnswers = [...answers];
      updatedAnswers[currentQuestion] = newAnswer;
      setAnswers(updatedAnswers);

      if (currentQuestion < questions.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
        setSelectedOption(null);
      } else {
        submitTest(updatedAnswers);
      }
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
      const previousAnswer = answers[currentQuestion - 1];
      if (previousAnswer) {
        setSelectedOption({
          index: previousAnswer.answer_index,
          text: previousAnswer.answer_text
        });
      } else {
        setSelectedOption(null);
      }
    }
  };

  const submitTest = async (finalAnswers) => {
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API}/personality/submit`, {
        answers: finalAnswers
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Refresh the page to trigger auth check
      window.location.reload();
    } catch (error) {
      console.error('Error submitting test:', error);
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="text-center">
          <div className="chakra-loading w-16 h-16 mx-auto mb-4"></div>
          <p className="text-white text-lg">Preparing your spiritual assessment...</p>
        </div>
      </div>
    );
  }

  if (submitting) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="text-center">
          <div className="chakra-loading w-20 h-20 mx-auto mb-6"></div>
          <h2 className="text-3xl font-bold text-white mb-4">Analyzing your spiritual essence...</h2>
          <p className="text-purple-200 text-lg">This may take a moment</p>
        </div>
      </div>
    );
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 p-4">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-32 h-32 bg-purple-400 rounded-full opacity-20 blur-xl animate-pulse"></div>
        <div className="absolute bottom-32 right-16 w-48 h-48 bg-indigo-400 rounded-full opacity-20 blur-xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-purple-300 rounded-full opacity-10 blur-2xl animate-pulse delay-500"></div>
      </div>

      <div className="relative z-10 max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Spiritual Assessment
          </h1>
          <p className="text-purple-200 text-lg md:text-xl max-w-2xl mx-auto">
            Discover your emotional quotient and spiritual path through these thoughtful questions
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-purple-200 text-sm">
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <span className="text-purple-200 text-sm">
              {Math.round(progress)}% Complete
            </span>
          </div>
          <div className="w-full bg-white bg-opacity-20 rounded-full h-2">
            <div 
              className="progress-bar h-2 rounded-full transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Question Card */}
        <div className="glass-effect rounded-2xl p-8 md:p-12 spiritual-glow mb-8">
          <div className="fade-in">
            <h2 className="text-2xl md:text-3xl font-semibold text-white mb-8 leading-relaxed">
              {questions[currentQuestion]?.question}
            </h2>

            <div className="grid gap-4 md:gap-6">
              {questions[currentQuestion]?.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleOptionSelect(index, option)}
                  className={`text-left p-6 rounded-xl border-2 transition-all duration-300 ${
                    selectedOption?.index === index
                      ? 'border-purple-400 bg-purple-500 bg-opacity-30 spiritual-glow'
                      : 'border-purple-300 border-opacity-30 bg-white bg-opacity-5 hover:bg-opacity-10 hover:border-opacity-50'
                  }`}
                >
                  <div className="flex items-start">
                    <div className={`w-6 h-6 rounded-full border-2 mr-4 mt-1 flex-shrink-0 ${
                      selectedOption?.index === index
                        ? 'border-purple-300 bg-purple-400'
                        : 'border-purple-300 border-opacity-50'
                    }`}>
                      {selectedOption?.index === index && (
                        <div className="w-2 h-2 bg-white rounded-full m-1"></div>
                      )}
                    </div>
                    <span className="text-white text-lg leading-relaxed">{option}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center">
          <button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className="flex items-center px-6 py-3 text-purple-300 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Previous
          </button>

          <div className="flex space-x-2">
            {questions.map((_, index) => (
              <div
                key={index}
                className={`w-3 h-3 rounded-full transition-all duration-300 ${
                  index < currentQuestion
                    ? 'bg-purple-400'
                    : index === currentQuestion
                    ? 'bg-purple-300'
                    : 'bg-white bg-opacity-20'
                }`}
              />
            ))}
          </div>

          <button
            onClick={handleNext}
            disabled={selectedOption === null}
            className="flex items-center px-8 py-3 spiritual-button text-white font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            {currentQuestion === questions.length - 1 ? 'Complete Assessment' : 'Next'}
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default OnboardingFlow;
