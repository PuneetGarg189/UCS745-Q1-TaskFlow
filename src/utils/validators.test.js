import { describe, expect, it } from 'vitest'
import { normalizeTask, validateTask } from './validators'
const valid = { title: ' Submit report ', description: ' Notes ', priority: 'high', dueDate: '2026-11-25' }
describe('task validation', () => {
  it('accepts a valid task and normalizes text', () => { expect(validateTask(valid)).toBeNull(); expect(normalizeTask(valid)).toEqual({ title: 'Submit report', description: 'Notes', priority: 'high', dueDate: '2026-11-25' }) })
  it('rejects empty and oversized fields', () => { expect(validateTask({ ...valid, title: ' ' })).toMatch(/title/); expect(validateTask({ ...valid, description: 'a'.repeat(501) })).toMatch(/Description/) })
  it('rejects unsupported priority values', () => expect(validateTask({ ...valid, priority: 'urgent' })).toMatch(/priority/))
})
