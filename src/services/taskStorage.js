const KEY = 'taskflow.tasks.v1'
export function loadTasks() { try { const raw = localStorage.getItem(KEY); if (!raw) return { tasks: [], error: null }; const parsed = JSON.parse(raw); if (!Array.isArray(parsed)) return { tasks: [], error: 'Saved task data is invalid. Your original data was preserved; clear it manually only if you choose to reset.' }; return { tasks: parsed, error: null } } catch { return { tasks: [], error: 'Saved task data could not be read. Your original data was preserved.' } } }
export function saveTasks(tasks) { try { localStorage.setItem(KEY, JSON.stringify(tasks)); return { ok: true } } catch { return { ok: false, error: 'Tasks could not be saved to this browser.' } } }
export { KEY as TASK_STORAGE_KEY }
