import json
import os
from logger import Logger
from gemini_client import get_gemini_client, generate_code
from file_manager import copy_template, save_files_from_ai
from gradle_runner import run_gradle_build

def _classify_error(error_log):
    """
    Analyzes a Gradle error log to classify it.
    """
    code_error_keywords = ["Unresolved reference", "compilation error", "e: file:///", "Syntax error"]
    env_error_keywords = ["corrupted", "SDK", "Could not determine java version", "Plugin not found", "Failed to apply plugin", "Could not resolve all files"]

    for keyword in env_error_keywords:
        if keyword in error_log:
            return "ENVIRONMENT_ERROR"
    for keyword in code_error_keywords:
        if keyword in error_log:
            return "CODE_ERROR"
    return "CODE_ERROR"

def create_android_app(blueprint_path):
    """
    Main orchestration logic for the Droidscribe agent.
    Features a multi-attempt loop to generate, build, and debug code.
    """
    logger = Logger()
    logger.log("--- Droidscribe Agent Run: Started ---")
    
    try:
        with open(blueprint_path, 'r') as f:
            original_blueprint = json.load(f)
        logger.log(f"Successfully loaded blueprint: {blueprint_path}")
    except Exception as e:
        logger.log(f"❌ CRITICAL ERROR: Failed to load blueprint file. {e}")
        return

    project_name = "GeneratedApp"
    template_dir = "template"
    max_retries = 3
    last_error = ""
    last_code = ""

    for attempt in range(1, max_retries + 1):
        logger.log(f"\n--- Attempt {attempt}/{max_retries} ---")

        if attempt == 1:
            if not copy_template(template_dir, project_name):
                logger.log("❌ CRITICAL ERROR: Failed to copy template.")
                return

        prompt = ""
        if attempt == 1:
            logger.log("Strategy: Initial implementation from blueprint.")
            spec = original_blueprint.get("spec", {})
            prompt = f"""You are a code-generation machine. Your entire response must be ONLY the code block for the requested file.
            
            Generate the Kotlin code for the file `app/src/main/java/com/example/generatedapp/MainActivity.kt` based on this JSON specification:
            ```json
            {json.dumps(spec, indent=2)}
            ```
            """
        else:
            logger.log("Strategy: Attempting to fix the previous build error with added context.")
            
            # Read the content of the Theme file to provide context to the AI
            theme_file_path = os.path.join(template_dir, "app/src/main/java/com/example/generatedapp/ui/theme/Theme.kt")
            try:
                with open(theme_file_path, 'r') as f:
                    theme_code_context = f.read()
            except FileNotFoundError:
                theme_code_context = "/* Theme.kt not found */"

            prompt = f"""You are a senior developer debugging a build failure.
            The previous code you generated failed to compile because of an unresolved reference.
            Analyze the failed code, the build error, and the provided context from other relevant files.
            Then, provide a corrected, complete version of the `MainActivity.kt` file.
            Your entire response must be ONLY the corrected code block for the file.
            
            CONTEXT FROM `Theme.kt`:
            ```kotlin
            {theme_code_context}
            ```

            FAILED CODE (`MainActivity.kt`):
            ```kotlin
            {last_code}
            ```

            BUILD ERROR:
            ```
            {last_error}
            ```
            """
        
        logger.log_section(f"Attempt {attempt} - Prompt to Gemini", prompt)
        model = get_gemini_client()
        generated_code = generate_code(model, prompt)
        
        if not generated_code:
            logger.log("❌ AI failed to generate code for this attempt. Ending run.")
            return
            
        logger.log_section(f"Attempt {attempt} - AI Response", generated_code)
        
        save_files_from_ai(generated_code, project_name, "app/src/main/java/com/example/generatedapp/MainActivity.kt")
        
        try:
            with open(os.path.join(project_name, "app/src/main/java/com/example/generatedapp/MainActivity.kt"), 'r') as f:
                last_code = f.read()
        except FileNotFoundError:
            logger.log("⚠️ Could not read back the generated MainActivity.kt for the next loop.")
            last_code = ""

        success, output = run_gradle_build(project_name)
        logger.log_section(f"Attempt {attempt} - Build Output", output)

        if success:
            logger.log("✅ BUILD SUCCESSFUL! The agent has completed its task.")
            print("\n🎉 Droidscribe finished successfully! Your app is ready.")
            return
        else:
            logger.log(f"❌ Build failed on attempt {attempt}.")
            last_error = output
            
            error_type = _classify_error(last_error)
            logger.log(f"Error classified as: {error_type}")
            
            if error_type == "ENVIRONMENT_ERROR":
                logger.log("Stopping run because this is an environment issue that the AI cannot fix.")
                print("\nDroidscribe stopped: The build failed due to an environment or configuration error.")
                return

    logger.log(f"--- Droidscribe Agent Run: FAILED ---")
    logger.log(f"Agent failed to produce a working build after {max_retries} attempts.")
    print("\nDroidscribe encountered errors and could not fix them. Check logs for details.")

