import subprocess
import os

def run_gradle_build(project_dir):
    """
    Runs './gradlew assembleDebug' in the specified project directory.
    """
    print("🛠️  Attempting to build the APK with Gradle...")
    gradlew_path = os.path.join(project_dir, "gradlew")

    if not os.path.exists(gradlew_path):
        print(f"❌ Error: gradlew wrapper not found at '{gradlew_path}'.")
        return False, "Gradle wrapper not found."

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
        print(process.stdout)
        return True, process.stdout
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print(e.stderr)
        return False, e.stderr

