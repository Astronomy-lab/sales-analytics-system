# ---------------- FILE HANDLING ----------------
from utils.file_handler import read_sales_data
from utils.file_handler import parse_transactions
from utils.file_handler import validate_and_filter

# ---------------- DATA PROCESSING ----------------
from utils.data_processor import calculate_total_revenue
from utils.data_processor import region_wise_sales
from utils.data_processor import top_selling_products
from utils.data_processor import low_performing_products
from utils.data_processor import customer_analysis
from utils.data_processor import daily_sales_trend
from utils.data_processor import find_peak_sales_day
from utils.data_processor import generate_sales_report

# ---------------- API ----------------
from utils.api_handler import fetch_all_products
from utils.api_handler import create_product_mapping
from utils.api_handler import enrich_sales_data
from utils.api_handler import save_enriched_data


def main():

    print("----------------------------------------")
    print("        SALES ANALYSIS PROGRAM")
    print("----------------------------------------")

    try:
        # STEP 1: READ FILE
        print("\nStep 1: Reading sales file")
        lines = read_sales_data("data/sales_data.txt")
        print("Total lines read:", len(lines))

        # STEP 2: PARSE DATA
        print("\nStep 2: Parsing data")
        data, wrong_rows = parse_transactions(lines)
        print("Valid records:", len(data))
        if wrong_rows > 0:
            print("Invalid rows skipped:", wrong_rows)

        # STEP 3: FILTER OPTION
        print("\nStep 3: Filter options")

        region_list = []
        amount_list = []

        for item in data:
            if item['Region'] not in region_list:
                region_list.append(item['Region'])

            amount_list.append(item['Quantity'] * item['UnitPrice'])

        print("Available regions:", ", ".join(region_list))
        print("Amount range:", min(amount_list), "to", max(amount_list))

        user_choice = input("Do you want to filter data? (y/n): ").lower()

        if user_choice == "y":
            user_region = input("Enter region (leave blank for all): ").strip()
            if user_region == "":
                user_region = None

            min_amt = input("Enter minimum amount (leave blank): ").strip()
            max_amt = input("Enter maximum amount (leave blank): ").strip()

            if min_amt == "":
                min_amt = None
            else:
                min_amt = float(min_amt)

            if max_amt == "":
                max_amt = None
            else:
                max_amt = float(max_amt)

            valid_data, info = validate_and_filter(
                data,
                region=user_region,
                min_amount=min_amt,
                max_amount=max_amt
            )
        else:
            valid_data, info = validate_and_filter(data)

        # STEP 4: VALIDATION RESULT
        print("\nStep 4: Validation result")
        print("Final valid records:", info['final_count'])
        print("Invalid records:", info['invalid'])

        # STEP 5: BASIC ANALYSIS
        print("\nStep 5: Doing analysis")
        calculate_total_revenue(valid_data)
        region_wise_sales(valid_data)
        top_selling_products(valid_data)
        low_performing_products(valid_data)
        customer_analysis(valid_data)
        daily_sales_trend(valid_data)
        find_peak_sales_day(valid_data)
        print("Analysis finished")

        # STEP 6: API DATA
        print("\nStep 6: Getting product data from API")
        api_data = fetch_all_products()
        print("Products received from API:", len(api_data))

        # STEP 7: ENRICH DATA
        print("\nStep 7: Matching sales data with API data")
        product_map = create_product_mapping(api_data)
        enriched_data = enrich_sales_data(valid_data, product_map)

        matched = 0
        for item in enriched_data:
            if item.get("API_Match") == True:
                matched = matched + 1

        if len(valid_data) > 0:
            percent = (matched / len(valid_data)) * 100
        else:
            percent = 0

        print("Matched records:", matched)
        print("Match percentage:", round(percent, 2), "%")

        # STEP 8: SAVE ENRICHED DATA
        print("\nStep 8: Saving enriched data")
        save_enriched_data(enriched_data)

        # STEP 9: REPORT
        print("\nStep 9: Creating report file")
        generate_sales_report(valid_data, enriched_data)

        # STEP 10: DONE
        print("\nStep 10: Program finished successfully")
        print("----------------------------------------")

    except Exception as err:
        print("\nSome error occurred")
        print("Error message:", err)
        print("Please check input files and folder names")


# PROGRAM START
if __name__ == "__main__":
    main()




