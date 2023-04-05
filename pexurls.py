import os
import re
import sys
import requests
from bs4 import BeautifulSoup
pexurls_file = "someurls.txt"
default_starting_point = 11500
default_ending_point = 90218
if len(sys.argv) > 0+1:
    start = int(sys.argv[1])
else:
    start = default_starting_point
if len(sys.argv) > 1+1:
    end = int(sys.argv[2])
else:
    end = default_ending_point
print("STARTING")
# Make a GET request to the webpage

def remove_url_hash(url):
    """
    Removes any hash string at the end of a URL using regex.

    Args:
        url (str): The URL to modify.

    Returns:
        str: The modified URL with any hash string removed.
    """
    return re.sub(r'#.*$', '', url)

def pex_remove_page_string(url):
    return re.sub(r"/p\d+", "", url)

def pex_sanitize_url(url):
    return re.sub(r"/p\d+#.*$", "", str(url))

def pex_geturlid(url):
    match = re.search(r"/(\d+)", url)
    if match:
        number = match.group(1)
        return int(number) 
    return start

def url_get(url):
    print(f"START GET: {url}")
    try:
        while True:
            response = requests.get(url)
            if response.status_code == 200:
                print("200 OK")
                return response.content
            elif response.status_code == 502 or response.status_code == 504:
                print("Bad Gateway. Retrying...")
            else:
                print(f"Error: Status code {response.status_code}")                
                return response.status_code
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        sys.exit()
        print(f"Error: {str(e)}")
        return None
def get_link_next(url):
    response = url_get(url)
    if response == 404:
        # get_link_prev()
        return f'https://www.pinoyexchange.com/discussion/{pex_geturlid(url)+1}/'
    if response is not None:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response, "html.parser")

        # Find the <link> tag with "prev" relationship
        prev_link = soup.find("link", rel="prev")

        # Extract the URL of the previous page
        if prev_link:
            prev_url = prev_link.get("href")
            # print("Previous URL:", prev_url)
            return prev_url

        else:            
            canon_link = soup.find("link", rel="canonical")
            if canon_link:
                    return canon_link.get("href")

        return f'https://www.pinoyexchange.com/discussion/{pex_geturlid(url)+1}/'
    return f'https://www.pinoyexchange.com/discussion/{pex_geturlid(url)+1}/'

if not os.path.isfile(pexurls_file):
    open(pexurls_file, "x").close()
links = []
with open(pexurls_file, "r") as f:
    lines = f.read().splitlines()

try:
    with open(pexurls_file, "r") as file:
        
        last_line = lines[-1].strip()  # Get last line of the file and remove trailing newline
        print(last_line)
        discussion_id = int(last_line.split("/")[-2])  # Split URL by "/" and get second-to-last element, then convert to int     
        discussion_id = pex_geturlid(last_line)
except Exception as e:
    discussion_id = start
def start_(strt=10000,end=911218):
    discussion_id = strt
    # print(discussion_id)
    while True:
        if(discussion_id == end+1):
            break
        # sys.exit()
        curlink = pex_sanitize_url(get_link_next(f'https://www.pinoyexchange.com/discussion/{discussion_id}'))
        print(curlink)
        if curlink:        
            with open(pexurls_file, "r") as f:
                lines = f.read().splitlines()
                links = sorted(lines)
            links.append(curlink)
            buddha = sorted(links)
            links = buddha
            if curlink != f"https://www.pinoyexchange.com/discussion/{discussion_id}/" or curlink != "https://www.pinoyexchange.com/entry/signin":
                with open(pexurls_file, "a+") as f:
                    f.write("\n".join(links))
            discussion_id +=1

start_(start,end)
