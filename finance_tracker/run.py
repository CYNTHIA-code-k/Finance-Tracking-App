from app import create_app

app = create_app('development')  # Create app instance with 'development' configuration

if __name__ == '__main__':
    app.run(debug=True)  # Run the app with debugging enabled
