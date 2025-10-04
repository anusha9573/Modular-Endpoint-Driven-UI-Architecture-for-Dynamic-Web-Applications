const submit = document.getElementById('submit');
const briefEl = document.getElementById('brief');
const tasksEl = document.getElementById('tasks');

submit.addEventListener('click', async () => {
  const brief = briefEl.value.trim();
  if (!brief) {
    tasksEl.textContent = 'Please enter a project brief.';
    return;
  }

  tasksEl.textContent = 'Generating tasks...';

  try {
    const res = await fetch('/generate_tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: brief })
    });
    if (!res.ok) {
      const err = await res.text();
      tasksEl.textContent = `Error: ${res.status} ${err}`;
      return;
    }
    const data = await res.json();
    tasksEl.textContent = data.tasks.join('\n');
    // show structured output (if present)
    const structuredDiv = document.getElementById('structured');
    structuredDiv.innerHTML = '';
    if (data.structured && data.structured.length) {
      data.structured.forEach(s => {
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
        structuredDiv.appendChild(card);
      });
      // show download
      const dl = document.getElementById('download');
      dl.style.display = 'inline-block';
      dl.onclick = () => { window.location = '/export_latest' };

      // fetch blueprint and show in dedicated area
      try {
        const bpResp = await fetch('/blueprint');
        if (bpResp.ok) {
          const bp = await bpResp.json();
          const bpWrap = document.getElementById('blueprintWrap');
          const bpPre = document.getElementById('blueprint');
          bpPre.textContent = JSON.stringify(bp, null, 2);
          bpWrap.style.display = 'block';
          // render categorized summary below the JSON
          renderBlueprintSummary(bp);
          const copyBtn = document.getElementById('copyBlueprint');
          copyBtn.onclick = () => {
            navigator.clipboard.writeText(bpPre.textContent).then(() => {
              copyBtn.textContent = 'Copied';
              setTimeout(() => copyBtn.textContent = 'Copy JSON', 1500);
            }).catch(() => alert('Copy failed'));
          };
        }
      } catch (e) {
        console.warn('blueprint fetch failed', e);
      }
    } else {
      structuredDiv.textContent = 'No structured output.';
    }
  } catch (e) {
    tasksEl.textContent = 'Network error: ' + e.toString();
  }
});

function renderList(title, items) {
  const container = document.createElement('div');
  const h = document.createElement('h4');
  h.textContent = title;
  container.appendChild(h);
  if (!items || !items.length) {
    const none = document.createElement('div');
    none.textContent = '— none —';
    container.appendChild(none);
    return container;
  }
  const ul = document.createElement('ul');
  items.forEach(it => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.textContent = it.task;
    if (it.output) {
      a.href = '/generated/' + it.output.replace(/^\/+/, '');
      a.target = '_blank';
    }
    li.appendChild(a);
    if (it.routes && it.routes.length) {
      const small = document.createElement('div');
      small.style.fontSize = '0.9em';
      small.style.color = '#555';
      small.textContent = 'Routes: ' + it.routes.join(', ');
      li.appendChild(small);
    }
    container.appendChild(li);
  });
  return container;
}

function renderBlueprintSummary(bp) {
  const structuredDiv = document.getElementById('structured');
  const wrap = document.createElement('div');
  wrap.style.borderTop = '1px solid #eee';
  wrap.style.marginTop = '8px';
  const title = document.createElement('h3');
  title.textContent = 'Project Start Summary';
  wrap.appendChild(title);
  wrap.appendChild(renderList('Components', bp.components || []));
  wrap.appendChild(renderList('APIs', bp.apis || []));
  wrap.appendChild(renderList('Models', bp.models || []));
  wrap.appendChild(renderList('Schemas', bp.schemas || []));
  wrap.appendChild(renderList('Workflows', bp.workflows || []));
  structuredDiv.appendChild(wrap);
}
