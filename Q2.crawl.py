import requests, lxml.html, time

THRESHOLD = 100
urls = []  # keep all urls we have detected
crawled = []  # keep all urls have been crawled
urls_pairs_list = []  # final list of lists(pairs)
# _xpaths = ["//table/tbody/tr/td[count(../../tr/th[contains(text(),'Opponent')]/preceding-sibling::*)+1=position() and count(../../tr/th[contains(text(),'Opponent')]/preceding-sibling::*)>0 ]//a[not (img) and contains(@href,'wiki')]/@href", "//table/tbody/tr/td[count(../../tr/th[contains(text(),'Partner')]/preceding-sibling::*)+1=position() and count(../../tr/th[contains(text(),'Partner')]/preceding-sibling::*)>0 ]//a[not (img) and contains(@href,'wiki')]/@href", "//table//td[../th[contains(text(),'Coach')]]//a[not (img) and contains(@href,'wiki')]/@href", "//table/tbody/tr/td[count(../../tr/td[b[contains(text(),'Opponent')]]/preceding-sibling::*)+1=position() and count(../../tr/td[b[contains(text(),'Opponent')]]/preceding-sibling::*)>0 ]//a[not (img) and contains(@href,'wiki')]/@href", "//table/tbody/tr/td[count(../../tr/td[b[contains(text(),'Partner')]]/preceding-sibling::*)+1=position() and count(../../tr/td[b[contains(text(),'Partner')]]/preceding-sibling::*)>0 ]//a[not (img) and contains(@href,'wiki')]/@href"]


class URL:
    def __init__(self, url, priority):
        self.link = url
        self.priority = priority


# given url , check if we detect it before
def is_in_urls(url):
    for u in urls:
        if u.link == url:
            return True
    return False


# given url , increment it's priority by 1
def increment_priority(url):
    for u in urls:
        if u.link == url:
            u.priority += 1
            break


# from all the urls , return the one with highest priority
def get_max_priority():
    max_p = urls[0]  # initial value
    for u in urls:
        # we don't need to crawl crawled urls
        if u.priority >= max_p.priority and u.link not in crawled:
            max_p = u
    if max_p in crawled:
        return None
    else:
        return max_p.link


# given url , remove it from urls list .(in case of exception)
def remove_url(url):
    for u in urls:
        if u.link == url:
            urls.remove(u)


# given url , crawl this page according to queries in xpaths list
def crawl(url, xpaths):
    if len(crawled) == THRESHOLD:
        return urls_pairs_list
    page = requests.get(url)
    doc = lxml.html.fromstring(page.content)
    page_urls = []  # keeps urls detected in this page, to avoid duplicates
    crawled.append(url)
    for query in xpaths:
        for current_url in doc.xpath(query):
            if not current_url.startswith('/wiki/'):  # just wiki urls
                continue
            current_url = "https://en.wikipedia.org" + current_url  # concatenate wiki prefix
            if current_url in page_urls:  # if detected in page before , just increment priority
                increment_priority(current_url)
                continue
            page_urls.append(current_url)
            urls_pairs_list.append([url, current_url])  # src, dst
            if not is_in_urls(current_url):  # first detection
                urls.append(URL(current_url, 1))
            else:  # detected before
                increment_priority(current_url)
    while len(urls) > 0:
        high_priority = get_max_priority()
        try:
            if high_priority is None:  # mean all urls have been crawled
                return urls_pairs_list
            time.sleep(3)  # ethics
            return crawl(high_priority, xpaths)  # recursion on high priority url
        except:
            remove_url(high_priority)  # in case of error in url
            pass


#result = crawl("https://en.wikipedia.org/wiki/Andy_Ram", _xpaths)
#for r in result:
#    print(r)
#print(len(result))
