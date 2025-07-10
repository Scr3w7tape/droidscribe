import sys
from agent import create_android_app

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_blueprint.json>")
        sys.exit(1)
        
    blueprint_path = sys.argv[1]
    create_android_app(blueprint_path)

