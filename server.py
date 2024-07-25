import socket
import threading
import json
import requests

# List to store traded stocks
traded_stocks = []

def print_traded_stocks():
    for trade in traded_stocks:
        print(f"{trade['type'].capitalize()} {trade['quantity']} shares of {trade['symbol']}")

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        # Receive data from client
        data = client_socket.recv(1024)
        if not data:
            break
        # Decode data and process buy/sell orders
        orders = json.loads(data.decode('utf-8'))
        for order in orders:
            if order['type'] == 'buy':
                # Process buy order
                traded_stocks.append(order)
            elif order['type'] == 'sell':
                # Process sell order
                traded_stocks.append(order)
        print_traded_stocks()

        # Retrieve real-time stock prices and send to client
        stock_prices = get_stock_prices([order['symbol'] for order in orders])
        client_socket.send(json.dumps(stock_prices).encode('utf-8'))
    client_socket.close()

# Function to retrieve real-time stock prices
def get_stock_prices(symbols):
    api_key = "42W8WWTN825APKYX"  # Your Alpha Vantage API key
    stock_prices = {}
    for symbol in symbols:
        response = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}')
        data = response.json()
        stock_prices[symbol] = data['Global Quote']['05. price']
    return stock_prices

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12542))  # Changed port number
    server.listen(5)
    print("Server listening on port 12542")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()
