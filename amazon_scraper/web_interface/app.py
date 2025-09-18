from flask import Flask, render_template, jsonify
import os
from storage.file_handler import FileHandler

app = Flask(__name__)

@app.route('/')
def index():
    """Display scraped data in web interface"""
    data = FileHandler.load_results()
    if not data:
        return "No data available. Please run the scraper first."
    
    return render_template('results.html', data=data)

@app.route('/api/data')
def api_data():
    """API endpoint to get scraped data as JSON"""
    data = FileHandler.load_results()
    if not data:
        return jsonify({'error': 'No data available'}), 404
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)
