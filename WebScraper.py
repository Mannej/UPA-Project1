import requests

# API URL
api_url = 'https://www.electrocity.ie/wp-json/wp/v2/product?product_cat=232'

def getProductList(): 
    product_links = []
    params = {'page': 1}  # Starting page number

    while True:
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            products = response.json()

            # Check if any products were returned
            if not products:
                break  # Exit the loop if no more products are found

            # Extract product URLs from the JSON response
            for product in products:
                product_url = product.get('link') 
                if product_url:
                    product_links.append(product_url)

            # Increment the page number for the next request
            params['page'] += 1
        else:
            print(f"Failed to retrieve products. Status code: {response.status_code}")
            break
            
    return product_links

def saveToFile(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')  # Write each link on a new line

if __name__ == "__main__":
    urls = getProductList()  # Call the function with parentheses
    for idx, link in enumerate(urls, start=1):
        print(f"{idx}: {link}")  # Corrected print statement
    saveToFile(urls, "urls.txt")
