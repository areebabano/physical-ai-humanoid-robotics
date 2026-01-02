import React from 'react';
import NavbarItem from '@theme/NavbarItem';
import NavbarItemCustomAuthButtons from '../NavbarItemCustomAuthButtons';

// Register the custom NavbarItem type
const Type = (props) => {
  return <NavbarItemCustomAuthButtons {...props} />;
};

export default Type;