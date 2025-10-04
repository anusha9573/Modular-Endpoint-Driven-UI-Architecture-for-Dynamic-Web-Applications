import React from 'react';
// List component for Expense
export default function ExpenseList({ items }) {
  return (<ul>{items.map((it,i)=> <li key={i}>{JSON.stringify(it)}</li>)}</ul>);
}
