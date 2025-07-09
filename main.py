import sys
from agent import create_android_app

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<your app description>\"")
        sys.exit(1)
        
    prompt = sys.argv[1]
    create_android_app(prompt)
