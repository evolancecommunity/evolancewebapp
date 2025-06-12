import React, { useState, useEffect, useContext, useRef } from 'react';
import { AuthContext } from '../App';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const VideoLessons = () => {
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [userReview, setUserReview] = useState({ rating: 5, review_text: '' });
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [videoLoading, setVideoLoading] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  
  const videoRef = useRef(null);
  const containerRef = useRef(null);

  const { user, API } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetchVideos();
  }, []);

  useEffect(() => {
    if (selectedVideo) {
      fetchVideoReviews(selectedVideo.id);
    }
  }, [selectedVideo]);

  const fetchVideos = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/videos`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setVideos(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching videos:', error);
      setLoading(false);
    }
  };

  const fetchVideoReviews = async (videoId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/videos/${videoId}/reviews`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setReviews(response.data);
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  };

  const submitReview = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API}/videos/review`, {
        video_id: selectedVideo.id,
        rating: userReview.rating,
        review_text: userReview.review_text
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setShowReviewForm(false);
      setUserReview({ rating: 5, review_text: '' });
      fetchVideoReviews(selectedVideo.id);
    } catch (error) {
      console.error('Error submitting review:', error);
    }
  };

  const toggleFullscreen = () => {
    if (!isFullscreen) {
      if (containerRef.current.requestFullscreen) {
        containerRef.current.requestFullscreen();
      } else if (containerRef.current.webkitRequestFullscreen) {
        containerRef.current.webkitRequestFullscreen();
      } else if (containerRef.current.msRequestFullscreen) {
        containerRef.current.msRequestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
      }
    }
    setIsFullscreen(!isFullscreen);
  };

  const changePlaybackSpeed = (speed) => {
    setPlaybackSpeed(speed);
    if (videoRef.current) {
      videoRef.current.playbackRate = speed;
    }
  };

  const getDifficultyColor = (level) => {
    switch (level) {
      case 1: return 'bg-green-500';
      case 2: return 'bg-yellow-500';
      case 3: return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getDifficultyText = (level) => {
    switch (level) {
      case 1: return 'Beginner';
      case 2: return 'Intermediate';
      case 3: return 'Advanced';
      default: return 'Unknown';
    }
  };

  const getAverageRating = () => {
    if (reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, review) => acc + review.rating, 0);
    return (sum / reviews.length).toFixed(1);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="text-center">
          <div className="chakra-loading w-16 h-16 mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading spiritual lessons...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-40 h-40 bg-purple-400 rounded-full opacity-10 blur-xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-60 h-60 bg-indigo-400 rounded-full opacity-10 blur-xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/3 right-1/4 w-32 h-32 bg-purple-300 rounded-full opacity-10 blur-xl animate-pulse delay-500"></div>
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

            <h1 className="text-2xl font-bold text-white">Video Lessons</h1>

            <div className="flex items-center space-x-2">
              <span className="text-purple-200 text-sm">{videos.length} Lessons</span>
            </div>
          </div>
        </div>
      </header>

      <div className="relative z-10 p-6">
        {!selectedVideo ? (
          /* Video Grid */
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
                Spiritual Video Lessons
              </h2>
              <p className="text-purple-200 text-lg md:text-xl max-w-2xl mx-auto">
                Learn from spiritual mentors and deepen your understanding through guided video lessons
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {videos.map((video) => (
                <div
                  key={video.id}
                  className="glass-effect rounded-2xl overflow-hidden spiritual-glow cursor-pointer transform hover:scale-105 transition-all duration-300"
                  onClick={() => setSelectedVideo(video)}
                >
                  {/* Video Thumbnail */}
                  <div className="relative h-48 bg-gradient-to-br from-purple-600 to-indigo-700 flex items-center justify-center">
                    <div className="absolute inset-0 bg-black bg-opacity-40"></div>
                    <svg className="w-16 h-16 text-white opacity-80 z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.01M15 10h1.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    
                    {/* Play Button Overlay */}
                    <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-20 hover:bg-opacity-40 transition-all duration-200">
                      <div className="w-16 h-16 bg-white bg-opacity-90 rounded-full flex items-center justify-center">
                        <svg className="w-8 h-8 text-purple-800 ml-1" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M8 5v14l11-7z"/>
                        </svg>
                      </div>
                    </div>

                    {/* Difficulty Badge */}
                    <div className={`absolute top-4 left-4 px-2 py-1 rounded-full text-xs font-medium text-white ${getDifficultyColor(video.difficulty_level)}`}>
                      {getDifficultyText(video.difficulty_level)}
                    </div>

                    {/* Duration */}
                    <div className="absolute bottom-4 right-4 bg-black bg-opacity-60 px-2 py-1 rounded text-xs text-white">
                      {video.duration}
                    </div>
                  </div>

                  {/* Video Info */}
                  <div className="p-6">
                    <h3 className="text-xl font-semibold text-white mb-2">{video.title}</h3>
                    <p className="text-purple-200 text-sm leading-relaxed mb-4">{video.description}</p>
                    
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="text-purple-300 text-sm font-medium">{video.mentor_name}</p>
                        <p className="text-purple-400 text-xs">{video.category}</p>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center text-yellow-400 text-sm">
                          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                          4.8
                        </div>
                        <p className="text-purple-400 text-xs">24 reviews</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          /* Video Player */
          <div className="max-w-6xl mx-auto">
            <button
              onClick={() => setSelectedVideo(null)}
              className="mb-6 flex items-center text-purple-200 hover:text-white transition-colors duration-200"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Videos
            </button>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Video Player Section */}
              <div className="lg:col-span-2">
                <div 
                  ref={containerRef}
                  className={`video-container relative bg-black rounded-2xl overflow-hidden spiritual-glow ${isFullscreen ? 'fixed inset-0 z-50 rounded-none' : ''}`}
                >
                  {/* Placeholder Video */}
                  <div className="relative w-full h-0 pb-[56.25%]">
                    <div className="absolute inset-0 bg-gradient-to-br from-purple-600 to-indigo-700 flex items-center justify-center">
                      <div className="text-center">
                        <svg className="w-24 h-24 text-white opacity-60 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.01M15 10h1.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="text-white text-lg mb-2">{selectedVideo.title}</p>
                        <p className="text-purple-200">Video content coming soon</p>
                      </div>
                    </div>
                  </div>

                  {/* Video Controls */}
                  <div className="video-controls">
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-4">
                        <button className="text-white hover:text-purple-300 transition-colors">
                          <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M8 5v14l11-7z"/>
                          </svg>
                        </button>
                        
                        <div className="flex items-center space-x-2">
                          <span className="text-white text-sm">Speed:</span>
                          <select 
                            value={playbackSpeed}
                            onChange={(e) => changePlaybackSpeed(parseFloat(e.target.value))}
                            className="bg-black bg-opacity-60 text-white text-sm rounded px-2 py-1"
                          >
                            <option value={0.5}>0.5x</option>
                            <option value={0.75}>0.75x</option>
                            <option value={1}>1x</option>
                            <option value={1.25}>1.25x</option>
                            <option value={1.5}>1.5x</option>
                            <option value={2}>2x</option>
                          </select>
                        </div>
                      </div>

                      <button
                        onClick={toggleFullscreen}
                        className="text-white hover:text-purple-300 transition-colors"
                      >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                {/* Video Information */}
                <div className="mt-6 glass-effect rounded-2xl p-6 spiritual-glow">
                  <h2 className="text-3xl font-bold text-white mb-4">{selectedVideo.title}</h2>
                  <p className="text-purple-200 leading-relaxed mb-6">{selectedVideo.description}</p>
                  
                  <div className="flex flex-wrap items-center gap-4 mb-6">
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-cyan-400 rounded-full flex items-center justify-center mr-3">
                        <span className="text-white font-bold text-lg">{selectedVideo.mentor_name[0]}</span>
                      </div>
                      <div>
                        <p className="text-white font-medium">{selectedVideo.mentor_name}</p>
                        <p className="text-purple-300 text-sm">Spiritual Mentor</p>
                      </div>
                    </div>
                    
                    <div className={`px-3 py-1 rounded-full text-sm font-medium text-white ${getDifficultyColor(selectedVideo.difficulty_level)}`}>
                      {getDifficultyText(selectedVideo.difficulty_level)}
                    </div>
                    
                    <div className="text-purple-300">
                      <span className="text-sm">{selectedVideo.duration}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Reviews Section */}
              <div className="lg:col-span-1">
                <div className="glass-effect rounded-2xl p-6 spiritual-glow">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold text-white">Reviews</h3>
                    <div className="flex items-center">
                      <svg className="w-5 h-5 text-yellow-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                      <span className="text-white font-medium">{getAverageRating()}</span>
                      <span className="text-purple-300 text-sm ml-1">({reviews.length})</span>
                    </div>
                  </div>

                  {/* Add Review Button */}
                  <button
                    onClick={() => setShowReviewForm(!showReviewForm)}
                    className="w-full spiritual-button text-white font-medium py-2 px-4 rounded-lg mb-6 transition-all duration-200"
                  >
                    Add Review
                  </button>

                  {/* Review Form */}
                  {showReviewForm && (
                    <div className="mb-6 p-4 bg-white bg-opacity-10 rounded-lg">
                      <div className="mb-4">
                        <label className="block text-purple-200 text-sm font-medium mb-2">Rating</label>
                        <div className="flex space-x-1">
                          {[1, 2, 3, 4, 5].map((star) => (
                            <button
                              key={star}
                              onClick={() => setUserReview({...userReview, rating: star})}
                              className={`w-8 h-8 ${userReview.rating >= star ? 'text-yellow-400' : 'text-gray-400'}`}
                            >
                              <svg fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                              </svg>
                            </button>
                          ))}
                        </div>
                      </div>
                      
                      <div className="mb-4">
                        <label className="block text-purple-200 text-sm font-medium mb-2">Review</label>
                        <textarea
                          value={userReview.review_text}
                          onChange={(e) => setUserReview({...userReview, review_text: e.target.value})}
                          className="w-full px-3 py-2 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                          rows="3"
                          placeholder="Share your thoughts..."
                        />
                      </div>
                      
                      <div className="flex space-x-2">
                        <button
                          onClick={submitReview}
                          className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
                        >
                          Submit
                        </button>
                        <button
                          onClick={() => setShowReviewForm(false)}
                          className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Reviews List */}
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {reviews.length === 0 ? (
                      <div className="text-center text-purple-300 py-8">
                        <p>No reviews yet. Be the first to share your thoughts!</p>
                      </div>
                    ) : (
                      reviews.map((review, index) => (
                        <div key={review.id || index} className="bg-white bg-opacity-5 rounded-lg p-4">
                          <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center">
                              <div className="w-8 h-8 bg-gradient-to-r from-purple-400 to-cyan-400 rounded-full flex items-center justify-center mr-3">
                                <span className="text-white text-sm font-bold">U</span>
                              </div>
                              <span className="text-white font-medium">User</span>
                            </div>
                            <div className="flex">
                              {[...Array(5)].map((_, i) => (
                                <svg
                                  key={i}
                                  className={`w-4 h-4 ${i < review.rating ? 'text-yellow-400' : 'text-gray-400'}`}
                                  fill="currentColor"
                                  viewBox="0 0 20 20"
                                >
                                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                              ))}
                            </div>
                          </div>
                          <p className="text-purple-200 text-sm leading-relaxed">{review.review_text}</p>
                          <p className="text-purple-400 text-xs mt-2">
                            {new Date(review.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoLessons;
