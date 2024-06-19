import subprocess
import threading

def run_app():
    subprocess.run(['streamlit', 'run', 'app/Beranda_🏠_.py'])

if __name__ == '__main__':
    # Memulai aplikasi dalam thread baru
    streamlit_thread = threading.Thread(target=run_app)
    streamlit_thread.start()
