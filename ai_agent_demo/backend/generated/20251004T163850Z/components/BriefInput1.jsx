import React, {useState} from 'react';
// Component for: Start a project: upload bank statements, parse expenses, authenticate users, show charts and recommendations.
export default function BriefInput() {
  const [value, setValue] = useState('');
  return (
    <div>
      <textarea value={value} onChange={e => setValue(e.target.value)} />
    </div>
  );
}
