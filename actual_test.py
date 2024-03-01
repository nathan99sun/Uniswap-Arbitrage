from uniswap import Uniswap
from web3 import Web3
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import bellman_ford
from scipy.optimize import minimize
import pandas as pd
import numpy as np
import re
import networkx as nx
from openpyxl import load_workbook
import random
from web3.auto import w3



address = None #"0x0A60Acc66497f091eF0e7AAE50063007b298897D"          # or None if you're not going to make transactions
private_key = None #"a77e21ad4824aaa9566ed0bc1d7567cdf2bac200dcd4eee9f667e4fd93c10992"  # or None if you're not going to make transactions
version = 3                       # specify which version of Uniswap to use
provider = "https://eth-mainnet.g.alchemy.com/v2/d0gWHSf7Ujhysm20KzkBCucOomzeamy5"
uniswap = Uniswap(address=address, private_key=private_key, version=version, provider=provider)

# Some token addresses we'll be using later in this guide
eth = "0x0000000000000000000000000000000000000000"
#bat = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
usdc = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
usdt = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
wbtc = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
uni = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
reth = "0xae78736Cd615f374D3085123A210448E74Fc6393"
wsteth = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
usde = "0x4c9EDD5852cd905f086C759E8383e09bff1E68B3"
ondo = "0xfAbA6f8e4a5E8Ab82F62fe7C39859FA577269BE3"

tokens = [eth, dai, usdc, usdt, wbtc, uni, reth, wsteth, usde, ondo]

def construct_graph(grapharray):
    G = nx.DiGraph()
    for elt in tokens:
        G.add_node(elt)
    for row in grapharray:
        token0 = row[0]
        token1 = row[1]
        price = row[2]
        fee = row[3]
            #print(feetier)
        G.add_weighted_edges_from( [(token0, token1, -np.log(price * (1-fee)))] )
        G.add_weighted_edges_from( [(token1, token0, -np.log(1/price * (1-fee)))] )
    return G
            
def find_cycle(G, tokens):
    random.shuffle(tokens)
    for t in tokens:
        try:
            nx.find_negative_cycle(G, t)
        except Exception:
            pass
        else:
            cycle = nx.find_negative_cycle(G, t)
            if len(cycle)>3:
                return nx.find_negative_cycle(G, t)
            

def uniswap_rate(A,B,alpha):
    return B/(A+alpha)

#print(uniswap.get_price_input(eth, dai, 100000))
grapharray = []
n = len(tokens)
for i in range(n):
    for j in range(i+1, n):
        elt1 = tokens[i]
        elt2 = tokens[j]
        try:         
            uniswap.get_pool_instance(elt1, elt2)
        except Exception:
            pass
        else:
            contract = uniswap.get_pool_instance(elt1, elt2)
            sqrtPriceX96 = uniswap.get_pool_state(contract)["sqrtPriceX96"]
            liquidity = uniswap.get_pool_state(contract)["liquidity"]
            token0 = uniswap.get_pool_immutables(contract)['token0']
            token1 = uniswap.get_pool_immutables(contract)['token1']
            fee = uniswap.get_pool_immutables(contract)['fee']
    
            price =  (sqrtPriceX96/  2 ** 96)**2

            print(token0 + " & " + token1)
            print(price)
            grapharray.append([token0, token1, price, fee])


print("done")
G = construct_graph(grapharray)

print(find_cycle(G, tokens))
