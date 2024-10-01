from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json

# Open and read the file
try:
    with open('urls.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]
except:
    print("Error opening file urls.txt")
    exit()

# Headers to avoid 403 error
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
for url in urls[:10]:
    try:
        request = Request(url, headers=headers)
        page = urlopen(request)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')

        # Url
        print(url, end="\t")

        # Name of the product
        name_script = soup.find('script', type='application/ld+json')
        json_data = json.loads(name_script.string)
        if json_data.get('name'):
            name = json_data.get('name')
            print(name, end="\t")
        else:
            print("Name not found", end="\t")

        # Price of the product
        price_meta = soup.find('meta', property='product:price:amount')
        if price_meta:
            price = price_meta['content']
            print(price + " €", end="\t")
        else:
            print("Price not found", end="\t")

        # Color of the product
        color_th = soup.find('th', text='Colour')
        if color_th:
            color = color_th.find_next('td').get_text(strip=True)
            print(color, end="\t")
        else:
            print("Color not found", end="\t")

        # Weight of the product
        weight_th = soup.find('th', text='Weight')
        if weight_th:
            weight = weight_th.find_next('td').get_text(strip=True)
            print(weight, end="\t")
        else:
            print("Weight not found", end="\t")

        # Smart features of the product
        smart_th = soup.find('th', text='Smart')
        if smart_th:
            smart_features = smart_th.find_next('td').get_text(strip=True)
            print(smart_features, end="\t")
        else:
            print("Smart features not found", end="\t")

        # Energy class of the product
        energy_class = None
        energy_labels = ['Energy Class', 'Energy efficiency rating', 'Energy Rating', 'Energy Efficiency Class', 'Energy efficiency class']
        for label in energy_labels:
            energy_th = soup.find('th', text=label)
            if energy_th:
                energy_class = energy_th.find_next('td').get_text(strip=True)
                print(energy_class, end="\t")
                break
        if not energy_class:
            print("Energy class not found", end="\t")

        # Noise level (dB) of the product 
        noise_level = None
        noise_labels = ['Noise level dB(A)', 'Noise level', 'Noise Level (dBa)', 'Noise Level dB(A)', 'Airborne acoustical noise emissions']
        for label in noise_labels:
            noise_th = soup.find('th', text=label)
            if noise_th:
                noise_level = noise_th.find_next('td').get_text(strip=True)
                if "dB" not in noise_level:
                    noise_level += " dB(A)"
                print(noise_level)
                break
        if not noise_level:
            print("Noise level not found")

    except Exception as e:
        print(f"An error occurred: {e}")