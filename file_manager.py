import os
import re
import shutil

def copy_template(template_dir, project_name):
    """Copies the template project to the destination directory."""
    print(f"📁 Copying template from '{template_dir}' to '{project_name}'...")
    if os.path.exists(project_name):
        shutil.rmtree(project_name)
    
    try:
        shutil.copytree(template_dir, project_name)
        print("  ✅ Template copied successfully.")
    except FileNotFoundError:
        print(f"❌ Error: Template directory '{template_dir}' not found.")
        return False
    return True

def save_static_file(project_name, file_path, content):
    """Saves a file with static content directly to the project."""
    print(f"✍️  Writing static file: {file_path}")
    full_path = os.path.join(project_name, file_path.strip())
    dir_name = os.path.dirname(full_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    with open(full_path, "w") as f:
        f.write(content)
    print(f"  ✅ Wrote: {full_path}")


def save_files_from_ai(generated_code, project_name, expected_file_path):
    """
    Parses the AI-generated code and saves the file.
    This function is resilient and can handle responses that don't perfectly
    match the requested format.
    """
    print(f"🤖 Writing AI-generated file to '{expected_file_path}'...")
    
    # First, try to find the perfect format: ```FILE: path/to/file.kt ... ```
    file_pattern = re.compile(r"```.*?FILE: (.*?)\s*\n(.*?)\n```", re.DOTALL)
    files = file_pattern.findall(generated_code)

    if files:
        # AI behaved perfectly.
        for file_path, file_content in files:
            full_path = os.path.join(project_name, file_path.strip())
            dir_name = os.path.dirname(full_path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            
            with open(full_path, "w") as f:
                f.write(file_content.strip())
            print(f"  ✅ Wrote (strict format): {full_path}")
        return

    # If the perfect format isn't found, look for a raw Kotlin code block.
    # This handles cases where the AI is "chatty" but still provides the code.
    code_block_pattern = re.compile(r"```(?:kotlin)?\s*\n(.*?)\n```", re.DOTALL)
    match = code_block_pattern.search(generated_code)
    if match:
        file_content = match.group(1).strip()
        full_path = os.path.join(project_name, expected_file_path.strip())
        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        with open(full_path, "w") as f:
            f.write(file_content)
        print(f"  ✅ Wrote (fallback format): {full_path}")
        return

    # If no format is found, log it for debugging.
    print("⚠️ No files or code blocks were found in the AI's response.")
    with open(os.path.join(project_name, "ai_raw_response.txt"), "w") as f:
        f.write(generated_code)

