import subprocess
import os

def run_gradle_build(project_dir):
    """
    Runs './gradlew assembleDebug' in the specified project directory.
    
    Returns:
        (bool, str): A tuple containing a boolean for success/failure
                     and the relevant output (stdout for success, stderr for failure).
    """
    print("🛠️  Attempting to build the APK with Gradle...")
    gradlew_path = os.path.join(project_dir, "gradlew")

    if not os.path.exists(gradlew_path):
        error_message = f"❌ Error: gradlew wrapper not found at '{gradlew_path}'."
        print(error_message)
        return False, error_message

    os.chmod(gradlew_path, 0o755)

    try:
        # Stop any daemons to ensure a fresh start
        subprocess.run(["./gradlew", "--stop"], cwd=project_dir, capture_output=True, text=True)

        # Run the standard build command.
        process = subprocess.run(
            ["./gradlew", "assembleDebug"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Build successful!")
        return True, process.stdout
    except subprocess.CalledProcessError as e:
        # On failure, return False and the standard error output.
        print("❌ Build failed!")
        return False, e.stderr

