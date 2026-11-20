import TaskCard from './TaskCard'
export default function TaskList(props) { return <div className="task-list">{props.tasks.map((task) => <TaskCard key={task.id} task={task} {...props} />)}</div> }
