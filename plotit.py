
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

__doc__="""Plotter for UCR crime stats.
         Data at
https://www.ucrdatatool.gov/Search/Crime/State/TrendsInOneVar.cfm
"""

default_file = 'violent_total.csv'
summary_columns = set(['ViolentCrimeRate'])

class Plotter:

   def __init__(self, filename):
      self.filename = filename
      self.data = pd.DataFrame.from_csv(self.filename, parse_dates=False)

   def make_comb_plot(self):
      fig, ax = plt.subplots()
      sum_data = self.data.cumsum(1)
      if sum_data.columns[-1] in summary_columns:
         sum_data = sum_data[sum_data.columns[:-1]]

      idx = sum_data.index
      for ii, column in enumerate(sum_data.columns):
         if ii==0:
            below = np.zeros(len(sum_data))
         else:
            below = sum_data[sum_data.columns[ii-1]]

         ax.fill_between(idx, below, sum_data[column], label=column.replace('Rate', ''))

      plt.legend(loc='best', frameon=False)
      plt.title("Rate per 100K", size='small')
      return fig

   def make_multi_plot(self):
      fig, axes = plt.subplots(nrows=self.data.shape[1], sharex=True, figsize=(6,8))
      plt.subplots_adjust(hspace=0.0, top=0.95)
      for ax, col in zip(axes, self.data.columns):
         ax.plot(self.data.index, self.data[col])

      # Prettify
      for ii, ax in enumerate(axes):
         ax.set_ylabel(self.data.columns[ii].replace('Rate',''), size='small')
         ax.get_xaxis().set_tick_params(direction='in')
         ax.get_xaxis().set_ticks_position('both')

      axes[0].set_title("Rate per 100K", size='small')
      return fig


def main():

   import argparse
   parser = argparse.ArgumentParser(description=__doc__)
   parser.add_argument('-f', '--filename', default=default_file,
                           help="CSV file to load. default: %(default)s")
   parser.add_argument('-n', '--no_show', default=False, action='store_true',
                     help="Do not show plot.")
   parser.add_argument('-s', '--save-comb-file', help="Save combined plot to this file.")
   parser.add_argument('-S', '--save-multi-file', help="Save multi_plot to this file.")

   args = parser.parse_args()

   plotter = Plotter(args.filename)
   fig1 = plotter.make_comb_plot()
   fig2 = plotter.make_multi_plot()

   if not args.no_show:
      plt.show()
   if args.save_comb_file:
      fig1.savefig(args.save_comb_file)
   if args.save_multi_file:
      fig2.savefig(args.save_multi_file)


if __name__=='__main__':
   main()

