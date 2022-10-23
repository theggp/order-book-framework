import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from dataclasses import dataclass
@dataclass
class BookOrder:
    price: float
    size: float


def NewOrderBook(data=None):
    ob_columns = ['price', 'size', 'type']

    if data:
        orderBook = pd.DataFrame(data, columns=ob_columns)
        orderBook = SortOrderBook(orderBook)
    else:
        orderBook = pd.DataFrame(columns=ob_columns)

    return orderBook

def SortOrderBook(orderBook: pd.DataFrame):

    return orderBook.sort_values('price', ascending=False).reset_index(drop=True)


class OrderBookManager:

    def __init__(self):

        self.minPriceMul = 0.85
        self.maxPriceMul = 1.15

        # default number of orders in the book
        self.defaultOrderQuantity = 1000
        self.clustersAmount = 6

        # sampling probability
        self.uniformP = 0.4
        self.clusterP = 1-self.uniformP

        # distributions parameters
        self.initialized = False
        self.clusters = None

    def get_order_ranges(self, price):
        min_price = price*self.minPriceMul
        max_price = price*self.maxPriceMul
        return min_price, max_price


    def initalize_distributions(self, price):

        min_price, max_price = self.get_order_ranges(price)
        clusters = np.random.uniform(min_price*1.05, max_price*0.95, self.clustersAmount)
        self.initialized = True
        self.clusters = clusters

    def fillBook(self, price, maxLiquidity, averageOrderSize=None, orderBook=pd.DataFrame()):

        if not averageOrderSize:
            averageOrderSize = maxLiquidity/self.defaultOrderQuantity
        assert averageOrderSize < maxLiquidity

        if not self.initialized:
            self.initalize_distributions(price)

        if orderBook.empty:
            currentLiquidity = 0
        else:
            currentLiquidity = orderBook.sum()['size']

        min_price, max_price = self.get_order_ranges(price)
        orders = []
        while currentLiquidity < maxLiquidity:

            # todo: update to truncated normal distribution using scipy
            sampleVolume = averageOrderSize * np.random.uniform(0.5, 1.5)

            if (np.random.uniform() < self.uniformP):
                samplePrice = np.random.uniform(min_price, max_price)
            else:
                samplePrice = np.random.choice(self.clusters) * np.random.uniform(0.995, 1.005)

            orders.append([samplePrice, sampleVolume, None])
            currentLiquidity += sampleVolume

        newOrderBook = NewOrderBook(orders)

        # print("new order book size is " + str(newOrderBook.shape))

        if not orderBook.empty:
            newOrderBook = SortOrderBook(pd.concat([orderBook, newOrderBook]))

        return newOrderBook

    def executeFills(self, orderBook, p0, p1):
        executedOrders = orderBook.loc[(orderBook['price'] < max(p0,p1)) & (orderBook['price'] > min(p0,p1))]
        orderBook = orderBook.drop(executedOrders.index)
        orderBook = orderBook.reset_index(drop=True)
        return orderBook

    def plot_book(self, orderBooks, prices):

        num_bins = 200
        min_price, max_price = self.get_order_ranges(prices[0])
        bins0 = pd.interval_range(start=min_price, freq=(max_price-min_price)/num_bins, end=max_price)

        books_data = []
        for book in orderBooks:

            # executedOrders = book.loc[(book['price'] < 22) & (book['price'] > 18)]
            # book = book.drop(executedOrders.index)

            book['bins'] = pd.cut(book['price'], bins=bins0)
            binBook = book.groupby('bins').sum()
            books_data.append([binBook['size'].values])

        data = np.concatenate(books_data).transpose()
        xgrid = np.arange(len(orderBooks))
        ygrid = [i.mid for i in binBook.index]

        fig, ax = plt.subplots()
        ax.pcolormesh(xgrid, ygrid, data)
        ax.set_frame_on(False)  # remove all spines

        plt.plot(prices, 'red')
        ax.set_ylabel('Price')
        ax.set_xlabel('Time')
        plt.show()



if __name__ == '__main__':

    OB = OrderBookManager()

    initial_liquidity = 10000
    liquidity_growth = 150

    price_i = 20
    daily_vol = 0.015
    price = price_i


    book = OB.fillBook(price_i, initial_liquidity)


    prices = []
    prices.append(price_i)

    books = []
    books.append(book)

    for i in range(30):
        price = price * (1 + np.random.normal(0, daily_vol))
        prices.append(price)

        book = OB.fillBook(price_i, initial_liquidity + (i*1) * liquidity_growth, orderBook=book)

        # simulating order fills for orders hit by the price
        book = OB.executeFills(book, prices[-2], prices[-1])

        books.append(book)

        # reset book clusters, test
        if i == 10:
            OB.initalize_distributions(price_i)
            initial_liquidity = initial_liquidity*1.1

    OB.plot_book(books, prices)