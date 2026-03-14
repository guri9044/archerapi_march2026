import requests

def get_cat_fact():
    # The endpoint to get a single random cat fact is /fact
    url = "https://catfact.ninja/fact"
    
    try:
        # Make a GET request to the API
        response = requests.get(url)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Extract and print the fact
        fact = data.get("fact")
        if fact:
            print("Here is a random cat fact:")
            print(f"🐾 {fact}")
        else:
            print("Could not parse the fact from the API response.")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the cat fact: {e}")

if __name__ == "__main__":
    get_cat_fact()
