import React, {useState} from 'react';
// Component for: Build an AI-powered personal finance web app that automatically categorizes expenses from uploaded bank statements, provides visual spending insights, and recommends saving strategies based on user behavior
export default function BriefInput() {
  const [value, setValue] = useState('');
  return (
    <div>
      <textarea value={value} onChange={e => setValue(e.target.value)} />
    </div>
  );
}
