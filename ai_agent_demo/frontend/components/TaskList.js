export default function TaskList({ container }) {
  this.container = container;
  this._listEl = document.createElement('pre');
  this._listEl.id = 'tasks';
  this._listEl.textContent = 'No tasks yet.';
  container.appendChild(this._listEl);

  this.setTasks = (tasks) => {
    if (!tasks || !tasks.length) {
      this._listEl.textContent = 'No tasks generated.';
      return;
    }
    this._listEl.textContent = tasks.join('\n');
  };
  this.setLoading = (flag) => {
    this._listEl.textContent = flag ? 'Generating tasks...' : this._listEl.textContent;
  };
  this.setError = (msg) => { this._listEl.textContent = msg; };
}
