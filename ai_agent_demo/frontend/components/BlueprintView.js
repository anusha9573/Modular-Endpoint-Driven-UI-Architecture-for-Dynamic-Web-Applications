export default function BlueprintView({ container }) {
  this.container = container;
  this.clear = () => { this.container.innerHTML = ''; };
  this.setBlueprint = (bp) => {
    this.clear();
    const pre = document.createElement('pre');
    pre.textContent = JSON.stringify(bp, null, 2);
    pre.style.maxHeight = '360px';
    pre.style.overflow = 'auto';
    pre.style.background = '#f7f7f7';
    pre.style.padding = '8px';
    pre.style.border = '1px solid #eee';
    this.container.appendChild(pre);

    // Summary sections
    const summary = document.createElement('div');
    summary.style.marginTop = '10px';
    const addList = (name, items) => {
      const h = document.createElement('h4');
      h.textContent = name;
      summary.appendChild(h);
      if (!items || !items.length) {
        const none = document.createElement('div'); none.textContent = '— none —'; summary.appendChild(none); return;
      }
      const ul = document.createElement('ul');
      items.forEach(it => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.textContent = it.task;
        if (it.output) { a.href = '/generated/' + it.output.replace(/^\/+/, ''); a.target = '_blank'; }
        li.appendChild(a);
        if (it.routes) {
          const small = document.createElement('div'); small.style.fontSize = '0.9em'; small.style.color = '#555'; small.textContent = 'Routes: ' + it.routes.join(', ');
          li.appendChild(small);
        }
        ul.appendChild(li);
      });
      summary.appendChild(ul);
    };
    addList('Components', bp.components || []);
    addList('APIs', bp.apis || []);
    addList('Models', bp.models || []);
    addList('Schemas', bp.schemas || []);
    addList('Workflows', bp.workflows || []);
    this.container.appendChild(summary);
  };
}
