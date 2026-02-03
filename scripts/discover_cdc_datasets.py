import urllib.request
import json
import ssl

def search_socrata(query):
    # Use SSL context to avoid certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    url = f"http://api.us.socrata.com/api/catalog/v1?search={query}&limit=20"
    
    try:
        with urllib.request.urlopen(url, context=ctx) as response:
            data = json.loads(response.read().decode())
            
        print(f"\n--- Results for '{query}' ---")
        if 'results' in data:
            for item in data['results']:
                res = item['resource']
                # Filter for county level relevance
                name = res.get('name', '')
                desc = res.get('description', '')
                domain = item['metadata']['domain']
                
                if 'county' in name.lower() or 'county' in desc.lower():
                    print(f"ID: {res['id']}")
                    print(f"Name: {name}")
                    print(f"Domain: {domain}")
                    print(f"Updated: {res.get('updatedAt', 'N/A')}")
                    print("-" * 30)
                    
    except Exception as e:
        print(f"Error: {e}")

search_socrata("obesity")
search_socrata("smoking")
