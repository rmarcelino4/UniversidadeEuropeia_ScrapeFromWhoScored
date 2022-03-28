from   data_viz_helpers import *
import matplotlib.pyplot as plt
import numpy as np
import ScraperFC as sfc
import seaborn as sns
import traceback

home_colors = 'Greens'
home_color = 'green'

away_colors = 'Blues'
away_color = 'blue'
#%%
scraper = sfc.WhoScored()

game = 'https://www.whoscored.com/Matches/1602930/Live/International-World-Cup-Qualification-UEFA-2021-2022-Portugal-Turkey'

#https://www.whoscored.com/Matches/1549379/Live/Russia-Premier-League-2021-2022-FC-Krasnodar-Ural
#https://www.whoscored.com/Matches/1570398/Live/Portugal-Liga-NOS-2021-2022-Pacos-de-Ferreira-FC-Porto
#%%
try:
    match_data = scraper.scrape_match(game)

except:
    traceback.print_exc()
scraper.close()

home_ids = [player['playerId'] for player in match_data['matchCentreData']['home']['players']]
away_ids = [player['playerId'] for player in match_data['matchCentreData']['away']['players']]

home, away = list(), list()
for event in match_data['matchCentreData']['events']:
    if 'playerId' not in event.keys():
        continue
    elif event['playerId'] in home_ids:
        home.append([event['x']*130/100, event['y']*90/100])
    elif event['playerId'] in away_ids:
        away.append([(-event['x']+100) * 130/100,
                     (-event['y']+100) * 90/100])
home, away = np.array(home), np.array(away)

EquipaCasa = match_data['matchCentreData']['home']['name']
EquipaFora = match_data['matchCentreData']['away']['name']
Data = match_data['matchCentreData']['startTime']
#%%

fig, ax = plt.subplots(figsize=[16,12])
x = home[:,0]
y = home[:,1]
ax = plot_field(ax)
ax = sns.kdeplot(x, y, clip=[[0,130], [0,90]], shade=True, thresh=False, cmap=home_colors, alpha=0.7)
ax.scatter(x, y, color='white', edgecolor='black')
ax.text(
    1, 91,
    match_data['matchCentreData']['home']['name'],
    fontsize=30,
    color=home_color,
)
ax.text(
    100, 95,
    match_data['matchCentreData']['startTime'],
    fontsize=10,
    color='black'
)

ax.text(
    100, 93,
    match_data['matchCentreData']['home']['name']+' ' 'vs' ' ' +match_data['matchCentreData']['away']['name'],
    fontsize=10,
    color='black'
)
ax.text(
    100, 91,
    'Resultado final'+': ' + match_data['matchCentreData']['score'],
    fontsize=10,
    color='black'
)

ax.set_title("Heatmap das ações coletivas de uma equipa\nUniv. Europeia - Football Analytics\nRui Marcelino", fontsize=15)
#plt.show()
away_ax = ax
#save figure
fig.savefig(EquipaCasa+'_heatmap_'+Data+'.png', dpi=600)
#%%
fig, ax = plt.subplots(figsize=[16,12])
x = away[:,0]
y = away[:,1]
ax = plot_field(ax)
ax = sns.kdeplot(x, y, clip=[[0,130], [0,90]], shade=True, thresh=False, cmap=away_colors, alpha=0.7)
ax.scatter(x, y, color='white', edgecolor='black')
ax.text(
    1, 91,
    match_data['matchCentreData']['away']['name'],
    fontsize=30,
    color=away_color
)
ax.text(
    100, 95,
    match_data['matchCentreData']['startTime'],
    fontsize=10,
    color='black'
)

ax.text(
    100, 93,
    match_data['matchCentreData']['home']['name']+' ' 'vs' ' ' +match_data['matchCentreData']['away']['name'],
    fontsize=10,
    color='black'
)
ax.text(
    100, 91,
    'Resultado Final'+': ' + match_data['matchCentreData']['score'],
    fontsize=10,
    color='black'
)
ax.set_title("Heatmap das ações coletivas de uma equipa\nUniv. Europeia - Football Analytics\nRui Marcelino", fontsize=15)
#plt.show()
away_ax = ax
#save figure
fig.savefig(EquipaFora+'_heatmap_'+Data+'.png', dpi=600)



fig, axs = plt.subplots(figsize=[16,6], nrows=1, ncols=2)

axs[0] = plot_field(axs[0])
axs[0].axis('off')
axs[1] = plot_field(axs[1])

#### Home ####
x = home[:,0]
y = home[:,1]
axs[0] = sns.kdeplot(x, y, clip=[[0,130], [0,90]], shade=True, thresh=False, cmap=home_colors, alpha=0.7, ax=axs[0])
# axs[0].scatter(x, y, color='white', edgecolor='black')

#### Away ####
x = away[:,0]
y = away[:,1]
axs[1] = sns.kdeplot(x, y, clip=[[0,130], [0,90]], shade=True, thresh=False, cmap=away_colors, alpha=0.7, ax=axs[1])
# axs[1].scatter(x, y, color='white', edgecolor='black')

fig.tight_layout()
#plt.show()
#save figure
fig.savefig(EquipaCasa+' ' + EquipaFora +' ' +'_heatmap_'+Data+'.png', dpi=600)


col_names = ['desc', 'cross_y', 'x', 'y', 'end_x', 'end_y']
home_def_to_mid = pd.DataFrame(columns=col_names)
home_mid_to_att = pd.DataFrame(columns=col_names)
away_def_to_mid = pd.DataFrame(columns=col_names)
away_mid_to_att = pd.DataFrame(columns=col_names)

scraper = sfc.WhoScored()



try:
    match_data = scraper.scrape_match(game)
except:
    traceback.print_exc()
scraper.close()
# Get home and away player IDs
home_ids = [player['playerId'] for player in match_data['matchCentreData']['home']['players']]
away_ids = [player['playerId'] for player in match_data['matchCentreData']['away']['players']]

for event in match_data['matchCentreData']['events']:
    event_desc = event['type']['displayName']
    try:
        player_id = event['playerId']
        m = (event['endY']-event['y']) / (event['endX']-event['x'])
        b = event['y'] - m*event['x']
    except KeyError:
        continue
    except ZeroDivisionError:
        continue
    if player_id in home_ids:
        if event['x']<33.3 and event['endX']>33.3 and event['endX']<66.6 and event_desc!='OffsidePass':
            home_def_to_mid = home_def_to_mid.append(
                pd.Series({
                    'desc': event_desc,
                    'cross_y': m*33.3 + b,
                    'x': event['x'],
                    'y': event['y'],
                    'end_x': event['endX'],
                    'end_y': event['endY']
                }),
                ignore_index=True
            )
        # transition from middle third to attacking third
        elif event['x']<66.6 and event['endX']>66.6 and event['x']>33.3 and event_desc!='OffsidePass':
            home_mid_to_att = home_mid_to_att.append(
                pd.Series({
                    'desc': event_desc,
                    'cross_y': m*66.6 + b,
                    'x': event['x'],
                    'y': event['y'],
                    'end_x': event['endX'],
                    'end_y': event['endY']
                }),
                ignore_index=True
            )
    elif player_id in away_ids:
        if event['x']<33.3 and event['endX']>33.3 and event['endX']<66.6 and event_desc!='OffsidePass':
            away_def_to_mid = away_def_to_mid.append(
                pd.Series({
                    'desc': event_desc,
                    'cross_y': m*33.3 + b,
                    'x': event['x'],
                    'y': event['y'],
                    'end_x': event['endX'],
                    'end_y': event['endY']
                }),
                ignore_index=True
            )
        # transition from middle third to attacking third
        elif event['x']<66.6 and event['endX']>66.6 and event['x']>33.3 and event_desc!='OffsidePass':
            away_mid_to_att = away_mid_to_att.append(
                pd.Series({
                    'desc': event_desc,
                    'cross_y': m*66.6 + b,
                    'x': event['x'],
                    'y': event['y'],
                    'end_x': event['endX'],
                    'end_y': event['endY']
                }),
                ignore_index=True
            )

n_bins = 20
bins = np.linspace(0,100,n_bins)
width = 1
dx_mult = 700
fig, ax = plt.subplots(figsize=[18,12])
ax = plot_field(ax)

# Labels
ax.set_title('As setas indicam a direção do ataque.', y=0.96, fontsize=15)
ax.text(
    1, 91,
    match_data['matchCentreData']['home']['name'],
    fontsize=30,
    color=home_color
)
ax.text(
    129, 91,
    match_data['matchCentreData']['away']['name'],
    fontsize=30,
    color=away_color,
    horizontalalignment='right'
)

# Out of defensive third
ax.plot([130/3, 130/3], [0, 90], color='black')
# Create histograms bins and values for each bin
vals, _ = np.histogram(home_def_to_mid['cross_y'], bins=bins, density=True)
# Plot the bins as arrows indicating the attacking direction. Use the values as the lengths
for i in range(len(vals)):
    if vals[i] == 0:
        continue
    ax.arrow(
        x=130/3, y=(bins[i]+bins[1]/2) * 90/100,
        dx=vals[i]*dx_mult, dy=0,
        width=width, color=home_color
    )
# Now do it for away team
vals, _ = np.histogram(away_def_to_mid['cross_y'], bins=bins, density=True)
for i in range(len(vals)):
    if vals[i] == 0:
        continue
    ax.arrow(
        x=130*2/3,
        # Need to flip and shift away team y values to get them going the other way
        y=(-bins[i]+100-bins[1]/2) * 90/100,
        dx=-vals[i]*dx_mult, dy=0,
        width=width, color=away_color
    )

# Into attacking third
ax.plot([130*2/3, 130*2/3], [0, 90], color='black')
vals, _ = np.histogram(home_mid_to_att['cross_y'], bins=bins, density=True)
for i in range(len(vals)):
    if vals[i] == 0:
        continue
    ax.arrow(
        x=130*2/3, y=(bins[i]+bins[1]/2) * 90/100,
        dx=vals[i]*dx_mult, dy=0,
        width=width, color=home_color, alpha=0.6
    )
# Now do it for away team
vals, _ = np.histogram(away_mid_to_att['cross_y'], bins=bins, density=True)
for i in range(len(vals)):
    if vals[i] == 0:
        continue
    ax.arrow(
        x=130/3, y=(-bins[i]+100-bins[1]/2) * 90/100,
        dx=-vals[i]*dx_mult, dy=0,
        width=width, color=away_color, alpha=0.6
    )

#plt.show()

#save figure
fig.savefig(EquipaCasa+' ' + EquipaFora +' ' +'ataques último terço_'+Data+'.png', dpi=600)
