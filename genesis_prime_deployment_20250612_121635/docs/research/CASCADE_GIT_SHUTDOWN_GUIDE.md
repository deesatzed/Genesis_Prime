# Guide: Setting Up an Efficient Shutdown/Restart Workflow with Cascade and Git

This guide explains how to set up and use a streamlined, semi-automated procedure for shutting down and restarting your development environment using Git for version control and Cascade for task execution.

## Why Use This Workflow?

Combining Git and Cascade for shutdown/restart offers several advantages over manual backups or ad-hoc processes:

*   **Reliability & History (Git):** Instead of manually copying files (which is error-prone), Git creates precise, timestamped snapshots (commits) of your entire project. You can easily view history (`git log`), compare versions, and revert to previous states if needed.
*   **Consistency:** The documented procedure ensures the same steps are followed every time, reducing the risk of forgetting something important (like stopping a service or saving a file).
*   **Efficiency (Cascade):** Cascade automates the command-line tasks (stopping Docker containers, Git commands), saving you time and reducing repetitive typing.
*   **Clear Context on Restart:** Using `git log` provides immediate context about the exact state you left the project in, making it faster to resume work.
*   **Best Practices:** Using version control (Git) is a standard best practice in software development.

## One-Time Setup (Per Project)

To add this workflow to a new or existing project:

1.  **Navigate** to your project's root directory in your terminal.
2.  **Tell Cascade:** Simply ask Cascade to set it up for you by saying:
    > "Cascade, build our SHUTDOWN_RESTART_PROCEDURE.md for this project."
3.  **Cascade Actions:** Cascade will automatically:
    *   Initialize a Git repository (`git init`) if one doesn't exist.
    *   Create a standard `.gitignore` file if one doesn't exist (crucial for preventing unwanted files like `.env` or virtual environments from being committed).
    *   Create or update the `SHUTDOWN_RESTART_PROCEDURE.md` file with the detailed Git-based steps.
    *   Add a reference to this procedure in your main `README.md` file (creating a basic README if needed).
    *   Commit these setup files (`.gitignore`, `SHUTDOWN_RESTART_PROCEDURE.md`, `README.md`) to Git.

Once Cascade confirms completion, the procedure is ready to use for that project.

## Using the Workflow

### Initiating Shutdown

1.  **You:** Tell Cascade, "I need to restart."
2.  **Cascade:** Will remind you to stop running servers.
3.  **You:** Manually stop any running application servers (e.g., Uvicorn, Node) using `Ctrl+C` in their respective terminals.
4.  **You:** Tell Cascade, "Servers are stopped."
5.  **Cascade:** Automatically performs the shutdown commands:
    *   Stops relevant Docker containers (if configured in the procedure, e.g., `docker stop <container_name>`).
    *   Stages all current changes (`git add .`).
    *   Commits the changes (`git commit -m "WIP: Saving progress before shutdown"` or similar).
    *   Confirms completion.
6.  **You:** Safely shut down or restart your system.

### After Restart

1.  **You:** Navigate to the project directory in your terminal.
2.  **You:** Tell Cascade, "I've restarted, let's resume based on the procedure."
3.  **Cascade:** Will remind you to activate your virtual environment.
4.  **You:** Manually activate your project's virtual environment (e.g., `source .venv/bin/activate` or `conda activate myenv`).
5.  **You:** Tell Cascade, "Environment is active."
6.  **Cascade:** Automatically performs the startup commands:
    *   Starts relevant Docker containers (if configured, e.g., `docker start <container_name>`).
    *   Shows the last commit message (`git log -1`) for context.
    *   Shows the current working directory status (`git status`) to confirm cleanliness.
    *   Confirms completion.
7.  **You:** Manually start your application servers (e.g., Uvicorn, Node) as needed, using commands likely documented in your project's `SETUP_AND_TESTING.md` or `README.md`.

By following this process, you ensure your work is safely saved and you can efficiently resume development with clear context after any interruption.
