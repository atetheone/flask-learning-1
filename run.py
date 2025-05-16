"""
Main entry point for the social media API application.
This module runs the Flask application.
"""

import os
from dotenv import load_dotenv
from src import create_app


# Load environment variables from .env file
load_dotenv()

# Get the environment from environment variables or default to development
env = os.environ.get('FLASK_ENV', 'development')

# Create the Flask application with the specified environment
app = create_app(env)

if __name__ == '__main__':
    """
    Run the Flask application when this script is executed directly.
    """
    # Get the port from environment variables or default to 5000
    port = int(os.environ.get('PORT', 5000))

    # Run the application
    app.run(host='0.0.0.0', port=port)

