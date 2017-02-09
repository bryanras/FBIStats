

import pandas as pd

__doc__="""File combiner. """

def main():

   import argparse
   parser = argparse.ArgumentParser(description=__doc__)
   parser.add_argument('load_file', nargs='+', help="Space-separated list of files to load.")
   parser.add_argument('write_file', help="File to write.")
   args = parser.parse_args()

   data = pd.DataFrame.from_csv(args.load_file[0], parse_dates=False)
   for filename in args.load_file[1:]:
      new_data = pd.DataFrame.from_csv(filename, parse_dates=False)
      for column in new_data:
         data[column] = new_data[column]


   data.index.name = 'year'
   data.to_csv(args.write_file)


if __name__=='__main__':
   main()

