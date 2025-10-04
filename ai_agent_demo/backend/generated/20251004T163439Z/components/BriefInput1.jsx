import React, {useState} from 'react';
// Component for: Please provide an app that uploads bank statements, parses expenses, and shows charts for insights.
export default function BriefInput() {
  const [value, setValue] = useState('');
  return (
    <div>
      <textarea value={value} onChange={e => setValue(e.target.value)} />
    </div>
  );
}
