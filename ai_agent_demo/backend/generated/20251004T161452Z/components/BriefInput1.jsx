import React, {useState} from 'react';
// Component for: Build an AI-powered personal finance web app that categorizes expenses and provides insights
export default function BriefInput() {
  const [value, setValue] = useState('');
  return (
    <div>
      <textarea value={value} onChange={e => setValue(e.target.value)} />
    </div>
  );
}
