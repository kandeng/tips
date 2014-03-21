# -*- coding: utf-8 -*-
import re
#import chardet
import lxml.html
import sys

import requests
## import urllib
## Replace urllib with requests, for better efficiency.

########################################################################################################################

class ExtractorSuper:
    ## Using the super class to unify the __init__ of the descendant classes
    def __init__(self, address):
        # data = urllib.urlopen(address).read()
        # self.tree = lxml.html.fromstring(data)

        ## Replace urllib with requests, for better efficiency.
        ## Also reinforce the utf-8 decode/encode.
        reload(sys)
        sys.setdefaultencoding('utf-8')

        data = requests.get(address)
        datautf8 = data.text.decode('utf-8')
        self.tree = lxml.html.fromstring(datautf8)


class ExtractorCategory(ExtractorSuper):
    """
    def __init__(self, address):
        data = urllib.urlopen(address).read()
        self.tree = lxml.html.fromstring(data)
    """

    def extractor_category(self, index1, index2):
        # a = tree.xpath('//li[@class="menuItem"][2]//a')
        h1 = self.tree.xpath('//li[@class="menuItem"][%d]//h3/text()'%index1)
        print '//li[@class="menuItem"][%d]//h3/text()'%index1, ">> ", h1[0].encode('utf8')

        h2 = self.tree.xpath('//li[@class="menuItem"][%d]//div[@class="subView-cate clearfix"][%d]//h4/a/text()'%(index1, index2))
        print '//li[@class="menuItem"][%d]//div[@class="subView-cate clearfix"][%d]//h4/a/text()'%(index1, index2), ">> ", h2[0].encode('utf8')

        links = self.tree.xpath('//li[@class="menuItem"][%d]//div[@class="subView-cate clearfix"][%d]//p/a'%(index1, index2))
        for i in links:
            print " >> links: ", i.items(), i.text.encode('utf-8')
            if i.values()[0].find('http://list.tmall.com/') != -1:
                print i.items(), i.text.encode('utf-8')


class ExtractorShop(ExtractorSuper):
    """
    def __init__(self, address):
        data = urllib.urlopen(address).read()
        self.tree = lxml.html.fromstring(data)
    """

    def extractor_shop(self, index):
        a = self.tree.xpath('//div[@class="shopHeader-info"][%d]/a'%index)
        print a[0].items(), a[0].text.encode('utf8')


class ExtractorItems(ExtractorSuper):
    """
    def __init__(self, address):
        data = urllib.urlopen(address).read()
        self.tree = lxml.html.fromstring(data)
    """

    def extractor_items(self, index):
        a = self.tree.xpath('//p[@class="productTitle"][%d]/a'%index)
        print a[0].items(), a[0].text.encode('utf8')




if __name__ == "__main__":

    print "-" * 80
    address = "http://mei.tmall.com/?spm=3.7095809.2000a021.1.e7d0Ef"
    ex = ExtractorCategory(address)
    ex.extractor_category(2, 1)
    ## Well done, get the names of the first-level and second-level category
    ## Todo: format the output.

    print "-" * 80
    address = "http://list.tmall.com/search_product.htm?cat=50029232&style=w"
    ex = ExtractorShop(address)
    ex.extractor_shop(2)
    ## Well done, get the name of a shop, and the URL accessing to the store.
    ## In addition, need to get the URL accessing the shop's main page, referring to the tag of "进入店铺"
    ## Retrieved by the code:                     http://list.tmall.com/search_shopitem.htm?user_id=749391658&from=_1_
    ## Retrieved by clicking the name on webpage: http://list.tmall.com/search_shopitem.htm?spm=a220m.1000858.1000725.2.gCGzZ5&user_id=749391658&from=_1_
    ## Retrieved by clicking "进入店铺":           http://olay.tmall.com/shop/view_shop.htm?spm=a220m.1000858.1000725.3.gCGzZ5&user_number_id=749391658&rn=a15fdaf0d8bd273105a737d88d33dce2

    print "-" * 80

    address = 'http://list.tmall.com/search_shopitem.htm?user_id=820351386'
    ex = ExtractorItems(address)
    ex.extractor_items(2)
    ## Well done, get the name of a product, and the URL to its main page.
    ## Interestingly, the URLs to the product's main page are different. Where did the code get the URL?
    ## Retrieved by the code:           http://detail.tmall.com/item.htm?id=36899762324&is_b=1&cat_id=2&q=&rn=e947d05c2d615e7ed567c946f1466cf2
    ## Retrieved by clicking the name:  http://detail.tmall.com/item.htm?spm=a220m.1000862.1000725.7.kFiewI&id=36899762324&is_b=1&cat_id=2&q=&rn=faa9e122734610fc9c2bf6812cde4ae6
    ## Retrieved by clicking the image: http://detail.tmall.com/item.htm?spm=a220m.1000862.1000725.6.kFiewI&id=36899762324&is_b=1&cat_id=2&q=&rn=faa9e122734610fc9c2bf6812cde4ae6


