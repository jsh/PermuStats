### 🏔️ The AI-Human Collaborative Workflow Guide

#### 1. The "Piton" Strategy (Git)
* **Micro-Commits:** Commit often. Do not wait for `ruff` or `pytest` to pass for local history.
* **Anchor Points:** Use `git commit -m "WIP: Phase 5 anchor" --no-verify` to save your progress before trying a risky AI snippet.
* **The "Reset" Rope:** If the AI leads you into a "whack-a-mole" trap, `git reset --hard` back to your last known good anchor.

#### 2. Managing the AI Loop
* **The "Abort & Elevate" Rule:** If Builder fails twice to fix a bug, stop. Take the logs back to the Architect (Green tab) to redefine the blueprint.
* **Context Snapshots:** Periodically feed the AI a `tree` of your project and a concatenated block of your core `.py` files to refresh its memory.
* **The Log Strategy:** Maintain a `log.md` of high-level architectural decisions. Paste relevant sections to the AI when it asks "Why?"

#### 3. Tab-Group Infrastructure
* **Green (Architect):** High-level design, `todo.md` management, and "Master Work Orders."
* **Red (Builder):** Execution, debugging, and implementation.
* **Yellow (General Tech):** One-off questions about library syntax or math (e.g., "How does Stirling recurrence work?").
* **Blue (The Inspector):** After code is written, take it here for a "Peer Review" to find edge cases the Builder missed.

#### 4. Toolchain & Environment
* **The Astral Stack:** Use `uv` for lightning-fast env management, `ruff` for linting, and `ty` for type safety.
* **CI/CD:** Let GitHub Actions be the "Final Exam." Use local hooks for "Quizzes" to keep the inner loop fast.
* **The "Copy-Paste" Contract:** Use code blocks for all AI instructions to minimize manual typing errors.

#### 5. Moving Toward Neovim Integration
* **Vim-Pureness vs. Speed:** If copy-pasting feels like a chore, consider `avante.nvim` or `gp.nvim`. They bring the "Builder" into your buffer while keeping your decades of muscle memory intact.
