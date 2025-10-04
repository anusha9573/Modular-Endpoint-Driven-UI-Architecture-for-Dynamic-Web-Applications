import React, {useState} from 'react';
// Component for: Start modular project: create reusable components for upload, list, charts; backend APIs for auth and expenses; DB schema and workflows.
export default function BriefInput() {
  const [value, setValue] = useState('');
  return (
    <div>
      <textarea value={value} onChange={e => setValue(e.target.value)} />
    </div>
  );
}
