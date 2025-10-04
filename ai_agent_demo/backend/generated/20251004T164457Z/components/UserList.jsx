import React from 'react';
// List component for User
export default function UserList({ items }) {
  return (<ul>{items.map((it,i)=> <li key={i}>{JSON.stringify(it)}</li>)}</ul>);
}
