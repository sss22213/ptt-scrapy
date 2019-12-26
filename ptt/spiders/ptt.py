import scrapy
from scrapy.http import FormRequest
from ptt.items import PostItem

class pttspider(scrapy.Spider):
    name = 'ptt'
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html',]
    _page = 0
    _page_total = 100

    def parse(self,response):
        # 18 old check
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:
            yield FormRequest.from_response(response,formdata = {"yes":"yes"},callback=self.parse)
        else:
            self._page = self._page + 1
            # This page
            for sub_url in response.css('div.r-ent > div.title > a::attr(href)'):
                url = response.urljoin(sub_url.get())
                yield scrapy.Request(url, callback=self.parse_post)
            # Next page
            if self._page < self._page_total:
                print("Next Page")
                url_no = response.xpath('//div[@id="action-bar-container"]//div[@class="action-bar"]//div[@class="btn-group btn-group-paging"]//a[contains(text(), "上頁")]/@href')
                url = response.urljoin(url_no.get())
                yield scrapy.Request(url, callback=self.parse)

    def parse_post(self, response):
        body = PostItem()
        body['title'] = response.xpath('//meta[@property="og:title"]//@content').get()
        body['author'] = response.xpath('//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span[1]/text()').get().split(' ')[0]
        body['nickname'] = response.xpath('//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span[1]/text()').get().split(' ')[1]
        body['date'] = response.xpath('//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()').get()
        body['content'] = response.xpath('//div[@id="main-content"]/text()').get()
        body['ip'] = response.xpath('//span[@class="f2"]/text()').get()[27:]
        # get comments
        comments = []
        for comment in response.xpath('//div[@class="push"]'):
            content = comment.css('span.push-content::text').get()[2:]
            user = comment.css('span.push-userid::text').get()
            tag = comment.css('span.push-tag::text').get()
            user_ip = comment.css('span.push-ipdatetime::text').get()
            comments.append({"user":user,"tag":tag,"content":content,"user_ip":user_ip})
            # print(comment)
        body['comments'] = comments
        body['url'] = response.url
        # print(body)
        # body['date'] = response.xpath('//span[@class="article-meta-value"]/text()').get()
        yield body
        # print(response.xpath('//meta[@property="og:title"]//@content').get())