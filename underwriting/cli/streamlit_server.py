"""
Streamlit server command-line interface.

This module provides CLI commands for starting and managing
the Streamlit web application.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

def add_streamlit_parser(subparsers):
    """Add Streamlit subcommand parser."""
    streamlit_parser = subparsers.add_parser(
        'streamlit',
        help='Start Streamlit web application'
    )
    
    streamlit_parser.add_argument(
        '--port',
        type=int,
        default=8501,
        help='Port to run Streamlit server on (default: 8501)'
    )
    
    streamlit_parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Host to bind Streamlit server to (default: localhost)'
    )
    
    streamlit_parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode with auto-reload'
    )
    
    streamlit_parser.add_argument(
        '--browser',
        action='store_true',
        default=True,
        help='Automatically open browser (default: True)'
    )
    
    streamlit_parser.add_argument(
        '--no-browser',
        action='store_true',
        help='Do not automatically open browser'
    )
    
    return streamlit_parser

def main(args):
    """Main function for Streamlit CLI."""
    try:
        # Get the current working directory (should be project root)
        project_root = Path.cwd()
        streamlit_app_path = project_root / "underwriting" / "streamlit" / "app.py"
        
        # Ensure the Streamlit app exists
        if not streamlit_app_path.exists():
            print(f"❌ Error: Streamlit app not found at {streamlit_app_path}")
            return 1
        
        # Set up environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root)
        
        # Build Streamlit command
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            str(streamlit_app_path),
            '--server.port', str(args.port),
            '--server.address', args.host
        ]
        
        # Add browser options
        #if args.no_browser:
        #    cmd.extend(['--server.headless', 'true'])
        #elif not args.browser:
        #    cmd.extend(['--server.headless', 'true'])
        
        # Add debug options
        if args.debug:
            cmd.extend(['--server.runOnSave', 'true'])
            cmd.extend(['--server.fileWatcherType', 'auto'])
        
        print(f"🚀 Starting Streamlit Underwriting Application...")
        print(f"📍 Server will be available at: http://{args.host}:{args.port}")
        print(f"🔧 Debug mode: {'Enabled' if args.debug else 'Disabled'}")
        print(f"🌐 Auto-open browser: {'No' if args.no_browser else 'Yes'}")
        print()
        print("💡 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start Streamlit server
        result = subprocess.run(cmd, env=env, cwd=project_root)
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n🛑 Streamlit server stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting Streamlit server: {str(e)}")
        return 1

if __name__ == "__main__":
    # For testing the module directly
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    add_streamlit_parser(subparsers)
    
    args = parser.parse_args(['streamlit', '--debug'])
    sys.exit(main(args))

