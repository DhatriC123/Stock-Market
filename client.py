import socket
import json

# Create client socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12541))  # Changed port number

# Send list of buy/sell orders to server
orders = [
    {'type': 'sell', 'symbol': 'AAPL', 'quantity': 10},
    {'type': 'buy', 'symbol': 'MSFT', 'quantity': 5},
    {'type': 'sell', 'symbol': 'GOOG', 'quantity': 2}
]

client_socket.send(json.dumps(orders).encode('utf-8'))

# Receive real-time stock updates from server
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    # Decode data and print updated stock prices
    stock_prices = json.loads(data.decode('utf-8'))
    print(stock_prices)

client_socket.close()
