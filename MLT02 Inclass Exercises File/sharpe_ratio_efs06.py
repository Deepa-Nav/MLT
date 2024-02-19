# For data manipulation
import numpy as np
import pandas as pd

# Line 1: Import the data
data = pd.read_csv("../data_modules/data_EFS06Q2.csv")

# Line 2: Get the asset names from the data columns as a list
asset_names = data.columns.tolist()[1:]

# Line 3: Set the Nifty allocation weight
nifty_weight = 0.05

# Line 4: Set the Junior allocation weight
junior_weight = 0.02

# Line 5: Set the Gold allocation weight
gold_weight =0.03

# Line 6: Save the allocation weights together as a list
#Create an array named allocations in which you will save three weights from above. Use the correct numpy method.
allocations = np.array([nifty_weight, junior_weight, gold_weight])

# Line 7: Set the initial capital to 100m
initial_capital = 100000000

# Create a list to save the quarter-end dates
quarter_end_dates = list()

# Run a loop to save the quarter-end dates
for year in [2016, 2017]:
    for month in [3, 6, 9, 12]:
        # Line 8: Save the dates of each yearly quarter
        monthly_data_dates = data.loc[f'{year}-{month}'].index     
        # Line 9: Obtain the last date of the yearly quarter dates
        quarter_end_date = monthly_data_dates[-1]
        
        # Append the quarter-end date to the list
        quarter_end_dates.append(quarter_end_date)

# Create the portfolio column
data['values'] = 0.0

# Create a list to save the name of the assets for the number of shares 
num_shares_names = [f'{asset}_num_shares' for asset in asset_names]

# Create the asset columns for saving the number of shares 
data[num_shares_names] = 0.0

# Line 10: Create an array for the number of shares
data.loc[data.index[0], num_shares_names] = np.floor(initial_capital * allocations / data[asset_names].iloc[0].values)

# Saving the array of the number of shares per asset as an array
num_shares = data.loc[data.index[0], num_shares_names]

# Line 11: Compute the portfolio value for the first day of the investment period
data['values'].iloc[0] = np.sum(num_shares * data[asset_names].iloc[0].values)

# Run a loop to fill the portfolio values
for i in range(1,len(data.index)):
    
    # Line 12: Compute the portfolio value in case we are not in the rebalancing date
    data['values'].iloc[i] = np.round(np.sum(num_shares * data[asset_names].iloc[i].values), 2)
    
    # In case we are on the portfolio-rebalacing date 
    if data.index[i] in quarter_end_dates:  
        # Line 13: Do the rebalacing by obtaining the number of shares
        num_shares = np.floor(data['values'].iloc[i] * allocations / data[asset_names].iloc[i].values)
        print(f'Portfolio allocation for date {data.index[i].date()} is {num_shares}')
        
        # Saving the number of shares per asset as an array
        #num_shares = data[num_shares_names].iloc[i]

# Line 14: Subset the 2016 portfolio values
portfolio_2016 = data.loc['2016', 'values']

# Line 15: Subset the 2017 portfolio values
portfolio_2017 = data.loc['2017', 'values']

# Line 16: Obtain the 2016 portfolio returns and save then in another dataframe
portfolio_rets_2016 = portfolio_2016.pct_change().dropna()

# Line 17: Obtain the 2017 portfolio returns and save then in another dataframe
portfolio_rets_2017 = portfolio_2017.pct_change().dropna()

# Line 18: Get the 2016 annualised returns
annualised_ret_2016 = portfolio_2016.iloc[-1]/portfolio_2016.iloc[0] - 1

# Line 19: Get the 2017 annualised returns
annualised_ret_2017 = portfolio_2017.iloc[-1]/portfolio_2017.iloc[0] - 1

# Line 20: Obtain the 2016 Sharpe ratio
sharpe_ratio_2016 = portfolio_rets_2016.mean()/portfolio_rets_2016.std()*np.sqrt(252)

# Line 21: Obtain the 2017 Sharpe ratio
sharpe_ratio_2017 = ____

# Print the annualised returns for 2016 and 2017
print(f'Annualised return for 2016 and 2017 are {annualised_ret_2016 * 100: .2f} and {annualised_ret_2017 * 100: .2f}, respectively.')

# Print the Sharpe ratio for 2016 and 2017
print(f'Sharpe ratio for 2016 and 2017 are {sharpe_ratio_2016: .2f} and {sharpe_ratio_2017: .2f}, respectively.')