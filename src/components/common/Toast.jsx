import { useEffect } from 'react'
export default function Toast({ message, type, onClose }) { useEffect(() => { const timer = setTimeout(onClose, 3600); return () => clearTimeout(timer) }, [onClose]); return <div className={`toast ${type}`} role="status"><span>{type === 'error' ? '!' : '✓'}</span>{message}<button onClick={onClose} aria-label="Dismiss notification">×</button></div> }
