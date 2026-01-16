# utils/data_processor.py

# -----------------------------------------
# TOTAL REVENUE
# -----------------------------------------
def calculate_total_revenue(data):
    # this will store final revenue
    total = 0.0

    for item in data:
        qty = item['Quantity']
        price = item['UnitPrice']
        total = total + (qty * price)

    return total


# -----------------------------------------
# REGION WISE SALES
# -----------------------------------------
def region_wise_sales(data):
    region_info = {}

    total_sales = calculate_total_revenue(data)

    for item in data:
        reg = item['Region']
        qty = item['Quantity']
        price = item['UnitPrice']
        amount = qty * price

        if reg not in region_info:
            region_info[reg] = {}
            region_info[reg]['sales'] = 0.0
            region_info[reg]['count'] = 0

        region_info[reg]['sales'] = region_info[reg]['sales'] + amount
        region_info[reg]['count'] = region_info[reg]['count'] + 1

    for reg in region_info:
        if total_sales == 0:
            region_info[reg]['percent'] = 0
        else:
            value = (region_info[reg]['sales'] / total_sales) * 100
            region_info[reg]['percent'] = round(value, 2)

    sorted_regions = sorted(
        region_info.items(),
        key=lambda x: x[1]['sales'],
        reverse=True
    )

    return dict(sorted_regions)


# -----------------------------------------
# TOP SELLING PRODUCTS
# -----------------------------------------
def top_selling_products(data, limit=5):
    product_info = {}

    for item in data:
        name = item['ProductName']
        qty = item['Quantity']
        price = item['UnitPrice']

        if name not in product_info:
            product_info[name] = {}
            product_info[name]['qty'] = 0
            product_info[name]['money'] = 0.0

        product_info[name]['qty'] = product_info[name]['qty'] + qty
        product_info[name]['money'] = product_info[name]['money'] + (qty * price)

    sorted_products = sorted(
        product_info.items(),
        key=lambda x: x[1]['qty'],
        reverse=True
    )

    output = []

    for p in sorted_products[:limit]:
        output.append((p[0], p[1]['qty'], p[1]['money']))

    return output


# -----------------------------------------
# CUSTOMER ANALYSIS
# -----------------------------------------
def customer_analysis(data):
    customer_info = {}

    for item in data:
        cid = item['CustomerID']
        qty = item['Quantity']
        price = item['UnitPrice']
        product = item['ProductName']
        amount = qty * price

        if cid not in customer_info:
            customer_info[cid] = {}
            customer_info[cid]['spent'] = 0.0
            customer_info[cid]['orders'] = 0
            customer_info[cid]['items'] = []

        customer_info[cid]['spent'] = customer_info[cid]['spent'] + amount
        customer_info[cid]['orders'] = customer_info[cid]['orders'] + 1

        if product not in customer_info[cid]['items']:
            customer_info[cid]['items'].append(product)

    for cid in customer_info:
        total = customer_info[cid]['spent']
        count = customer_info[cid]['orders']

        if count == 0:
            avg = 0
        else:
            avg = total / count

        customer_info[cid]['average'] = round(avg, 2)
        customer_info[cid]['products_bought'] = customer_info[cid]['items']
        del customer_info[cid]['items']

    sorted_customers = sorted(
        customer_info.items(),
        key=lambda x: x[1]['spent'],
        reverse=True
    )

    return dict(sorted_customers)


# -----------------------------------------
# DAILY SALES TREND
# -----------------------------------------
def daily_sales_trend(data):
    daily = {}

    for item in data:
        date = item['Date']
        qty = item['Quantity']
        price = item['UnitPrice']
        cid = item['CustomerID']
        amount = qty * price

        if date not in daily:
            daily[date] = {}
            daily[date]['sales'] = 0.0
            daily[date]['count'] = 0
            daily[date]['customers'] = []

        daily[date]['sales'] = daily[date]['sales'] + amount
        daily[date]['count'] = daily[date]['count'] + 1

        if cid not in daily[date]['customers']:
            daily[date]['customers'].append(cid)

    for date in daily:
        daily[date]['unique_customers'] = len(daily[date]['customers'])
        del daily[date]['customers']

    return dict(sorted(daily.items()))


# -----------------------------------------
# PEAK SALES DAY
# -----------------------------------------
def find_peak_sales_day(data):
    daily = daily_sales_trend(data)

    best_day = ""
    best_amount = 0.0
    best_count = 0

    for date in daily:
        if daily[date]['sales'] > best_amount:
            best_amount = daily[date]['sales']
            best_count = daily[date]['count']
            best_day = date

    return best_day, best_amount, best_count


# -----------------------------------------
# LOW PERFORMING PRODUCTS
# -----------------------------------------
def low_performing_products(data, limit=10):
    product_info = {}

    for item in data:
        name = item['ProductName']
        qty = item['Quantity']
        price = item['UnitPrice']

        if name not in product_info:
            product_info[name] = {}
            product_info[name]['qty'] = 0
            product_info[name]['money'] = 0.0

        product_info[name]['qty'] = product_info[name]['qty'] + qty
        product_info[name]['money'] = product_info[name]['money'] + (qty * price)

    low_list = []

    for name in product_info:
        if product_info[name]['qty'] < limit:
            low_list.append(
                (name, product_info[name]['qty'], product_info[name]['money'])
            )

    low_list.sort(key=lambda x: x[1])

    return low_list