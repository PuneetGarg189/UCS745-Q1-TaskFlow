import { describe, expect, it } from 'vitest'
import { filterTasks, getStats, isOverdue, sortTasks } from './taskHelpers'

const task = (overrides) => ({ id: 'a', title: 'Assignment', description: '', priority: 'medium', dueDate: '', completed: false, createdAt: '2026-11-01T00:00:00.000Z', updatedAt: '2026-11-01T00:00:00.000Z', ...overrides })

describe('task helpers', () => {
  it('places pending dated tasks first, undated pending next, then completed tasks', () => {
    const tasks = [task({ id: 'done', completed: true, dueDate: '2026-01-01' }), task({ id: 'none' }), task({ id: 'late', dueDate: '2026-12-03' }), task({ id: 'early', dueDate: '2026-11-25' })]
    expect(sortTasks(tasks).map(({ id }) => id)).toEqual(['early', 'late', 'none', 'done'])
  })
  it('marks only incomplete calendar dates before today as overdue', () => {
    const today = new Date(2026, 10, 21)
    expect(isOverdue(task({ dueDate: '2026-11-20' }), today)).toBe(true)
    expect(isOverdue(task({ dueDate: '2026-11-21' }), today)).toBe(false)
    expect(isOverdue(task({ dueDate: '2026-11-20', completed: true }), today)).toBe(false)
  })
  it('combines a case-insensitive search and status filter', () => {
    const tasks = [task({ id: 'one', title: 'Cloud Assignment' }), task({ id: 'two', title: 'Read cloud notes', completed: true }), task({ id: 'three', title: 'Math revision' })]
    expect(filterTasks(tasks, 'pending', 'CLOUD').map(({ id }) => id)).toEqual(['one'])
    expect(filterTasks(tasks, 'completed', 'cloud').map(({ id }) => id)).toEqual(['two'])
  })
  it('derives accurate dashboard statistics', () => expect(getStats([task(), task({ id: 'two', completed: true })])).toEqual({ total: 2, pending: 1, completed: 1 }))
})
