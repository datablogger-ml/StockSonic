import matplotlib.pyplot as plt


def chart_rsi(title, df):
    """

    :param title:
    :param df:
    :return:
    """
    fig, ax = plt.subplots()
    ax.set_title(title)
    fig.subplots_adjust(bottom=0.2)
    ax.plot(df['Date'], df['RSI'])
    ax.set_ylim(0, 100)
    ax.axhline(y=70, color='r', linestyle='-')
    ax.axhline(y=30, color='r', linestyle='-')
    ax.grid(True)
    ax.set_ylabel(r'RSI')
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
    plt.show()
