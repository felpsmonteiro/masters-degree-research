import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def line_plot(x, ys, path=None, line_legends=None, legend_path=None, 
              xlabel=None, ylabel=None, title=None, xlog=False, ylog=False,
              linestyles = [':', 'dashed', ':', '--', '-.', 'dashed'],          
              colors = ['#360CE8', '#4ECE00', '#faa43a', '#F01F0F', '#AF10E0'],
              markers = ['d','|','o','v','d','1'],
              figsize=(5, 5),
              ylim=None):

    fig, ax = plt.subplots(figsize=figsize, tight_layout=True)

    if markers is None:
        markers = ["None"]*len(ys)

    if linestyles is None:
        linestyles = ['-']*len(ys)
    
    if line_legends is None:
        line_legends = [None]*len(ys)
    
    lines = []
    for i,y in enumerate(ys):    
        lines.append(
            ax.plot(x, y, 
                linestyle=linestyles[i],
                linewidth=1.5, 
                color=colors[i],
                label=line_legends[i],
                marker=markers[i],
                markersize=4
                # alpha=0.5
            )
        )

    plt.legend()
    if ylog:
        plt.yscale('log')
    # if xlog:
        # plt.xscale('log')    
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    if title:
        ax.set_title(title)
    if ylim is not None:
        ax.set_ylim(ylim)
    ax.grid(True)
    
    if path:
        dir_path = os.path.dirname(os.path.realpath(path))
        os.makedirs(dir_path, exist_ok=True)
        plt.savefig(path, dpi=300)
        print('Graphic saved at: ' + path)
    else:
        plt.show()
    plt.clf()
    plt.close()

def plot_line_graph(data=None, x=None, y=None, hue=None, style=None,
                    title=None, xlabel=None, ylabel=None, filename=None,
                    yscale='linear', save_path='.', dpi=300, figsize=(5,5)):
    
    sns.set_theme(style="darkgrid")
    graph = sns.lineplot(data=df, x=x_col, y=y_col, hue=legend_col, style=legend_col, err_style='band', markers=True, dashes=False)
    graph.set_title(title)
    graph.set_xlabel(xlabel)
    graph.set_ylabel(ylabel)
    graph.set_yscale(yscale)
    fig = graph.get_figure()
    fig.savefig(f"{save_path}/{filename}")