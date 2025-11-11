import pandas as pd
from random import randint

population = {
        'LotArea': [],
        'LotFrontage': [],
        'OverallQual': [],
        'OverallCond': [],
        'YearBuilt': [],
        'TotalBsmtSF': [],
        '1stFlrSF': [],
        'GrLivArea': [],
        'TotRmsAbvGrd': [], 
        'GarageYrBlt': [],
        'GarageArea': [],
        'YrSold': []
    }
for _ in range(5):
    population['LotArea'].append(randint(1300, 71000)) # 215245數值過於極端
    population['LotFrontage'].append(randint(21, 200)) # 313數值過於極端
    population['OverallQual'].append(randint(2, 10))
    population['OverallCond'].append(randint(2, 9))
    population['YearBuilt'].append(randint(1880, 2010))
    population['TotalBsmtSF'].append(randint(0, 3300)) # 6110數值過於極端
    population['1stFlrSF'].append(randint(438, 3300)) # 4692數值過於極端
    population['GrLivArea'].append(randint(438, 4700)) # 5642數值過於極端
    population['TotRmsAbvGrd'].append(randint(3, 12)) 
    population['GarageYrBlt'].append(randint(1900, 2010))
    population['GarageArea'].append(randint(160, 1418))
    population['YrSold'].append(randint(2006, 2010))
        
population = pd.DataFrame(population)
# print(len(population['LotArea']))
factor_space = {
    'LotArea': (3330, 16278),
    'LotFrontage': (34, 107),
    'OverallQual': (4, 9),
    'OverallCond': (4, 8),
    'YearBuilt': (1916, 2007),
    'TotalBsmtSF': (539, 1810),
    '1stFlrSF': (682, 1844),
    'GrLivArea': (864, 2480), 
    'TotRmsAbvGrd': (4, 10), 
    'GarageYrBlt': (1926, 2007),
    'GarageArea': (240, 864),
    'YrSold': (2006, 2010)
}
start_idx = len(population)

for i in range(3):
    population.loc[start_idx + i] = [randint(low, high) for low, high in factor_space.values()]

df = pd.read_csv('home-data-for-ml-course/test.csv')
# df.to_excel('test.xlsx')

for (i, j) in zip([1, 2, 3], [4, 5, 6]):
    print(i, j)
# factor_space = {
#         'LotArea': (3330, 16278),
#         'LotFrontage': (34, 107),
#         'OverallQual': (4, 9),
#         'OverallCond': (4, 8),
#         'YearBuilt': (1916, 2007),
#         'TotalBsmtSF': (539, 1810),
#         '1stFlrSF': (682, 1844),
#         'GrLivArea': (864, 2480), 
#         'TotRmsAbvGrd': (4, 10), 
#         'GarageYrBlt': (1926, 2007),
#         'GarageArea': (240, 864),
#         'YrSold': (2006, 2010)
#     }
# print([randint(low, high) for low, high in factor_space.values()])

# print(population)
# print(population.loc[0])
# for key in population:
#     print(type(population[key][0]))
# row = population.iloc[0]  # 取出第 3 筆（索引從 0 開始）
# can = population.iloc[:5].sample(n=2)
# uu = dict(can.iloc[0])
# ii = dict(can.iloc[1])
#  print(len(list(ii['YrSold'])))
# for key in uu:
#     print(key)
# print(population)
# inds = [2, 3, 1, 4, 0]
# population_sorted = population.iloc[inds].reset_index(drop=True)
# # print(population_sorted)
# print(dict(population)['TotRmsAbvGrd'][-2:])
# print(round(51*0.8))