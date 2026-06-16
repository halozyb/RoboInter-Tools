"""
RoboInter-Tools Launcher
========================
Drop MP4 files next to the EXE, double-click to start annotating.

This script:
1. Auto-detects MP4 files in the working directory
2. Generates annotation pool JSON files
3. Starts the Flask annotation server (background thread)
4. Launches the PyQt5 annotation client (auto-connected to localhost)
"""

import sys
import os
import json
import threading
import time
import argparse


def get_base_dir():
    """Resolve the base directory (where the EXE or script lives)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def ensure_dirs(base):
    """Create required directory structure."""
    for d in ['video', 'human_anno_lang', 'user_config/lang']:
        os.makedirs(os.path.join(base, d), exist_ok=True)


def find_mp4_files(base):
    """Find all MP4 files under the base directory."""
    mp4_files = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ('human_anno_lang', 'user_config')]
        for f in files:
            if f.lower().endswith('.mp4'):
                mp4_files.append(os.path.join(root, f))
    return sorted(mp4_files)


def generate_pool(base, mp4_files):
    """Generate annotation pool JSON files for the language annotation server."""
    users = ['local']
    no_annotation = {u: {} for u in users}
    has_annotation = {u: {} for u in users}

    for idx, mp4_path in enumerate(mp4_files):
        video_name = os.path.splitext(os.path.basename(mp4_path))[0]
        user = users[idx % len(users)]
        no_annotation[user][mp4_path] = {
            'anno_path': '',
            'save_path': os.path.join(base, 'human_anno_lang', f'{video_name}.npz'),
        }

    with open(os.path.join(base, 'no_annotation_lang.json'), 'w') as f:
        json.dump(no_annotation, f, indent=2)
    with open(os.path.join(base, 'has_annotation_lang.json'), 'w') as f:
        json.dump(has_annotation, f, indent=2)
    with open(os.path.join(base, 'user_list.txt'), 'w') as f:
        f.write('local\n')


def start_server(base, port):
    """Start the Flask annotation server in a daemon thread."""
    sys.path.insert(0, base)

    # Build in-memory server config pointing to base directory
    import server.server as srv
    srv.CONFIG = {'server': {
        'root_dir': base,
        'no_annotation_lang': 'no_annotation_lang.json',
        'has_annotation_lang': 'has_annotation_lang.json',
        'user_list_file': 'user_list.txt',
        'user_history_dir': 'user_config',
        'save_path_lang_temp': 'human_anno_lang/{video_name}.npz',
        'video_dir': 'video',
        'error_log': 'user_config/error_video.txt',
    }}
    srv.ROOT_DIR = base
    srv.PATHS = {
        'no_annotation_lang': os.path.join(base, 'no_annotation_lang.json'),
        'has_annotation_lang': os.path.join(base, 'has_annotation_lang.json'),
        'user_list_file': os.path.join(base, 'user_list.txt'),
        'user_history_dir': os.path.join(base, 'user_config'),
    }

    def run():
        srv.app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)

    t = threading.Thread(target=run, daemon=True)
    t.start()
    time.sleep(1)  # Give server time to start
    return t


def run_client():
    """Run the PyQt5 client (auto-connects to localhost via env vars)."""
    from client.client import QApplication, sys as client_sys, VideoPlayer
    import argparse as ap

    app = QApplication(sys.argv)
    app.setApplicationName('RoboInter-Tools')

    parser = ap.ArgumentParser()
    parser.add_argument('--out_file', type=str, default='./annotation.pkl')
    parser.add_argument('--sam_anno', type=str, default='./sam_anno.pkl')
    parser.add_argument('--lang_anno', type=str, default='./lang_anno.pkl')
    args = parser.parse_args([])

    player = VideoPlayer(args)
    player.resize(1100, 600)
    player.show()
    sys.exit(app.exec_())


def main():
    parser = argparse.ArgumentParser(description='RoboInter-Tools Launcher')
    parser.add_argument('--port', type=int, default=10086, help='Server port')
    args = parser.parse_args()

    base = get_base_dir()
    os.chdir(base)

    # Set environment variables so client auto-connects to localhost
    os.environ['ROBINTER_IP'] = '127.0.0.1'
    os.environ['ROBINTER_PORT'] = str(args.port)
    os.environ['ROBINTER_USERNAME'] = 'local'

    print('=' * 50)
    print('  RoboInter-Tools')
    print('=' * 50)
    print(f'  Working dir: {base}')

    # 1. Ensure directories
    ensure_dirs(base)

    # 2. Find MP4 files
    mp4_files = find_mp4_files(base)
    if not mp4_files:
        print()
        print('  [!] No MP4 files found!')
        print(f'  Place .mp4 files in: {base}')
        print()
        input('  Press Enter to exit...')
        sys.exit(1)

    print(f'  Found {len(mp4_files)} MP4 file(s):')
    for f in mp4_files:
        print(f'    - {os.path.relpath(f, base)}')

    # 3. Generate annotation pool
    generate_pool(base, mp4_files)
    print('  Annotation pool ready')

    # 4. Start server
    print(f'  Starting server on 127.0.0.1:{args.port} ...')
    start_server(base, args.port)
    print('  Server running')

    # 5. Launch client
    print('  Launching annotation client...')
    print('=' * 50)
    run_client()


if __name__ == '__main__':
    main()
