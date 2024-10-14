import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import propagation
import investmentclasses

def plot_value_history(portfolio: 'propagation.Simulation_trace'):
    hist = np.array(portfolio.portfolio_history).T
    plt.figure()
    plt.plot(hist[0], hist[1:].sum(axis=0), label='Total value')
    plt.plot(hist[0], hist[1], label='Cash')
    for counter, asset in enumerate(portfolio.assets):
        plt.plot(hist[0], hist[counter + 2], label=asset.key_name)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m.%y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Values [€]', fontsize=14)
    plt.legend()
    plt.gcf().autofmt_xdate()

    plt.show()

def plot_deviation_history(portfolio: 'propagation.Simulation_trace'):
    hist = np.array(portfolio.portfolio_history).T
    dates = hist[0]
    total_value = hist[1:].sum(axis=0)

    plt.figure()
    asset: 'investmentclasses.Investment'
    for counter, asset in enumerate(portfolio.assets):
        deviation = hist[counter + 2]/(total_value*asset.target_ratio)*100
        plt.plot(dates[1:], deviation[1:], label=asset.key_name)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m.%y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Deviation [%]', fontsize=14)
    plt.legend()
    plt.gcf().autofmt_xdate()

    plt.show()


def plot_1D_metrics(variation, variation_range, metric_values):
    fig, axes = plt.subplots(1,2, figsize = (8,3))
    for counter, ax in enumerate(axes):
        ax.plot(variation_range, metric_values[counter], 'o')
        ax.set_xscale(variation[3])
        ax.set_xlabel(variation[4])
    axes[0].set_ylabel('IRR')
    axes[1].set_ylabel('Costs')
    fig.savefig('test.pdf', bbox_inches='tight')
    plt.show()


#ideas:
# deposit size over lost costs
# length of rebalancing
# deviation threshold


def plot_return_over_2d_variable_variation(self):
    ...