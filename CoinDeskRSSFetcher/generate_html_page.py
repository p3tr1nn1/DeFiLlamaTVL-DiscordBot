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
                margin: 0 0 10px 0; 
            }
            .article-description { 
                font-size: 14px; 
                color: #c0c0c0; 
                margin-bottom: 10px; 
            }
            .publication-date {
                font-size: 12px; 
                color: #a0a0a0; 
                margin-top: 10px; 
                border-top: 1px solid #333; 
                padding-top: 10px; 
            }
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
                <div class="publication-date">Published on: {pub_date}</div>
            </div>
        '''

    html_content += '''
    </body>
    </html>
    '''

    with open(HTML_OUTPUT_PATH, 'w') as file:
        file.write(html_content)
