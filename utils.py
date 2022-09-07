import requests

def get_html(url):
    """
    function for get html structures
    """
    response = requests.get(url)
    return response.text