def execute_trade(config, market_data):
    if market_data['price'] is None or market_data['moving_average'] is None:
        print("Skipping trade execution due to missing market data.")
        return
    
    if market_data['price'] > market_data['moving_average']:
        trade_decision = "BUY"
    elif market_data['price'] < market_data['moving_average']:
        trade_decision = "SELL"
    else:
        trade_decision = "HOLD"
    
    print(f"AI Strategy decided to {trade_decision} based on market trends.")
