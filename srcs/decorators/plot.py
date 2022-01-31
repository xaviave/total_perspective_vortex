import inspect
import logging
import functools

import matplotlib.pyplot as plt

# from matplotlib.animation import PillowWriter


def plot_meta_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = inspect.signature(func).bind(*args, **kwargs)
        bound.apply_defaults()
        bound = dict(bound.arguments)
        fig = func(*args, **kwargs)
        if bound.get("save_fig", False):
            f = bound["plot_filename"]
            logging.info(f"Saving in {f}")
            if f.endswith(".mp4"):
                fig.save(f)
            else:
                plt.savefig(f)
        if bound.get("show", False):
            plt.show()
        try:
            plt.close(fig)
        except TypeError:
            # if FuncAnimation class
            pass

    return wrapper
