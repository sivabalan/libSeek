from Crawler4py.Crawler import Crawler
from GitHubConfig import GitHubConfig

crawler = Crawler(GitHubConfig())

print (crawler.StartCrawling())

exit(0)