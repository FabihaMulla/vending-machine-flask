"""
Application Entry Point
Runs the Flask development server
"""

from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 VENDING MACHINE - MEALY MACHINE IMPLEMENTATION")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("API endpoints available at http://localhost:5000/api")
    print("=" * 60)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
