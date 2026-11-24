# TaskFlow — Student Productivity Manager

A lightweight student planner for organizing coursework,
assignments, and deadlines.

## Problem statement

Students often track assignments across notebooks, messages, and learning platforms. TaskFlow provides one simple browser-based workspace for recording tasks, prioritising them, and seeing what needs attention first.

## Features

- Create, edit, and delete tasks with confirmation.
- Mark tasks complete or reopen them later.
- Search titles case-insensitively and combine search with status filters.
- Sort pending tasks by due date, keep undated tasks after dated work, and show completed tasks last.
- Flag overdue incomplete tasks without time-zone conversion errors.
- Persist tasks in browser `localStorage` under `taskflow.tasks.v1`.
- Responsive, keyboard-friendly dashboard with accessible modal controls and reduced-motion support.

## Technology stack

- React and Vite
- JavaScript (ES6+), HTML5, and pure CSS3
- React `useState` with a custom `useTasks` hook
- Vitest
- GitHub Actions and GitHub Pages

## Folder structure

```text
src/
├── components/       # Layout and reusable UI
├── features/         # Dashboard and task UI
├── hooks/            # useTasks state operations
├── services/         # localStorage access
├── styles/           # CSS variables, layout, components, responsive rules
└── utils/            # validation and task business rules
```

## Install and run locally

```bash
npm install
npm run dev
```

## Test, build, and preview

```bash
npm run test
npm run build
npm run preview
```

## GitHub Pages deployment

The workflow in `.github/workflows/deploy.yml` tests and builds the application on each push to `main`, then deploys the generated `dist` folder using GitHub Pages Actions. After creating the public GitHub repository named `UCS745-Q1-TaskFlow`, open **Settings → Pages** and select **GitHub Actions** as the source. The expected URL is:

`Live website: https://puneetgarg189.github.io/UCS745-Q1-TaskFlow/`

The Vite base path is configured for this repository name.

## Data persistence

Tasks are saved only in this browser profile through `localStorage`. They persist across refreshes and browser restarts, but do not synchronise across browsers or devices. If stored data cannot be parsed, TaskFlow preserves it rather than silently overwriting it and shows a recovery warning.

## Current limitations

- No user accounts or cross-device synchronisation.
- No reminders or calendar integration.
- Data is limited to the browser’s local storage capacity.

## Future enhancements

- Calendar and weekly planning views.
- Optional task tags and course grouping.
- Import/export of task data.
- User-selectable themes.
