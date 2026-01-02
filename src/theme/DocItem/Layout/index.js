import React from 'react';
import clsx from 'clsx';
import { useDoc } from '@docusaurus/plugin-content-docs/client';
import DocItemPaginator from '@theme/DocItem/Paginator';
import DocVersionBanner from '@theme/DocVersionBanner';
import DocVersionBadge from '@theme/DocVersionBadge';
import { theme } from '@docusaurus/preset-classic';
import DocBreadcrumbs from '@theme/DocBreadcrumbs';
import DocItemFooter from '@theme/DocItem/Footer';
import DocItemContent from '@theme/DocItem/Content';
import styles from './styles.module.css';

// Professional DocItem Layout Component
export default function DocItemLayout({ children }) {
  const doc = useDoc();
  const { metadata } = doc;
  const { permalink, title } = metadata;

  return (
    <div className="doc-item-container">
      <div className="doc-item-layout">
        <div className="doc-item-header">
          <DocBreadcrumbs />
          <DocVersionBanner />
          <DocVersionBadge />
          <h1 className="doc-item-title">{title}</h1>
        </div>

        <div className="doc-item-content-container">
          <div className="doc-item-content">
            <DocItemContent>{children}</DocItemContent>
          </div>
        </div>

        <div className="doc-item-footer">
          <DocItemFooter />
          <DocItemPaginator />
        </div>
      </div>

      <style jsx>{`
        .doc-item-container {
          padding: 2rem 1rem;
          background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
          min-height: calc(100vh - 200px);
        }

        .doc-item-layout {
          max-width: 1200px;
          margin: 0 auto;
          background: #2d2d2d;
          border-radius: 12px;
          padding: 2.5rem;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
          border: 1px solid #4fc3f7;
          backdrop-filter: blur(10px);
        }

        .doc-item-header {
          margin-bottom: 2rem;
          padding-bottom: 1.5rem;
          border-bottom: 2px solid #4fc3f7;
        }

        .doc-item-title {
          color: #4fc3f7;
          font-size: 2.2rem;
          margin: 0.5rem 0 1rem 0;
          font-weight: 700;
        }

        .doc-item-content-container {
          margin: 1.5rem 0;
        }

        .doc-item-content {
          color: #e0e0e0;
          line-height: 1.8;
        }

        .doc-item-content :where(h1, h2, h3, h4, h5, h6) {
          color: #4fc3f7;
          border-bottom: 1px solid #4fc3f7;
          padding-bottom: 0.5rem;
          margin-top: 2rem;
          margin-bottom: 1rem;
        }

        .doc-item-content p {
          margin-bottom: 1.2rem;
          font-size: 1.1rem;
          line-height: 1.7;
        }

        .doc-item-content code {
          background-color: #1a1a1a;
          color: #4fc3f7;
          padding: 0.2rem 0.4rem;
          border-radius: 4px;
          font-size: 0.9em;
        }

        .doc-item-content pre {
          background-color: #1a1a1a;
          border: 1px solid #4fc3f7;
          border-radius: 8px;
          padding: 1rem;
          margin: 1.5rem 0;
          overflow-x: auto;
        }

        .doc-item-content blockquote {
          border-left: 4px solid #4fc3f7;
          background-color: rgba(79, 195, 247, 0.1);
          padding: 1rem 1.5rem;
          margin: 1.5rem 0;
          border-radius: 0 4px 4px 0;
        }

        .doc-item-footer {
          margin-top: 2.5rem;
          padding-top: 1.5rem;
          border-top: 1px solid #4fc3f7;
        }

        @media (max-width: 768px) {
          .doc-item-layout {
            padding: 1.5rem;
            margin: 1rem;
          }

          .doc-item-title {
            font-size: 1.8rem;
          }
        }
      `}</style>
    </div>
  );
}