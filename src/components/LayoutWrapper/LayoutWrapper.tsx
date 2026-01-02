import React, { ReactNode } from 'react';

interface LayoutWrapperProps {
  children: ReactNode;
}

const LayoutWrapper: React.FC<LayoutWrapperProps> = ({ children }) => {
  return (
    <>
      {children}
    </>
  );
};

export default LayoutWrapper;