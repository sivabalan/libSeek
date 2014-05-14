import binascii,os,re,json
re.DOTALL = True

def process(part):
    try:
        parts = part.split("\n")
        filename = re.match("__FILENAME__ = (.*)\.py", parts[0]).groups()[0]
        data = "\n".join(parts[1:])
        pycontent = binascii.a2b_base64(data.strip())
        return filename, pycontent
    except AttributeError:
        print "KKKKRASHHHHH!!", part

def getlibs(pycontent):
    pylines = pycontent.replace("\r", "").split("\n")
    #match cases:
    #import re                  get re
    #from re import *           get re
    #from re.compile import *   get compile
    # import re.compile         get compile
    #can have ; at end
    libs = set()
    for line in pylines:
        line = line.strip()
        matches = re.match("^import\s+(.*)", line)
        modulepath = None
        if matches:
            modulepath = matches.groups()[0].strip()
        else:
            matches = re.match("^from\s+([\w|\.|\*]+)\s+import\s+(.+)", line)
            if matches:
                modulepath = matches.groups()[0].strip()
                if modulepath == "__future__":
                    modulepath = matches.groups()[1].strip()
        if modulepath:
            libparts = modulepath.split(",")
            libparts = [part.split("as")[0].strip() for part in libparts]
            for part in libparts:
                libs.add(part.split(".")[-1].strip() if part.split(".")[-1].strip() != "*" else "")
    return libs


def processRepo(dir):
    file = open("repoData/" + dir + "/allPythonContent.py", "r")
    content = file.read()
    parts = content.split("########NEW FILE########\n")
    liblist = {}
    libraries = set()
    for part in parts:
        pyfile = process(part)
        if (pyfile):
            liblist[pyfile[0]] = getlibs(pyfile[1])

    for file in liblist:
        for lib in liblist[file]:
            if lib != "" and lib not in liblist:
                libraries.add(lib)

    return libraries


repoCount = 0
for dir in os.listdir("repoData"):
    if os.access("repoData/" + dir + "/allPythonContent.py", os.F_OK):
        libraries = processRepo(dir)
        json.dump({ "libs" : list(libraries)}, open("repoData/" + dir + "/libs-new.json", "w"), sort_keys=True, indent=4, separators=(',', ': '))
        print repoCount
        repoCount += 1
    else:
        try:
            os.remove("repoData/" + dir + "/metaData.json")
            os.rmdir("repoData/" + dir)
        except OSError:
            os.remove("repoData/" + dir + "/description.txt")
            os.rmdir("repoData/" + dir)