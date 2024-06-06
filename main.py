import subprocess
import threading

def run_app():
    subprocess.run(['python', 'app.py'], cwd='authenticator')  # Menentukan jalur kerja ke folder 'authenticator'

if __name__ == '__main__':
    # Memulai aplikasi dalam thread baru
    streamlit_thread = threading.Thread(target=run_app)
    streamlit_thread.start()
