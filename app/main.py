import subprocess
import sys
import os

def main():
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Start FastAPI server (uvicorn) - app.backend.api.main:app
    fastapi_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.backend.api.main:app",
        "--reload", "--host", "0.0.0.0", "--port", "8000"
    ])

    # Start Streamlit frontend (app.frontend.main)
    streamlit_proc = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "app/frontend/main.py"
    ])

    try:
        fastapi_proc.wait()
        streamlit_proc.wait()
    except KeyboardInterrupt:
        print("Shutting down both servers...")
        fastapi_proc.terminate()
        streamlit_proc.terminate()

if __name__ == "__main__":
    main()
