import requests
import json

# URL where form sends data
url = "https://mnr.pitc.com.pk/get_data.php"   # change this to real URL

def scrape_contact(refnumber):    
        
    try: 
        # Data you want to send
            # "refnumber": "01131540135800"
        payload = {
            "refnumber": refnumber
        }

        # Send POST request
        response = requests.get(url, params=payload)

        with open(f"DATA/CONTACT/contact.json", "r") as f:
            existing_data = json.load(f)
        
        existing_data[refnumber] = response.json()
        
        with open(f"DATA/CONTACT/contact.json", "w") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        return response.text

    except Exception as e:
        return {"error": "Failed to scrape contact details", "details": str(e)}


# scrape_contact("01131540135800")


