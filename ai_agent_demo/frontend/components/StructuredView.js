export default function StructuredView({ container }) {
  this.container = container;
  this.clear = () => { this.container.innerHTML = ''; };
  this.setStructured = (items) => {
    this.clear();
    if (!items || !items.length) {
      this.container.textContent = 'No structured output.';
      return;
    }
    items.forEach(s => {
      const card = document.createElement('div');
      card.style.border = '1px solid #ddd';
      card.style.padding = '8px';
      card.style.margin = '6px 0';
      const title = document.createElement('div');
      title.textContent = `${s.role.toUpperCase()}: ${s.title}`;
      title.style.fontWeight = '600';
      const desc = document.createElement('div');
      desc.textContent = s.description;
      const pre = document.createElement('pre');
      pre.textContent = s.code || '';
      card.appendChild(title);
      card.appendChild(desc);
      card.appendChild(pre);
      this.container.appendChild(card);
    });
  };
}
