try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

import json, shelve, re, os

from Crawler4py.Config import Config

class GitHubConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.UserAgentString = "lordnahor-libseek-MSR-app"
        self.MaxWorkerThreads = 8
        self.DepthFirstTraversal = True
        self.FrontierTimeOut = 100
        self.WorkerTimeOut = 100
        self.OutBufferTimeOut = 100
        self.PolitenessDelay = 1000
        self.MaxPageSize = 1048576*5
        self.IgnoreRobotRule = True
        self.urlToNameMap = shelve.open("urlDataPersist.shelve")
    
    def GetSeeds(self):
        '''Returns the first set of urls to start crawling from'''
        seeds = []
        repoMetaData = json.load(open("../bucket2.json", "r"))
        try:
            os.mkdir("repoData")
        except OSError:
            pass
        for repo in repoMetaData:
            name = repo["full_name"].replace("/", "-")
            try:
                os.mkdir("repoData/" + name)
            except OSError:
                pass
            metaFile = open("repoData/" + name + "/metadata.json", "w")
            json.dump(repo, metaFile, sort_keys=True, indent=4, separators=(',', ': '))
            metaFile.close()
            seeds.append(repo["contents_url"][:-7])
    
        return seeds

    def HandleData(self, parsedData):
        '''Function to handle url data. Guaranteed to be Thread safe.
        parsedData = {"url" : "url", "text" : "text data from html", "html" : "raw html data"}
        Advisable to make this function light. Data can be massaged later. Storing data probably is more important'''
        downloadData = json.loads(parsedData["html"])
        if type(downloadData) is type({}) and "content" in downloadData:
            foldername = "-".join(re.match(".*repos/(.*)/(.*)/git.*", parsedData["url"]).groups())
            if parsedData["url"].encode("utf-8") not in self.urlToNameMap:
                filename = parsedData["url"].encode("utf-8")
            else:
                filename = self.urlToNameMap[parsedData["url"].encode("utf-8")]
            if "readme" in filename.lower():
                file = open("repoData/" + foldername + "/description.txt", "a")
            else:
                file = open("repoData/" + foldername + "/allPythonContent.py", "a")
            try:
                file.write("__FILENAME__ = " + (filename) + "\n" + downloadData["content"] + "\n########NEW FILE########\n")
            except UnicodeError:
                print "Error at ", filename, parsedData["url"]
            file.close()
            print ("Wrote data to " + foldername + " File: " + filename)
            if parsedData["url"].encode("utf-8") in self.urlToNameMap:
                del self.urlToNameMap[parsedData["url"].encode("utf-8")]
                self.urlToNameMap.sync()
        
    
        pass

    def AllowedSchemes(self, scheme):
        '''Function that allows the schemes/protocols in the set.'''
        return scheme.lower() in set(["http", "https", "ftp"])

    def ValidUrl(self, url):
        '''Function to determine if the url is a valid url that should be fetched or not.'''
        return True

    def GetTextData(self, htmlData):
        '''Function to clean up html raw data and get the text from it. Keep it small.
        Not thread safe, returns an object that will go into the parsedData["text"] field for HandleData function above'''
        return ""

    def ExtractNextLinks(self, url, rawData, outputLinks):
        '''Function to extract the next links to iterate over. No need to validate the links. They get validated at the ValudUrl function when added to the frontier
        Add the output links to the outputLinks parameter (has to be a list). Return Bool signifying success of extracting the links.
        rawData for url will not be stored if this function returns False. If there are no links but the rawData is still valid and has to be saved return True
        Keep this default implementation if you need all the html links from rawData'''
        downloadData = json.loads(rawData)
        if type(downloadData) is list:
            # First download file
            for file in downloadData:
                if file["type"] == "file":
                    if file["name"].endswith(".py") or "readme" in file["name"].lower():
                        if "git_url" in file:
                            outputLinks.append(file["git_url"])
                            self.urlToNameMap[file["git_url"].encode("utf-8")] = file["name"]
                            self.urlToNameMap.sync()
                elif file["type"] == "dir":
                    outputLinks.append(file["git_url"])
        else:
            # One of the recursive download files.
            if "tree" in downloadData:
                # is a folder. go recursive
                for file in downloadData["tree"]:
                    if file["type"] != "blob" or file["path"].endswith(".py") or "readme" in file["path"].lower():
                        if "url" in file:
                            outputLinks.append(file["url"])
                            if file["type"] == "blob":
                                self.urlToNameMap[file["url"].encode("utf-8")] = file["path"]
                                self.urlToNameMap.sync()
                # if a blob file, dont bother with doing anything. can be processed right away.
        return True

    def GetAuthenticationData(self):
        ''' Function that returns dict(top_level_url : tuple(username, password)) for basic authentication purposes'''
        credsFile = open("../github-creds.json")
        creds = json.load(credsFile)
        username = creds["username"]
        password = creds["password"]
        credsFile.close()
        return {"api.github.com" : (username, password)}