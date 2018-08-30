from os.path import join

from .vars import STORAGE_PATH


def save_plot(plt, folder, name):
    plt.savefig(join(STORAGE_PATH, 'images', folder, '{}.png'.format(name)))
    plt.close()

def save_weights(df, name):
    df.to_pickle(join(STORAGE_PATH, 'portfolios', 'weights', '{}.p'.format(name)))

def save_strategy(df, name):
    #ensure_latest(df=df)
    df.to_pickle(join(STORAGE_PATH, 'strategies', '{}.p'.format(name)))

def save_indicator(df, name):
    #ensure_latest(df=df)
    df.to_pickle(join(STORAGE_PATH, 'indicators', '{}.p'.format(name)))

def save_port(data, name):
    ''' Helper for saving portfolios.'''
    ensure_latest(df=data)
    data.to_pickle(join(STORAGE_PATH, 'portfolios', '{}.p'.format(name)))
