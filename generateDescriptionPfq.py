import json
import os
import base64, binascii
import nltk
import re

<<<<<<< HEAD
allProjFile = open("../projects_meta_data.json")
=======
allProjFile = open("projects_meta_data.json")
>>>>>>> 84e0fa98905512848fe15a25965fc3ac125374f9
allProjDict = json.load(allProjFile)
allProjFile.close()

repoDir = "repoData/"
descFileName = "/description.txt"
pyContentFileName = "/allPythonContent.py"
wordFreqFileName = "/wordFrequencies.pfq" # word <num. occurrences> 

stops = {}
stopslist = "a a's    able    about    above    according accordingly    across    actually    after    afterwards again    against    ain't    all    allow allows    almost    alone    along    already also    although    always    am    among amongst    an    and    another    any anybody    anyhow    anyone    anything    anyway anyways    anywhere    apart    appear    appreciate appropriate    are    aren't    around    as aside    ask    asking    associated    at available    away    awfully    be    became because    become    becomes    becoming    been before    beforehand    behind    being    believe below    beside    besides    best    better between    beyond    both    brief    but by    c'mon    c's    came    can can't    cannot    cant    cause    causes certain    certainly    changes    clearly    co com    come    comes    concerning    consequently consider    considering    contain    containing    contains corresponding    could    couldn't    course    currently definitely    described    despite    did    didn't different    do    does    doesn't    doing don't    done    down    downwards    during each    edu    eg    eight    either else    elsewhere    enough    entirely    especially et    etc    even    ever    every everybody    everyone    everything    everywhere    ex exactly    example    except    far    few fifth    first    five    followed    following follows    for    former    formerly    forth four    from    further    furthermore    get gets    getting    given    gives    go goes    going    gone    got    gotten greetings    had    hadn't    happens    hardly has    hasn't    have    haven't    having he    he's    hello    help    hence her    here    here's    hereafter    hereby herein    hereupon    hers    herself    hi him    himself    his    hither    hopefully how    howbeit    however    i'd    i'll i'm    i've    ie    if    ignored immediate    in    inasmuch    inc    indeed indicate    indicated    indicates    inner    insofar instead    into    inward    is    isn't it    it'd    it'll    it's    its itself    just    keep    keeps    kept know    known    knows    last    lately later    latter    latterly    least    less lest    let    let's    like    liked likely    little    look    looking    looks ltd    mainly    many    may    maybe me    mean    meanwhile    merely    might more    moreover    most    mostly    much must    my    myself    name    namely nd    near    nearly    necessary    need needs    neither    never    nevertheless    new next    nine    no    nobody    non none    noone    nor    normally    not nothing    novel    now    nowhere    obviously of    off    often    oh    ok okay    old    on    once    one ones    only    onto    or    other others    otherwise    ought    our    ours ourselves    out    outside    over    overall own    particular    particularly    per    perhaps placed    please    plus    possible    presumably probably    provides    que    quite    qv rather    rd    re    really    reasonably regarding    regardless    regards    relatively    respectively right    said    same    saw    say saying    says    second    secondly    see seeing    seem    seemed    seeming    seems seen    self    selves    sensible    sent serious    seriously    seven    several    shall she    should    shouldn't    since    six so    some    somebody    somehow    someone something    sometime    sometimes    somewhat    somewhere soon    sorry    specified    specify    specifying still    sub    such    sup    sure t's    take    taken    tell    tends th    than    thank    thanks    thanx that    that's    thats    the    their theirs    them    themselves    then    thence there    there's    thereafter    thereby    therefore therein    theres    thereupon    these    they they'd    they'll    they're    they've    think third    this    thorough    thoroughly    those though    three    through    throughout    thru thus    to    together    too    took toward    towards    tried    tries    truly try    trying    twice    two    un under    unfortunately    unless    unlikely    until unto    up    upon    us    use used    useful    uses    using    usually value    various    very    via    viz vs    want    wants    was    wasn't way    we    we'd    we'll    we're we've    welcome    well    went    were weren't    what    what's    whatever    when whence    whenever    where    where's    whereafter whereas    whereby    wherein    whereupon    wherever whether    which    while    whither    who who's    whoever    whole    whom    whose why    will    willing    wish    with within    without    won't    wonder    would wouldn't    yes    yet    you    you'd you'll    you're    you've    your    yours yourself    yourselves    zero next prev previous".split()
for item in stopslist:
    stops[item.strip()] = 1
wnl = nltk.WordNetLemmatizer()

badrepos = {"bad_repo" : [], "decode_dontknow" : []}
for i in range(0,len(allProjDict)):
<<<<<<< HEAD
#for i in range(len(allProjDict) - 1,len(allProjDict)):
    folderName = allProjDict[i]["full_name"].replace("/", "-")
    tokenString = ""
    if(os.path.isfile(repoDir+folderName+descFileName) and os.path.isfile(repoDir+folderName+pyContentFileName)):
        if allProjDict[i]["description"]:      
            tokenString = allProjDict[i]["description"]
            descString = allProjDict[i]["description"].lower()
=======
	folderName = allProjDict[i]["full_name"].replace("/", "-")
	tokenString = ""
	if(os.path.isfile(repoDir+folderName+descFileName) and os.path.isfile(repoDir+folderName+pyContentFileName)):
		tokenString = allProjDict[i]["description"]
		descString = allProjDict[i]["description"].lower()
		print(str(i) + " : " + folderName)
>>>>>>> 84e0fa98905512848fe15a25965fc3ac125374f9

        print(str(i) + " : " + folderName)

        descFile = open(repoDir+folderName+descFileName);
        desc = descFile.read()
        descFile.close()
        descLines = desc.split("########NEW FILE########\n")
        try:
            for j in range(0,len(descLines)):
                if(descLines[j].strip() != ""):
                    descContent = "\n".join(descLines[j].split('\n')[1:]).strip()
                    descContent = binascii.a2b_base64(descContent)
                    try:
                        tokenString += descContent.replace("\n"," ")
                    except UnicodeDecodeError:
                        try:
                            tokenString += descContent.decode("utf-8").replace("\n"," ")
                        except UnicodeError:
                            try:
                                tokenString += descContent.decode("utf-16").replace("\n"," ")
                            except UnicodeError:
                                badrepos["decode_dontknow"].append(folderName)
                                tokenString += ""
        except TypeError:
            badrepos["bad_repo"].append(folderName)
            continue
    else:
        continue

    if(tokenString != ""):
        tokens = nltk.word_tokenize(tokenString)
        tokenDict = {}
        for i in range(len(tokens)):
            lcToken = tokens[i].lower()
            tokens[i] = wnl.lemmatize(lcToken)
            if re.match(".*[\d+|\W+].*", tokens[i]) == None and lcToken not in stops and len(tokens[i]) > 1:
                if(lcToken in tokenDict):
                    tokenDict[lcToken] += 1
                else:
                    tokenDict[lcToken] = 1

        tokenTupleList = []
        for token in tokenDict:
            tokenTupleList.append((token, tokenDict[token], int(token in descString.split())))

        tokenTupleList.sort(key = lambda x: (x[2],x[1],x[0]), reverse = True)

        tokenWriteString = ""
        for i in range(0,len(tokenTupleList)):
            tokenWriteString += tokenTupleList[i][0]+'\t'+str(tokenTupleList[i][1])+'\t'+str(tokenTupleList[i][2])+'\n'
        
        wordFreqFile = open(repoDir+folderName+wordFreqFileName, "w")
        wordFreqFile.write(tokenWriteString.strip())
        wordFreqFile.close()

json.dump(badrepos, open("badrepos.json", "w"), sort_keys=True, indent=4, separators=(',', ': '))
