import React from 'react';

export default function AvatarVisualization() {
  return (
    <div style={{
      width: '100%',
      height: 400,
      background: 'radial-gradient(ellipse at center, #0a1833 60%, #000 100%)',
      borderRadius: 24,
      boxShadow: '0 8px 32px #00bfff33',
      position: 'relative',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: '#00bfff',
      fontSize: '18px',
      fontWeight: '500'
    }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{
          width: 120,
          height: 120,
          border: '2px solid #00bfff',
          borderRadius: '50%',
          margin: '0 auto 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'rgba(0, 191, 255, 0.1)',
          boxShadow: '0 0 20px rgba(0, 191, 255, 0.3)'
        }}>
          <span style={{ fontSize: '48px' }}>🧘</span>
        </div>
        <div>Emotional Avatar</div>
        <div style={{ fontSize: '14px', opacity: 0.7, marginTop: '8px' }}>
          Visualization unavailable
        </div>
      </div>
    </div>
  );
} 