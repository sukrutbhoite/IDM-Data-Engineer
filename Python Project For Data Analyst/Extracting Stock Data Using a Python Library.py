import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt # <--- Add this import!

# Fetch Apple stock data
apple = yf.Ticker("AAPL")
apple_share_price_data = apple.history(period="max")

# Reset the index to make 'Date' a regular column
apple_share_price_data.reset_index(inplace=True)

# Plot Open vs Date
# We assign the plot to an Axes object (ax1) for better control,
# but the key is the plt.show() call right after.
ax1 = apple_share_price_data.plot(x="Date", y="Open", title="AAPL Open Price Over Time")
plt.xlabel("Date") # Add an x-axis label for clarity
plt.ylabel("Open Price ($)") # Add a y-axis label
plt.grid(True) # Add a grid for easier reading
plt.show() # <--- This line tells matplotlib to display the first plot!

# Print Apple Dividends data
print("\n--- Apple Dividends Data ---")
print(apple.dividends)

# Plot Dividends
# Similarly, we plot the dividends and then call plt.show()
ax2 = apple.dividends.plot(title="AAPL Dividends History", figsize=(12, 6)) # Adjust figsize for better view
plt.xlabel("Date") # Add x-axis label
plt.ylabel("Dividend Amount ($)") # Add y-axis label
plt.grid(True)
plt.show() # <--- This line tells matplotlib to display the second plot!

print("\nPlots generated successfully!")