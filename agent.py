import json
from gemini_client import get_gemini_client, generate_code
from file_manager import copy_template, save_static_file, save_files_from_ai
from gradle_runner import run_gradle_build

def create_android_app(blueprint_path):
    """
    Main orchestration logic for the Droidscribe agent.
    Reads a JSON blueprint and generates an app from it.
    """
    try:
        with open(blueprint_path, 'r') as f:
            blueprint = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Blueprint file not found at '{blueprint_path}'")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Blueprint file '{blueprint_path}' is not valid JSON.")
        return

    project_name = "GeneratedApp"
    template_dir = "template"

    # 1. Copy the base project template
    if not copy_template(template_dir, project_name):
        return

    # 2. Process the files specified in the blueprint
    print("⚙️  Processing blueprint...")
    for file_spec in blueprint.get("filesToGenerate", []):
        file_path = file_spec.get("path")
        file_type = file_spec.get("type")

        if not file_path or not file_type:
            continue

        if file_type == "StaticContent":
            content = file_spec.get("content", "")
            save_static_file(project_name, file_path, content)

        elif file_type == "ComposeScreen":
            spec = file_spec.get("spec", {})
            imports = file_spec.get("imports", [])
            
            # Format the imports for the prompt
            import_statements = "\\n".join([f"import {imp}" for imp in imports])

            prompt = f"""You are a code generation engine. You only respond with code.
Your entire response will be a single code block for the specified file path.
Do not include any other text, conversation, or markdown formatting.

Generate the Kotlin code for the file at path `{file_path}`.

**CRITICAL INSTRUCTIONS:**
- The package name MUST be `{blueprint.get("packageName", "com.example.generatedapp")}`.
- You MUST include the following import statements:
{import_statements}
- Implement the logic based on this JSON specification:
```json
{json.dumps(spec, indent=2)}
```
"""
            model = get_gemini_client()
            generated_code = generate_code(model, prompt)
            if generated_code:
                save_files_from_ai(generated_code, project_name, file_path)

    # 3. Run the Gradle build
    success, output = run_gradle_build(project_name)
    
    if success:
        print("\n🎉 Droidscribe finished successfully! Your app is ready.")
    else:
        print("\nDroidscribe encountered errors. See build output above.")

