Turn my existing {source_task} implementation in PsyFlow/TAPs into a {target_task} task with as few changes as possible.

**Key requirements:**
- The unit for all stimuli sizes must be in 'deg' (degrees of visual angle).
- When creating the new task, a new folder should be created with the task name, and the temporary `task_cache` folder should be removed.
- All voice-over files (`_voice.mp3`) and other non-relevant files in the `assets/` directory of the source task must be removed.
- When accessing recorded variables for stats (e.g., in `main.py` for break or final stats), you must prefix the variable with the `stimunit` label from `run_trial.py`. For example, to access `hit` for a `stimunit` labeled "target", use `target_hit`.

Breakdown:

Stage 0: Plan
* Read literature and figure out what a typical {target_task} task looks like.
* Define the flow: blocks → trials → events.
* Identify stimulus types (ensuring sizes are in 'deg'), response keys, timing parameters, and key output fields.

Stage 1: config.yaml
* Adapt the existing config.yaml to run a {target_task} task.
* Ensure all stimulus sizes are defined in 'deg' and are of an appropriate size for a typical screen.
* Highlight any parameters that need careful review.

Stage 2: Trial logic (src/run_trial.py)
* Adapt one existing trial template to run a single {target_task} trial.
* (Optional) If needed, add helpers in src/utils.py; otherwise skip.

Stage 3: Block/session logic (main.py)
* Implement block order, feedback screens, and pauses based on the template task.
* Keep the public API consistent with the original task.
* Ensure that when accessing recorded variables to a specific stimunit, the correct `stimunit` prefix is used (e.g., `target_hit`).

Stage 4: Asset handling
* Identify and list for removal all `_voice.mp3` files from the `assets/` directory.
* Identify and list for removal any other files in `assets/` not relevant to the new {target_task}.

Stage 5: README.md
* Match the structure and tone of existing tasks.
* Cover: purpose, install steps, config details, run instructions, and expected outputs.

Stage 6: Static validation
* Check for correct chainable syntax (e.g., using `\\` for new lines).
* Check that `src/__init__.py` is properly defined.
* Cross-reference `config.yaml` with `main.py`, `run_trial.py`, and `utils.py` (if it exists) to ensure all stimuli, variables, durations, and triggers are defined and used consistently.
* Check that config.yaml keys line up with code references.
* Ensure logged DataFrame columns match the template task.
* Verify naming, docstrings, and imports follow PsyFlow conventions.
* Spot any logic errors or unused variables.

(No PsychoPy runtime or unit tests are required during this step)

