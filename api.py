import alpaca_trade_api as tradeapi
import config
import websocket
import json

def convertWatchlist():
    stockList = ['AAPL', 'NVDA', 'AMD', 'IBM', 'AMZN', 'TCS']
    #api = tradeapi.REST(config.APCA_API_KEY_ID, config.APCA_API_SECRET_KEY, config.APCA_API_BASE_URL)
    api = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_API_SECRET_KEY, config.APCA_API_BASE_URL)
    watchList = []

    for stock in stockList:
        data = api.get_asset(stock)
        symbol = data.__getattr__('symbol')
        exchange = data.__getattr__('exchange')

        x = str(exchange + ':' + symbol)
        watchList.append(x)

    return watchList

def on_message(ws, message):
    data = json.loads(message)
    symbol = data['T']
    last_price = data['c']

    # Emit the symbol and last price to all connected clients
    socketio.emit('update_symbol', {'symbol': symbol, 'last_price': last_price}, broadcast=True)

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    for symbol in convertWatchlist():
        ws.send(json.dumps({
            "action": "listen",
            "data": {
                "streams": [f"trade_updates:{symbol}"]
            }
        }))

# Run the WebSocket connection in a separate thread
def start_websocket():
    ws_url = "wss://stream.data.alpaca.markets/v2/sip"

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.on_open = on_open

    ws.run_forever()

if __name__ == "__main__":
    from threading import Thread

    # Start the WebSocket connection in a separate thread
    websocket_thread = Thread(target=start_websocket)

    # Start the thread
    websocket_thread.start()
