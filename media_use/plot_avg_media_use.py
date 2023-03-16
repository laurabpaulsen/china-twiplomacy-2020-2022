"""
This python script is used to plot the average number of images and videos per tweet for original diplomats tweets as well as tweets retweeted by diplomats.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mtpl
import matplotlib.dates as mdates
import os



mtpl.rcParams['font.family'] = 'serif'
mtpl.rcParams['figure.titlesize'] = 20
mtpl.rcParams['axes.labelsize'] = 14
mtpl.rcParams['xtick.labelsize'] = 10
mtpl.rcParams['ytick.labelsize'] = 10
mtpl.rcParams['legend.fontsize'] = 10
mtpl.rcParams['figure.dpi'] = 300

date_form = mdates.DateFormatter("%b-%Y")

palette = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]


def plot_number_of_media_per_day(df, no_rt, figsize=(10, 10), media_type = 'photo', lang = None):
    '''Plots the number of tweets per day'''
    if lang != None:
        df = df[df['lang']==lang]
        no_rt = no_rt[no_rt['lang']==lang]

    no_rt = no_rt.groupby('created_at').mean().reset_index()
    df = df[df['retweet']=='retweeted']
    df = df.groupby('created_at').mean().reset_index()
    fig, ax = plt.subplots(1, 1, figsize=figsize)

    

    # only retweets
    ax.plot(df['created_at'], df[media_type], alpha = 0.2, color = palette[1])
    gaussian = df[media_type].rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
    if lang == None:
        ax.plot(df['created_at'], gaussian, color = palette[1], alpha=1, label = 'Retweeted by diplomats (all languages)')
    else:
        ax.plot(df['created_at'], gaussian, color = palette[1], alpha=1, label = f'Retweeted by diplomats ({lang})')
    # only original
    ax.plot(no_rt['created_at'], no_rt[media_type], alpha = 0.2, color = palette[2])
    gaussian = no_rt[media_type].rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
    if lang == None:
        ax.plot(no_rt['created_at'], gaussian, color = palette[2], alpha=1, label = 'All original diplomat tweets (all languages)')
    else: 
        ax.plot(no_rt['created_at'], gaussian, color = palette[2], alpha=1, label = f'All original diplomat tweets ({lang})')



    ax.legend()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(date_form)

    ax.set_ylabel(f'Average number of {media_type}s per tweet')
    # turn xticks 90 degrees
    plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
    if lang == None:
        plt.savefig(os.path.join('figs', f'avg_{media_type}s.png'))
    else: 
        plt.savefig(os.path.join('figs', f'avg_{media_type}s_{lang}.png'))
    plt.close()


if __name__ == '__main__':
    df = pd.read_csv('media_info.csv')
    df = df[df['category'] != 'Media']
    df['created_at'] = pd.to_datetime(df['created_at'], format = '%Y-%m-%d')
    df = df.sort_values(by='created_at')
    df_no_rt = df[df['retweet'] != 'retweeted']

    plot_number_of_media_per_day(df, df_no_rt)
    plot_number_of_media_per_day(df, df_no_rt, media_type = 'video')
    plot_number_of_media_per_day(df, df_no_rt, lang = 'en')
    plot_number_of_media_per_day(df, df_no_rt, media_type = 'video', lang = 'en')
