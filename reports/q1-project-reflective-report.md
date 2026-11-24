# TaskFlow Project Reflective Report

## Project summary

TaskFlow was developed as a React and Vite student productivity application for UCS 745 Q1. The application enables students to create, edit, delete, complete, reopen, search, filter, prioritise, and organise coursework tasks. Attendance-style dashboard statistics are derived from saved task records rather than hardcoded values. Tasks persist in browser localStorage under `taskflow.tasks.v1`.

## Development and testing

The project used a modular frontend structure with reusable layout and task components, a `useTasks` hook for task operations, isolated storage access, and utilities for validation, ordering, overdue identification, and statistics. Pure CSS was used for the responsive interface.

Nine automated Vitest tests passed. They covered validation, sorting, overdue calculation, combined search/filtering, dashboard statistics, and storage serialisation/parsing. Manual smoke checks confirmed task creation, task completion, persistence after refresh, overdue display, and mobile responsiveness. The production Vite build completed successfully.

## GitHub and deployment

The public repository was created at `PuneetGarg189/UCS745-Q1-TaskFlow`. GitHub Actions was configured to run `npm ci`, the automated test suite, and the production build before publishing the Pages artifact. The deployment completed successfully, and the live application is available at `https://puneetgarg189.github.io/UCS745-Q1-TaskFlow/`.

## Conflict-resolution process

The intentional conflict was isolated to the README description paragraph, leaving application code unaffected. Both branches, `feature-a-readme-title` and `feature-b-readme-title`, began at common base commit `e30593a`. Feature A changed the paragraph and was successfully integrated with merge commit `4208683`. Feature B changed the same paragraph differently, producing an actual content conflict during the second merge. The conflict was inspected with `git status` and `git diff`, then resolved manually by replacing the conflicting alternatives with an agreed final description. Resolution commit `614a1d` was pushed to `main`, and the final workflow passed.

## Key lessons learned

This project demonstrated the value of separating business rules from UI components, testing derived behaviour rather than hardcoding outputs, and using reproducible CI before deployment. The real merge conflict showed why branches must share a common base and why conflicts must be inspected and resolved deliberately. Maintaining concise, meaningful commits and a clean working tree made final verification straightforward.
