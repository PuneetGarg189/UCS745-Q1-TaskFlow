export default function AppLayout({ sidebar, children }) { return <div className="app-shell">{sidebar}<div className="app-content">{children}</div></div> }
