import sqlite3
import os

DATABASE_PATH = 'central_rss_articles.db'
HTML_OUTPUT_PATH = 'crypto_news.html'

def fetch_data():
    """Fetches data from the discord_queue table."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    # Fetch data sorted by publication_date in descending order
    cursor.execute('SELECT title, link, description, publication_date, content_url FROM discord_queue ORDER BY publication_date DESC')
    data = cursor.fetchall()
    conn.close()
    return data

def generate_html(data):
    """Generates an HTML page from the data."""
    html_content = '''
    <html>
    <head>
        <title>Crypto News</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background-color: #121212; 
                color: #e0e0e0; 
            }
            .article-block { 
                margin-bottom: 20px; 
                padding: 10px; 
                border: 1px solid #333; 
                border-radius: 5px; 
                background-color: #1e1e1e;
            }
            .article-image { 
                max-width: 150px; 
                height: auto; 
                display: block; 
                margin-bottom: 10px; 
            }
            .article-title { 
                font-size: 20px; 
                font-weight: bold; 
                margin: 0; 
            }
            .article-description { margin-top: 5px; }
            .article-title a { 
                text-decoration: none; 
                color: #4f9d69; 
            }
            .article-title a:hover { 
                text-decoration: underline; 
            }
        </style>
    </head>
    <body>
        <h1>Crypto News</h1>
    '''

    for title, link, description, pub_date, content_url in data:
        html_content += f'''
            <div class="article-block">
                <div class="article-title"><a href="{link}">{title}</a></div>
                <img src="{content_url}" class="article-image" alt="{title}">
                <div class="article-description">{description}</div>
                <div>Published on: {pub_date}</div>
            </div>
        '''

    html_content += '''
    </body>
    </html>
    '''

    with open(HTML_OUTPUT_PATH, 'w') as file:
        file.write(html_content)

def main():
    data = fetch_data()
    generate_html(data)

if __name__ == '__main__':
    main()
