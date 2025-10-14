import yfinance as yf

msft = yf.Ticker("MSFT")
info = msft.info
print("Company Name:", info.get('longName'))
print("Sector:", info.get('sector'))
print("Industry:", info.get('industry'))
print("Employees:", info.get('fullTimeEmployees'))
print("Market Cap:", info.get('marketCap'))
print("Revenue:", info.get('totalRevenue'))

print("\n--- Recent Stock Performance ---")
hist = msft.history(period="1mo")
print("Current Price:", hist['Close'].iloc[-1])
print("Month High:", hist['High'].max())
print("Month Low:", hist['Low'].min())