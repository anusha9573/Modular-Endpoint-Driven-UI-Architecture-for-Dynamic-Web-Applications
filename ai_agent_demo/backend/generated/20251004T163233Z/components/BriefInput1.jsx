import React, {useState} from 'react';
// Component for: Create a small app to upload bank statements, parse expenses, and show a dashboard with charts.
export default function BriefInput() {
  const [value, setValue] = useState('');
  return (
    <div>
      <textarea value={value} onChange={e => setValue(e.target.value)} />
    </div>
  );
}
