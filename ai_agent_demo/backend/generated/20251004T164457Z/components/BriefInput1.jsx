import React, {useState} from 'react';
// Component for: Develop an AI-powered travel booking app with personalized itinerary suggestions and dynamic pricing.
export default function BriefInput() {
  const [value, setValue] = useState('');
  return (
    <div>
      <textarea value={value} onChange={e => setValue(e.target.value)} />
    </div>
  );
}
