import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import { AuthProvider } from '../../contexts/AuthContext';

export default function Layout(props) {
  return (
    <AuthProvider>
      <OriginalLayout {...props} />
    </AuthProvider>
  );
}