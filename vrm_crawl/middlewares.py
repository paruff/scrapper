"""Scrapy Middleware definitions.

Future: Custom middleware for request/response processing.
"""

from scrapy import signals


class VrmCrawlSpiderMiddleware:
    """Placeholder spider middleware."""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        yield from result

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        yield from start_requests

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class VrmCrawlDownloaderMiddleware:
    """Placeholder downloader middleware."""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
