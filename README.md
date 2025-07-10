🤖 Droidscribe: The Spec-Driven AI App Agent
Droidscribe is a Python-based AI agent that generates complete, ready-to-build Android applications by interpreting a formal technical specification, or "Agent Blueprint."

It uses a reliable, template-based approach to create a full Android Studio project structure. It then populates this project with a combination of static boilerplate code and AI-generated code based on the instructions in a structured JSON blueprint. The agent can automatically trigger a Gradle build to compile the generated code into an APK, providing an end-to-end solution for spec-driven Android development.

🏛️ Architecture: The "Agent Blueprint" Model
Droidscribe operates on a spec-driven model. Instead of relying on ambiguous natural language prompts, the agent builds an application based on a precise technical document. This significantly increases the reliability and consistency of the generated code.

We use a two-document approach for each app blueprint:

The Human Blueprint (.md): A detailed, human-readable Markdown file that serves as the project's technical design document. It's meant for collaboration, documentation, and high-level planning.

The AI Blueprint (.json): A highly structured JSON file that contains the exact, unambiguous instructions for the agent. It defines which files are static, which require AI generation, and the precise specification for the AI to follow. This is the file the agent actually executes.

⚙️ Installation and Setup
This project is designed to run in a WSL (Windows Subsystem for Linux) or a native Linux environment.

Clone the Repository:

git clone https://github.com/Scr3w7tape/droidscribe.git
cd droidscribe

Run the Automated Setup Script:
This script will install all system dependencies and create the project files.

chmod +x setup.sh
./setup.sh

Complete Manual Steps:
The script will prompt you to complete the final manual steps, which involve configuring your Gemini API key and your Android SDK path.

🚀 How to Run
Once the setup is complete and you have activated the Python virtual environment (source venv/bin/activate), you can run the agent by passing it the path to an AI Blueprint file.

python main.py "path/to/your/blueprint.json"

Example:

python main.py blueprints/dice_roller.json

The agent will then:

Copy the base project template to a new GeneratedApp/ directory.

Read and process the JSON blueprint.

Write the static files and generate the dynamic code via the Gemini API.

Attempt to build the APK using Gradle.
