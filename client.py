
import socket
import json

def get_user_orders():
    orders = []
    while True:
        order_type = input("Enter order type (buy/sell): ").strip().lower()
        symbol = input("Enter stock symbol: ").strip().upper()
        quantity = int(input("Enter quantity: ").strip())

        # Add the order to the list
        orders.append({
            'type': order_type,
            'symbol': symbol,
            'quantity': quantity
        })

        another_order = input("Do you want to add another order? (yes/no): ").strip().lower()
        if another_order != 'yes':
            break
    
    return orders

# Create client socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12542))  # 12451

# Get orders from the user
orders = get_user_orders()

# Send list of buy/sell orders to server
client_socket.send(json.dumps(orders).encode('utf-8'))

# Receive real-time stock updates from server
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    # Decode data and print updated stock prices
    stock_prices = json.loads(data.decode('utf-8'))
    print("Updated stock prices:")
    for symbol, price in stock_prices.items():
        print(f"{symbol}: ${price}")

client_socket.close()

