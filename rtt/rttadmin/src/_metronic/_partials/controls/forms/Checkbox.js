import React from 'react';

export const Checkbox = ({ isSelected, onChange, children }) => (
  <>
    <input type="checkbox" style={{ display: 'none' }} />
    <label className="checkbox checkbox-lg checkbox-single">
      <input type="checkbox" checked={isSelected} onChange={onChange} />
      {children}
      <span />
    </label>
  </>
);