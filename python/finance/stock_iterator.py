#!/usr/bin/python
'''
  usage:  ./stock_iterator.py --stock=TICKER
  Given a file of ticker data in TICKER_history.csv, the program calculates a the volatility for a sliding window using a stocks change in closing prices.  Each days change in stock price is expressed in terms of the sliding window standard deviations.  Finally, the stock price, corresponding volatility, and days change in terms of standard deviations are graphed with matplotlib.
'''
import scipy
import numpy
import math
import time
import optparse
#from optparse import OptionParser
import re
import matplotlib.pyplot


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


class StockArray(object):
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self, start_p, end_p, volume, time_o):
        self._registry.append(self)
        self.start_price = start_p
        self.volume      = start_p
        self.end_price   = end_p
        self.price_change= 0
        self.time        = time_o
        self.std_dev     = 0
        self.mean        = 0
        self.spike       = 0

    def get_length(self):
        return(len._registry)

    @classmethod
    def run_cc_window_calculation(self):
        current_offset = 0
        step = 1
        win_size = 20
        sum_start_px = 0
        previous_close = 0
        array_of_close_close_log_changes = []
        for stock_object in StockArray:
            if previous_close != 0:
                array_of_close_close_log_changes.append(math.log(stock_object.end_price/previous_close))
                stock_object.price_change = stock_object.end_price - previous_close
            previous_close=stock_object.end_price

        numChunks = (( len(array_of_close_close_log_changes) - win_size)/ step )+1
        for i in range(0,numChunks,step):
            sliding_window_cc = array_of_close_close_log_changes[i:i+win_size]
            m = scipy.mean(sliding_window_cc)
            s = scipy.std(sliding_window_cc)
            self._registry[i+win_size].std_dev = s
            self._registry[i+win_size].mean    = m
            if not self._registry[i+win_size-1].price_change == 0 and not self._registry[i+win_size-1].std_dev == 0:
              self._registry[i+win_size].spike = self._registry[i+win_size].price_change / ( self._registry[i+win_size-1].std_dev * self._registry[i+win_size-1].end_price )




def run_it():
    parser = optparse.OptionParser(usage='usage: %prog <stock name>')
    parser.add_option('-s','--stock', action='store', type='string', help='Stock Ticker', dest='stock_name')
    (options, args) = parser.parse_args()
    stock_name = options.stock_name
    if stock_name == None:
        parser.print_help()
        exit(2)

    stock_csv = stock_name + '_history.csv'
    fh = open(stock_csv)
    stock_lines = fh.readlines()
    fh.close


    for line in stock_lines:
        if re.search("^\#", line):
            pass
        elif re.search("^\w", line):
            date, open_px, high, low, close_px, volume = line.split(',')
            float_open = float(open_px)
            float_close = float(close_px)
            float_volume = float(volume)
            time_obj = time.strptime(date, "%Y%m%d")
            StockArray(float_open,float_close,float_volume,time_obj)
        else:
            pass


    StockArray.run_cc_window_calculation()
    x_count = []
    y_spike = []
    x_log_dev = []
    y_log_dev = []
    y_stock_price = []
    yesterdays_price = 1
    count  = 0

    for stock_object in StockArray:
        if stock_object.std_dev == 0:
            continue
        x_count.append( count )
        y_spike.append( stock_object.spike )
        y_log_dev.append( stock_object.std_dev )
        y_stock_price.append( stock_object.end_price )
        yesterdays_price = stock_object.end_price
        count += 1

    matplotlib.pyplot.figure(1)
    ax1 = matplotlib.pyplot.subplot(311)
    matplotlib.pyplot.bar(x_count, y_spike)
    matplotlib.pyplot.title("Spike Chart for " + stock_name )
    matplotlib.pyplot.xlabel("day")
    matplotlib.pyplot.ylabel("change in std dev")
    matplotlib.pyplot.subplot(312, sharex = ax1)
    matplotlib.pyplot.plot(x_count, y_log_dev, 'b-')
    matplotlib.pyplot.title("")
    matplotlib.pyplot.xlabel("day")
    matplotlib.pyplot.ylabel("volatility")
    matplotlib.pyplot.subplot(313, sharex = ax1)
    matplotlib.pyplot.plot(x_count, y_stock_price, 'b-')
    matplotlib.pyplot.title("")
    matplotlib.pyplot.xlabel("day")
    matplotlib.pyplot.ylabel("stock price")
    matplotlib.pyplot.show()


if __name__ == '__main__':
    run_it()


