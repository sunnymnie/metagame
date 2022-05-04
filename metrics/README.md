# Metrics gold-panning

Plan: 
1. Find possible addresses ...somehow...
    - May want to create another algorithm to find pumped cryptos
    - Or pass in a pumped ERC20 and outputs a list of all addresses that transacted between two times
2. Assign each address a score
    - A combination of winrate and average trade sizes and number of trades

Program in completion:
- Input a token with block range, output a dataframe of addresses and corresponding whale-score and other metrics