import { useState } from 'react'
import AppLayout from './components/layout/AppLayout'
import Header from './components/layout/Header'
import Sidebar from './components/layout/Sidebar'
import Toast from './components/common/Toast'
import StatsOverview from './features/dashboard/StatsOverview'
import EmptyState from './features/tasks/EmptyState'
import SearchBar from './features/tasks/SearchBar'
import TaskFilters from './features/tasks/TaskFilters'
import TaskFormModal from './features/tasks/TaskFormModal'
import TaskList from './features/tasks/TaskList'
import { useTasks } from './hooks/useTasks'

export default function App() {
  const [filter, setFilter] = useState('all')
  const [query, setQuery] = useState('')
  const [editingTask, setEditingTask] = useState(null)
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [toast, setToast] = useState(null)
  const { tasks, error, addTask, updateTask, removeTask, toggleTask, stats } = useTasks()
  const visibleTasks = tasks.filter((task) => (filter === 'all' || (filter === 'completed' ? task.completed : !task.completed)) && task.title.toLowerCase().includes(query.trim().toLowerCase()))
  const notify = (message, type = 'success') => setToast({ message, type })
  const openCreate = () => { setEditingTask(null); setIsFormOpen(true) }
  const saveTask = (data) => { const result = editingTask ? updateTask(editingTask.id, data) : addTask(data); if (result.ok) { setIsFormOpen(false); notify(editingTask ? 'Task updated.' : 'Task added.') } else notify(result.error, 'error'); return result }
  const deleteTask = (task) => { if (window.confirm(`Delete “${task.title}”? This action cannot be undone.`)) { const result = removeTask(task.id); result.ok ? notify('Task deleted.') : notify(result.error, 'error') } }
  return <AppLayout sidebar={<Sidebar activeFilter={filter} onSelect={setFilter} stats={stats} />}><Header onAddTask={openCreate} /><main className="dashboard" id="main-content">{error && <div className="storage-warning" role="alert">{error}</div>}<section className="hero" aria-labelledby="dashboard-title"><div><p className="eyebrow">Student workspace</p><h1 id="dashboard-title">Stay ahead of every deadline.</h1><p>Plan coursework, focus on what matters, and keep your momentum.</p></div><button className="mobile-add" onClick={openCreate}>+ Add task</button></section><StatsOverview stats={stats} /><section className="tasks-panel" aria-labelledby="tasks-title"><div className="section-heading"><div><h2 id="tasks-title">Your tasks</h2><p>{visibleTasks.length} {visibleTasks.length === 1 ? 'task' : 'tasks'} shown</p></div></div><div className="task-tools"><SearchBar value={query} onChange={setQuery} /><TaskFilters value={filter} onChange={setFilter} /></div>{visibleTasks.length ? <TaskList tasks={visibleTasks} onEdit={(task) => { setEditingTask(task); setIsFormOpen(true) }} onDelete={deleteTask} onToggle={(task) => { const result = toggleTask(task.id); result.ok ? notify(task.completed ? 'Task reopened.' : 'Task completed.') : notify(result.error, 'error') }} /> : <EmptyState hasTasks={tasks.length > 0} onAdd={openCreate} />}</section></main>{isFormOpen && <TaskFormModal task={editingTask} onClose={() => setIsFormOpen(false)} onSave={saveTask} />}{toast && <Toast {...toast} onClose={() => setToast(null)} />}</AppLayout>
}
