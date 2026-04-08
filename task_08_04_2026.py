def calculate_bill(price, tax=10, discount=20):
    price_with_tax = price + (price * tax / 100)
    final_price = price_with_tax - (price_with_tax * discount / 100)
    return final_price
bill=calculate_bill(1000)
print(bill)