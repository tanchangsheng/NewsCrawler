import scrapy


class TodaySpider(scrapy.Spider):
    name = "today"

    start_urls = [
        'http://www.todayonline.com/singapore'
    ]

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = 'today_html/sgnews-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
    
        next_page = response.css('li.pager-next a::attr(href)').extract_first()
        if next_page is not None:
            page_num = next_page.split()[-1]
            if page_num == "5":
                return
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)