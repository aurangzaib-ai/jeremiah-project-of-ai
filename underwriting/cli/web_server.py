"""
Web server command-line interface for the underwriting system.
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from underwriting.web.app import create_app


def main():
    """Main entry point for the web server CLI."""
    
    parser = argparse.ArgumentParser(
        description="Start the Automobile Insurance Underwriting Web Server"
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind to (default: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Enable auto-reload on file changes'
    )
    
    args = parser.parse_args()
    
    # Set environment variables
    if args.debug:
        os.environ['FLASK_DEBUG'] = 'true'
    
    # Create Flask app
    app = create_app()
    
    print(f"Starting Automobile Insurance Underwriting Web Server...")
    print(f"Server will be available at: http://{args.host}:{args.port}")
    print(f"Debug mode: {'Enabled' if args.debug else 'Disabled'}")
    print(f"Auto-reload: {'Enabled' if args.reload else 'Disabled'}")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Start the Flask development server
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            use_reloader=args.reload,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

