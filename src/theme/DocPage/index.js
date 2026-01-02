import React from 'react';
import DocPage from '@theme-original/DocPage';
import { useColorMode } from '@docusaurus/theme-common';
import { useEffect } from 'react';

// Enhanced DocPage component with professional styling
export default function DocPageEnhanced(props) {
  const { colorMode } = useColorMode();

  // Apply theme-specific styling
  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.body.setAttribute('data-theme', colorMode);
    }
  }, [colorMode]);

  return (
    <>
      <style jsx>{`
        .doc-page {
          background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
          min-height: 100vh;
        }

        .doc-container {
          max-width: 1400px;
          margin: 0 auto;
          padding: 2rem;
        }

        .doc-content {
          background: #2d2d2d;
          border-radius: 12px;
          padding: 2.5rem;
          margin: 1.5rem 0;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
          border: 1px solid #4fc3f7;
          backdrop-filter: blur(10px);
        }

        .doc-header {
          border-bottom: 2px solid #4fc3f7;
          padding-bottom: 1rem;
          margin-bottom: 2rem;
        }

        .doc-title {
          color: #4fc3f7;
          font-size: 2.5rem;
          margin: 0 0 1rem 0;
          font-weight: 700;
        }

        .doc-subtitle {
          color: #e0e0e0;
          font-size: 1.2rem;
          margin: 0 0 1.5rem 0;
          font-style: italic;
        }

        .doc-toc {
          background: #1a1a1a;
          border-radius: 8px;
          padding: 1.5rem;
          margin: 1rem 0;
          border: 1px solid #4fc3f7;
        }

        .doc-footer {
          margin-top: 2rem;
          padding-top: 1.5rem;
          border-top: 1px solid #4fc3f7;
          color: #b0bec5;
          font-size: 0.9rem;
        }

        @media (max-width: 768px) {
          .doc-content {
            padding: 1.5rem;
            margin: 1rem 0;
          }

          .doc-title {
            font-size: 2rem;
          }
        }
      `}</style>
      <div className="doc-page">
        <div className="doc-container">
          <DocPage {...props} />
        </div>
      </div>
    </>
  );
}