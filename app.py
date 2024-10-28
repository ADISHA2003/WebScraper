from flask import Flask, request, render_template, jsonify, send_file
from scraper import scrape_website
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required!'}), 400

    try:
        scraped_data = scrape_website(url)

        # Prepare data for DataFrame
        data_for_df = {
            'url': [scraped_data['url']],
            'title': [scraped_data['title']],
            'html': [scraped_data['html']],
            'text': [scraped_data['text']]
        }

        # Paths for saving data
        json_path = 'scraped_data.json'
        excel_path = 'scraped_data.xlsx'
        csv_path = 'scraped_data.csv'

        # Create DataFrame from the structured data
        df = pd.DataFrame(data_for_df)

        # Save to Excel
        df.to_excel(excel_path, index=False)

        # Save to CSV
        df.to_csv(csv_path, index=False)

        # Save HTML to JSON format for download with UTF-8 encoding
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(scraped_data['html'])

        return jsonify({'data': scraped_data, 'message': 'Scraping completed!'})

    except Exception as e:
        # Return a more descriptive error message
        return jsonify({'error': f'Scraping failed: {str(e)}'}), 500

@app.route('/download/<file_type>')
def download(file_type):
    if file_type == 'json':
        return send_file('scraped_data.json', as_attachment=True)
    elif file_type == 'excel':
        return send_file('scraped_data.xlsx', as_attachment=True)
    elif file_type == 'csv':
        return send_file('scraped_data.csv', as_attachment=True)
    else:
        return jsonify({'error': 'Invalid file type requested!'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))