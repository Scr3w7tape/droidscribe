import subprocess
import os

def run_gradle_build(project_dir):
    """
    Runs './gradlew assembleDebug' in the specified project directory.
    """
    print("🛠️  Attempting to build the APK with Gradle...")
    gradlew_path = os.path.join(project_dir, "gradlew")

    # This check correctly verifies the script exists before we try to run it.
    if not os.path.exists(gradlew_path):
        print(f"❌ Error: gradlew wrapper not found at '{gradlew_path}'.")
        return False, "Gradle wrapper not found."

    # Make gradlew executable
    os.chmod(gradlew_path, 0o755)

    try:
        # The fix is here: We now call './gradlew' relative to the project_dir,
        # which is set as the current working directory (cwd).
        process = subprocess.run(
            ["./gradlew", "assembleDebug"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Build successful!")
        print(process.stdout)
        return True, process.stdout
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print(e.stderr)
        return False, e.stderr

