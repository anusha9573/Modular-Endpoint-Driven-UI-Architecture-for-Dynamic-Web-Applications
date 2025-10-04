export default function BriefInput({ container }) {
  this.container = container;
  this.onSubmit = null;

  const textarea = document.createElement('textarea');
  textarea.id = 'brief';
  textarea.rows = 6;
  textarea.placeholder = 'Paste your project brief here';
  textarea.style.width = '100%';

  const btn = document.createElement('button');
  btn.textContent = 'Generate Tasks';
  btn.style.marginTop = '8px';

  btn.addEventListener('click', () => {
    const val = textarea.value.trim();
    if (!val) return;
    if (this.onSubmit) this.onSubmit(val);
  });

  container.appendChild(textarea);
  container.appendChild(btn);
}
