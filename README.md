#  crawling pages of tennis players in Wikipedia
> Q2.crawl.py
```python
crawl(url, xpaths)
```
this function take two parameters , url and xpaths
* url : string containing the URL of the start page of tennis player
* xpaths : list of strings representing legal **XPath** expressions
<br>
- The function will use the xpaths to extract a set of URLs from the web page. <br>
- These URLs will also be crawled in order of priority:<br>
&nbsp;&nbsp;1. Keep counts for the number of times each URL was found. URLs seen the highest
number of times have the highest priority.<br>
&nbsp;&nbsp;2. Break ties as you choose.<br>
-crawling ethics :wait at least 3 seconds between page reads.<br>
-In total, at most 100 URLs will be crawled in this manner.<br>
-The function will return a list of lists. Each inner list will contain two strings: the first will be the
-full source URL, and the second will be the full URL of a page detected in the source URL by the crawler

### How to extract URLs of tennis player from current tennis player's wikipedia page ?

in wikipedia, each page of tennis players has a table of Matches he participated in , which have
a column of _'partner'_ and _'opponents'_ , so we can , by xpath queries, extract these urls <br><br>
<img width="613"  src="https://user-images.githubusercontent.com/69496372/89895130-edafc500-dbe3-11ea-9846-8b4fcf429cb6.png">

list of useful xpath queries: <br>
```xpaths
_xpaths = ["//table/tbody/tr/td[count(../../tr/th[contains(text(),'Opponent')]/preceding-sibling::*)+1=position() and count(../../tr/th[contains(text(),'Opponent')]/preceding-sibling::*)>0 ]//a[not (img) and contains(@href,'wiki')]/@href", "//table/tbody/tr/td[count(../../tr/th[contains(text(),'Partner')]/preceding-sibling::*)+1=position() and count(../../tr/th[contains(text(),'Partner')]/preceding-sibling::*)>0 ]//a[not (img) and contains(@href,'wiki')]/@href", "//table//td[../th[contains(text(),'Coach')]]//a[not (img) and contains(@href,'wiki')]/@href", "//table/tbody/tr/td[count(../../tr/td[b[contains(text(),'Opponent')]]/preceding-sibling::*)+1=position() and count(../../tr/td[b[contains(text(),'Opponent')]]/preceding-sibling::*)>0 ]//a[not (img) and contains(@href,'wiki')]/@href", "//table/tbody/tr/td[count(../../tr/td[b[contains(text(),'Partner')]]/preceding-sibling::*)+1=position() and count(../../tr/td[b[contains(text(),'Partner')]]/preceding-sibling::*)>0 ]//a[not (img) and contains(@href,'wiki')]/@href"]```
