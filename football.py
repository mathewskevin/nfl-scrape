import os
import pandas as pd
import pdb

#football_file = [i for i in os.listdir() if i.endswith('.xlsx')][0]
football_file = 'football.csv'

data = pd.read_csv('football.csv', header=None)
win_rates = pd.read_csv('win_rates.csv')

bottom_index = int(data.shape[0] / 2)

top_df = data.iloc[0:bottom_index]
top_df = top_df[top_df[1].notna()]

bottom_df = data.iloc[bottom_index:]
bottom_df = bottom_df[bottom_df[1].notna()]

games = top_df[[0,1]]
top_df = top_df.iloc[:, 2:].reset_index(drop=True)
bottom_df = bottom_df.iloc[:, 2:].reset_index(drop=True)

picks = pd.concat([top_df, bottom_df], axis=1).dropna(axis=1)
games.columns = ['Visitor','Home']

df_list = []; loc_list = []
for idx, row in games.iterrows():
	home = row['Home']; home_rate = win_rates.loc[win_rates['Will Name']==home,['Win Rate']]
	visitor = row['Visitor']; visitor_rate = win_rates.loc[win_rates['Will Name']==visitor,['Win Rate']]
	
	if home_rate.shape[0] == 1:
		home_rate = home_rate.iloc[0,0]
	else:
		print(home_rate.shape)
	
	if visitor_rate.shape[0] == 1:
		visitor_rate = visitor_rate.iloc[0,0]
	else:
		print(visitor_rate.shape)
	
	if home_rate > visitor_rate:
		df_list.append(home)
		loc_list.append('Home')
	else:
		df_list.append(visitor)
		loc_list.append('Visitor')
	
my_picks_df = pd.DataFrame(df_list, columns=['My Picks'])
my_loc_df = pd.DataFrame(loc_list, columns=['My Picks'])
	
df_list = []
for idx, row in picks.iterrows():
    df_counts = row.value_counts()
    idx_vals  =[i for i in df_counts.index]
    row_vals = [str(i) for i in df_counts.values]
    
    str_list = []
    for i in range(0, len(idx_vals)):
        str_val = row_vals[i] + ' ' + idx_vals[i]
        str_list.append(str_val)
    
    df_list.append(' | '.join(str_list))

count_df = pd.DataFrame(df_list, columns=['Counts'])

games_df = games.reset_index(drop=True)
count_df = count_df.reset_index(drop=True)

games_df = pd.concat([games_df, my_loc_df], axis=1)
games_df = pd.concat([games_df, my_picks_df], axis=1)
games_df = pd.concat([games_df, count_df], axis=1)
games_df = pd.concat([games_df, picks], axis=1)
games_df.to_excel('output.xlsx', index=False)

print('done.')