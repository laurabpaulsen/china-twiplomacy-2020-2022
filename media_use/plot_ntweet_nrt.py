"""
Plots the number of tweets and retweets per day (for all tweets with images, all tweets with videos, and all tweets without images and videos).

This is done for all languages, as well as only for English tweets.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import os


mpl.rcParams['font.family'] = 'DejaVu Serif'
locator = mdates.MonthLocator()  # every month
date_form = mdates.DateFormatter("%b-%Y")

def return_counts(data, measure):
    """
    Returns the number of tweets or retweets per day.
    """
    if measure == 'tweets':
        counts = data['created_at'].groupby(data['created_at']).count()
    elif measure == 'retweets':
        # sum the number of retweets per day
        counts = data['retweet_count'].groupby(data['created_at']).sum()
    
    return counts

def plot_ax(tweets, ax, measure):
    """
    Plots the number of tweets or retweets per day.
    """

    # get the counts per day (either tweets or retweets)
    counts = return_counts(tweets, measure)
    
    # plot the values
    ax.plot(counts.index, counts.values, linewidth = 1, alpha = 0.5)

    # plot a smoothed version of the data
    gaussian = counts.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 10)
    ax.plot(counts.index, gaussian, alpha=1, linewidth = 1, color = 'darkblue')

    # dates on the x-axis
    ax.xaxis_date()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(date_form)

    # turn the labels on the x-axis 180 degrees and remove every second one
    for i, label in enumerate(ax.xaxis.get_ticklabels()):
        label.set_rotation(90)
        if i % 2 == 0:
            label.set_visible(False)

    return ax


def plot_joy_anger(data, ax):
    
    joy = df.groupby(['created_at'])['joy'].mean()
    anger = df.groupby(['created_at'])['anger'].mean()
    
    # plot the values
    ## joy
    ax.plot(joy.index, joy.values, linewidth = 1, alpha = 0.4, color = 'green')
    gaussian = joy.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 10)
    ax.plot(joy.index, gaussian, alpha=1, linewidth = 1, color = 'darkgreen')
    
    ## anger
    ax.plot(anger.index, anger.values, linewidth = 1, alpha = 0.4, color = 'red')
    gaussian = anger.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 10)
    ax.plot(anger.index, gaussian, alpha=1, linewidth = 1, color = 'darkred')
    

    # dates on the x-axis
    ax.xaxis_date()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(date_form)

    # turn the labels on the x-axis 180 degrees and remove every second one
    for i, label in enumerate(ax.xaxis.get_ticklabels()):
        label.set_rotation(90)
        if i % 2 == 0:
            label.set_visible(False)

    return ax

def plot_all(data_list, title_list, lang = 'all'):
    counter = -1
    fig, axs = plt.subplots(3, 3, figsize = (20, 10), sharex=True, sharey="row")
    
    for data in data_list:
        if lang != 'all': # only keep the data for the specified language
            data = data[data['lang'] == lang]
        
        # plot seperate plots for each category
        # add to the all in one plot
        counter += 1

        axs[0, counter] = plot_ax(data, axs[0, counter], measure = 'tweets')
        axs[1, counter] = plot_ax(data, axs[1, counter], measure = 'retweets')
        axs[2, counter] = plot_joy_anger(data, axs[2, counter])

    # set the titles of the plots
    for i, title in enumerate(title_list):
        axs[0, i].set_title(title, size = 15)

    axs[0, 0].set_ylabel('Number of tweets', size = 15)
    axs[1, 0].set_ylabel('Number of retweets', size = 15)

    # add a x-axis label to the whole figure
    fig.supxlabel('Date', size = 15)

    # prep title depending on language
    if lang == 'all':
        lang_info = 'all languages'
    else:
        lang_info = lang

    fig.suptitle(f'Original diplomat tweets ({lang_info})', size = 20)
    
    plt.tight_layout()
    plt.savefig(os.path.join('figs', f'orig_diplomat_tweets_rt_ntweets_time_{lang}.png'))




if __name__ == '__main__':
    # read in the data
    df = pd.read_csv('media_info.csv')
    emo = pd.read_csv(os.path.join('..', 'emotion_classification', 'data', 'emotion_diplomat_data.csv'), usecols = ['tweetID', 'joy', 'love', 'anger', 'sadness', 'fear', 'surprise'])
    print(len(emo['tweetID']))
    print(len(df['tweetID']))
    df = pd.merge(df, emo, how="inner", on = "tweetID")
    print(len(df['tweetID']))


    # merge

    # date time format
    df['created_at'] = pd.to_datetime(df['created_at'], format = '%Y-%m-%d')
    
    # only original diplomat tweets
    diplo_all = df[df['category'] == 'Diplomat'] 
    diplo_orig = diplo_all[diplo_all['retweet'] != 'retweeted']

    # only tweets with photos, videos, or neither
    diplo_orig_photos = diplo_orig[diplo_orig['photo'] != 0]
    diplo_orig_videos = diplo_orig[diplo_orig['video'] != 0]
    diplo_orig_text = diplo_orig.query('photo == 0 & video == 0')

    # all languages
    data_list = [diplo_orig_photos, diplo_orig_videos, diplo_orig_text]
    title_list = ['Tweets with photos', 'Tweets with videos', 'Tweets without photos or videos']
    plot_all(data_list, title_list, lang = 'all')

    # only English
    plot_all(data_list, title_list, lang = 'en')


    