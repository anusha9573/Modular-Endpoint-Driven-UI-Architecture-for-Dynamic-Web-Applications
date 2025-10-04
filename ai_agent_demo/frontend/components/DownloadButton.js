export default function DownloadButton({ container }) {
  this.container = container;
  const btn = document.createElement('button');
  btn.textContent = 'Download Generated ZIP';
  btn.style.display = 'none';
  btn.addEventListener('click', () => {
    window.location = '/export_latest';
  });
  container.appendChild(btn);
  this.show = () => { btn.style.display = 'inline-block'; };
  this.hide = () => { btn.style.display = 'none'; };
}
