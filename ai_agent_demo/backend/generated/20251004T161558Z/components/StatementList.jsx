import React from 'react';
// List component for Statement
export default function StatementList({ items }) {
  return (<ul>{items.map((it,i)=> <li key={i}>{JSON.stringify(it)}</li>)}</ul>);
}
