import { afterEach, describe, expect, it, vi } from 'vitest'
import { loadTasks, saveTasks, TASK_STORAGE_KEY } from './taskStorage'
const store = new Map()
vi.stubGlobal('localStorage', { getItem: (key) => store.get(key) ?? null, setItem: (key, value) => store.set(key, value), clear: () => store.clear() })
afterEach(() => store.clear())
describe('task storage', () => {
  it('serializes and parses task arrays', () => { const tasks = [{ id: 'task-1', title: 'Study' }]; expect(saveTasks(tasks)).toEqual({ ok: true }); expect(JSON.parse(store.get(TASK_STORAGE_KEY))).toEqual(tasks); expect(loadTasks()).toEqual({ tasks, error: null }) })
  it('preserves invalid stored content and reports the issue', () => { store.set(TASK_STORAGE_KEY, '{broken'); expect(loadTasks().error).toMatch(/preserved/); expect(store.get(TASK_STORAGE_KEY)).toBe('{broken') })
})
