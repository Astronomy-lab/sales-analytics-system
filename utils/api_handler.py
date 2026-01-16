# utils/api_handler.py

import requests


# -----------------------------------------
# FETCH ALL PRODUCTS FROM API
# -----------------------------------------
def fetch_all_products():
    """
    This function gets product data from DummyJSON API
    """

    api_url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(api_url, timeout=10)

        # check if request worked
        response.raise_for_status()

        data = response.json()

        if "products" in data:
            product_list = data["products"]
        else:
            product_list = []

        print("API SUCCESS - Total products:", len(product_list))
        return product_list

    except Exception as error:
        print("API ERROR:", error)
        return []


# -----------------------------------------
# CREATE PRODUCT ID MAPPING
# -----------------------------------------
def create_product_mapping(api_products):
    """
    Creates a dictionary using product id as key
    """

    mapping = {}

    for product in api_products:
        pid = product.get("id")

        mapping[pid] = {}
        mapping[pid]['title'] = product.get("title")
        mapping[pid]['category'] = product.get("category")
        mapping[pid]['brand'] = product.get("brand")
        mapping[pid]['rating'] = product.get("rating")

    return mapping


# -----------------------------------------
# ENRICH SALES DATA USING API DATA
# -----------------------------------------
def enrich_sales_data(transactions, product_map):
    """
    Adds API details to sales transactions
    """

    final_data = []

    for item in transactions:
        new_item = item.copy()

        try:
            # ProductID looks like P101, so remove P
            product_id_text = item['ProductID'].replace("P", "")
            product_id_number = int(product_id_text)

            if product_id_number in product_map:
                new_item['API_Category'] = product_map[product_id_number]['category']
                new_item['API_Brand'] = product_map[product_id_number]['brand']
                new_item['API_Rating'] = product_map[product_id_number]['rating']
                new_item['API_Match'] = True
            else:
                new_item['API_Category'] = None
                new_item['API_Brand'] = None
                new_item['API_Rating'] = None
                new_item['API_Match'] = False

        except:
            new_item['API_Category'] = None
            new_item['API_Brand'] = None
            new_item['API_Rating'] = None
            new_item['API_Match'] = False

        final_data.append(new_item)

    return final_data


# -----------------------------------------
# SAVE ENRICHED DATA TO FILE
# -----------------------------------------
def save_enriched_data(data, file_name="data/enriched_sales_data.txt"):
    """
    Saves enriched data into a text file
    """

    file = open(file_name, "w", encoding="utf-8")

    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    file.write(header)

    for item in data:
        line = (
            item['TransactionID'] + "|" +
            item['Date'] + "|" +
            item['ProductID'] + "|" +
            item['ProductName'] + "|" +
            str(item['Quantity']) + "|" +
            str(item['UnitPrice']) + "|" +
            item['CustomerID'] + "|" +
            item['Region'] + "|" +
            str(item.get('API_Category')) + "|" +
            str(item.get('API_Brand')) + "|" +
            str(item.get('API_Rating')) + "|" +
            str(item.get('API_Match')) + "\n"
        )

        file.write(line)

    file.close()

    print("Enriched data saved in file:", file_name)
