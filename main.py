import subprocess
import threading
import os

def run_app():
    # Mendapatkan jalur lengkap ke berkas Beranda_🏠_.py di dalam folder 'app'
    app_path = os.path.join('app', 'Beranda_🏠_.py')
    subprocess.Popen(['streamlit', 'run', app_path])

if __name__ == '__main__':
    # Memulai aplikasi dalam thread baru
    streamlit_thread = threading.Thread(target=run_app)
    streamlit_thread.start()
