import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Set environment variables for Vercel
os.environ['FLASK_ENV'] = 'production'
os.environ['SERVERLESS'] = 'true'

try:
    # Disable heavy ML imports for serverless
    import warnings
    warnings.filterwarnings("ignore")
    
    # Mock problematic modules for serverless environment
    class MockModule:
        def __getattr__(self, name):
            return lambda *args, **kwargs: None
    
    # Pre-emptively mock heavy modules
    sys.modules['spacy'] = MockModule()
    sys.modules['nltk'] = MockModule()
    sys.modules['sentence_transformers'] = MockModule()
    
    # Import Flask app
    from backend.app import create_app
    
    # Create app instance for serverless
    app = create_app()
    
    # Vercel expects the Flask app to be named 'app'
    # This will be the WSGI application
    
except Exception as e:
    # Fallback minimal app for debugging
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/api')
    @app.route('/api/')
    def hello():
        return jsonify({
            'message': 'Prime Minister Internship Portal API',
            'error': f'Startup error: {str(e)}',
            'status': 'partial'
        })
    
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'OK',
            'message': 'API is running (fallback mode)',
            'environment': 'production'
        })

# For direct execution (local testing)
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))