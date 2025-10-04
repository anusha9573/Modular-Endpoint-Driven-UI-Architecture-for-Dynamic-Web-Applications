import BriefInput from './components/BriefInput.js';
import TaskList from './components/TaskList.js';
import StructuredView from './components/StructuredView.js';
import BlueprintView from './components/BlueprintView.js';
import DownloadButton from './components/DownloadButton.js';

const briefRoot = document.getElementById('briefRoot');
const tasksRoot = document.getElementById('tasksRoot');
const structuredRoot = document.getElementById('structuredRoot');
const blueprintRoot = document.getElementById('blueprintRoot');
const downloadRoot = document.getElementById('downloadRoot');

const briefInput = new BriefInput({ container: briefRoot });
const taskList = new TaskList({ container: tasksRoot });
const structuredView = new StructuredView({ container: structuredRoot });
const blueprintView = new BlueprintView({ container: blueprintRoot });
const downloadBtn = new DownloadButton({ container: downloadRoot });

briefInput.onSubmit = async (text) => {
  taskList.setLoading(true);
  structuredView.clear();
  blueprintView.clear();
  downloadBtn.hide();
  try {
    const res = await fetch('/generate_tasks?fast=true', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!res.ok) {
      const err = await res.text();
      taskList.setError(`Error: ${res.status} ${err}`);
      return;
    }
    const data = await res.json();
    taskList.setTasks(data.tasks || []);
    structuredView.setStructured(data.structured || []);
    // fetch blueprint
    const bpRes = await fetch('/blueprint');
    if (bpRes.ok) {
      const bp = await bpRes.json();
      blueprintView.setBlueprint(bp);
      downloadBtn.show();
    }
  } catch (e) {
    taskList.setError('Network error: ' + e.toString());
  } finally {
    taskList.setLoading(false);
  }
};
