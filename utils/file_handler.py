# utils/file_handler.py

# --------------------------------------------------
# FUNCTION 1: READ SALES DATA FROM FILE
# --------------------------------------------------
def read_sales_data(file_path):
    """
    This function reads a sales file.
    It tries different encodings because some files
    do not open with utf-8.
    It returns all lines except the first line (header).
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']

    for enc in encodings:
        try:
            file = open(file_path, 'r', encoding=enc)
            lines = file.readlines()
            file.close()

            data_lines = []

            # skip first line because it is header
            for line in lines[1:]:
                line = line.strip()   # remove spaces and \n
                if line != "":
                    data_lines.append(line)

            return data_lines

        except UnicodeDecodeError:
            # if this encoding does not work, try next
            continue

        except FileNotFoundError:
            print("File not found:", file_path)
            return []

    print("File encoding not supported")
    return []


# --------------------------------------------------
# FUNCTION 2: PARSE RAW LINES INTO DICTIONARY
# --------------------------------------------------
def parse_transactions(lines):
    """
    This function converts each line into a dictionary.
    Each line should have 8 values separated by '|'
    """

    transactions = []
    invalid_count = 0

    for line in lines:
        line = line.strip()

        if line == "":
            continue

        parts = line.split('|')

        # if line does not have 8 parts, skip it
        if len(parts) != 8:
            invalid_count = invalid_count + 1
            continue

        try:
            transaction = {}

            transaction['TransactionID'] = parts[0]
            transaction['Date'] = parts[1]
            transaction['ProductID'] = parts[2]

            # remove commas from product name
            transaction['ProductName'] = parts[3].replace(',', '')

            # convert quantity to int
            transaction['Quantity'] = int(parts[4])

            # remove commas and convert price to float
            price = parts[5].replace(',', '')
            transaction['UnitPrice'] = float(price)

            transaction['CustomerID'] = parts[6]
            transaction['Region'] = parts[7]

            transactions.append(transaction)

        except:
            invalid_count = invalid_count + 1

    return transactions, invalid_count


# --------------------------------------------------
# FUNCTION 3: VALIDATE AND FILTER TRANSACTIONS
# --------------------------------------------------
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    This function checks whether transactions are valid.
    It can also filter by region and total amount.
    """

    valid_transactions = []

    invalid = 0
    removed_region = 0
    removed_amount = 0

    for t in transactions:
        quantity = t['Quantity']
        price = t['UnitPrice']
        amount = quantity * price

        # basic validation checks
        if quantity <= 0:
            invalid = invalid + 1
            continue

        if price <= 0:
            invalid = invalid + 1
            continue

        if t['CustomerID'] == "":
            invalid = invalid + 1
            continue

        if t['Region'] == "":
            invalid = invalid + 1
            continue

        if t['TransactionID'][0] != 'T':
            invalid = invalid + 1
            continue

        if t['ProductID'][0] != 'P':
            invalid = invalid + 1
            continue

        if t['CustomerID'][0] != 'C':
            invalid = invalid + 1
            continue

        # region filter
        if region is not None:
            if t['Region'] != region:
                removed_region = removed_region + 1
                continue

        # minimum amount filter
        if min_amount is not None:
            if amount < min_amount:
                removed_amount = removed_amount + 1
                continue

        # maximum amount filter
        if max_amount is not None:
            if amount > max_amount:
                removed_amount = removed_amount + 1
                continue

        # if everything is okay, add to valid list
        valid_transactions.append(t)

    summary = {}
    summary['total_input'] = len(transactions)
    summary['invalid'] = invalid
    summary['filtered_by_region'] = removed_region
    summary['filtered_by_amount'] = removed_amount
    summary['final_count'] = len(valid_transactions)

    return valid_transactions, summary

