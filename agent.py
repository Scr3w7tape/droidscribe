from gemini_client import get_gemini_client, generate_code
from file_manager import copy_template, save_files_from_ai
from gradle_runner import run_gradle_build

def create_android_app(prompt):
    """
    Main orchestration logic for the Droidscribe agent using a template.
    """
    project_name = "GeneratedApp"
    template_dir = "template"

    # 1. Copy the base project template
    if not copy_template(template_dir, project_name):
        return

    # 2. Construct a more focused prompt for the AI
    detailed_prompt = f"""
You are Droidscribe, an expert Android developer.
A user wants an app with the following description: "{prompt}".

Your task is to generate ONLY the necessary Kotlin source code and Gradle build files to bring this app to life.
A project structure with a working Gradle wrapper already exists. You only need to provide the content for the following files.

**Output Format:**
You MUST generate the content for each file, enclosed in a code block with the file path specified after the opening backticks. For example: ```FILE: path/to/your/file.kt ... ```

**Files to Generate:**
- `build.gradle.kts` (Root level)
- `settings.gradle.kts`
- `app/build.gradle.kts`
- `app/src/main/AndroidManifest.xml`
- `app/src/main/java/com/example/generatedapp/MainActivity.kt`
- `app/src/main/java/com/example/generatedapp/ui/theme/Theme.kt`
- `app/src/main/java/com/example/generatedapp/ui/theme/Color.kt`
- `app/src/main/java/com/example/generatedapp/ui/theme/Type.kt`

Ensure the code is modern, uses Jetpack Compose, and is fully functional.
    """
    
    # 3. Get Gemini client and generate the code
    model = get_gemini_client()
    generated_code = generate_code(model, detailed_prompt)
    if not generated_code:
        print("Stopping due to code generation failure.")
        return

    # 4. Save the AI-generated files over the template placeholders
    save_files_from_ai(generated_code, project_name)
    
    # 5. Run the Gradle build
    success, output = run_gradle_build(project_name)
    
    if success:
        print("\n🎉 Droidscribe finished successfully! Your app is ready.")
    else:
        print("\n🔥 Droidscribe encountered errors. See build output above.")


