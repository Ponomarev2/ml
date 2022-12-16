import collections

def listDiff(a,b):
    i = 0
    while i < len(a):
        j = 0
        while j < len(b):
            if a[i] == b[j]:
                a.pop(i)
                b.pop(j)
                i -= 1
                break
            j += 1
        i += 1
        
    return a

def prepareText(text):
    text = text.lower()
    return text
    
def getVocab(text, trashold=30, punctuation = [' ', ], maxNgramLen=12):
    chars = list(text)
    counterTokens = dict(collections.Counter(chars))
    visited = {}
    empty = []
    f = 0
    countersNgram = [dict(collections.Counter([text[i:i+prefixLen + 1] for i in range(len(text) - prefixLen)])) for prefixLen in range(1,maxNgramLen)] # ngramLen - 2,3,4...
    while f == 0:
        f = 1
        maxCount = 0
        for elem, count in counterTokens.items():
            if (count > maxCount) and (elem not in punctuation) and (elem not in empty) and (count > trashold):
                maxCount = count
                prefix = elem
                f = 0
                
        if prefix == 'h':          
            print(prefix)
            print(counterTokens)    

        while 1:
            try:        
                if visited[prefix] != '':
                    pass
            except:
                visited[prefix] = ''

            maxCount = 0
            newprefix = 'X'
            tokensString = ' '.join(list(counterTokens.keys()))
            for elem, count in counterTokens.items():
                word = prefix + elem
                try:
                    count = countersNgram[len(word)-2][word]
                except:
                    continue
                
                if (elem not in punctuation) and (elem not in visited[prefix]) and (word not in tokensString):
                    if (count > maxCount) and (count > trashold) :
                        maxCount = count
                        newprefix = word
                        suffix = elem

                    elif (newprefix in word) and ((maxCount - count) < trashold):
                        maxCount = count
                        newprefix = word
                        suffix = elem

            if prefix == 'h':
                print(newprefix, maxCount)
            
            if maxCount == 0:
                #print(visited[prefix])
                #print(counter2)
                empty.append(prefix)
                break

            counterTokens[newprefix] = maxCount
            counterTokens[prefix] -= maxCount
            counterTokens[suffix] -= maxCount

            visited[prefix] += ' ' + suffix
            
            try:
                if counterTokens[prefix] < trashold and prefix != suffix:
                    counterTokens.pop(prefix)

                if counterTokens[suffix] <= 0:
                    counterTokens.pop(suffix)    
            except:
                pass
            
            prefix = newprefix

    
    for token in list(counterTokens.keys()):
        count = counterTokens[token]
        if count < trashold:
            counterTokens.pop(token)
        
    print(counterTokens)
    
    # add sybs
    for elem in list(set(text)):
        counterTokens[elem] = 1
    return counterTokens

def getFirstTokens(text, word2num, maxlen):
    first_tokens = []
    for i in range(maxlen, 0, -1):
        try:
            if word2num[text[:i]] != '':
                first_tokens.append(i)
        except:
            continue
            
    return first_tokens

def getBestNextTokenLen(text, word2num, maxlen):
    for i in range(maxlen, 0, -1):
        try:
            if word2num[text[:i]] != '':
                return i
        except:
            continue
            
    return 0

def bestLenOf2Tokens(text, word2num, maxlen):
    first_tokens = getFirstTokens(text, word2num, maxlen)
    maxl = 0
    maxi = 0
    for l in first_tokens:
        suml = l + getBestNextTokenLen(text[l:], word2num, maxlen)
        if suml > maxl:
            maxl = suml
            maxi = l
       
    return maxi

def tokenizeText(text, word2num):
    tokens = []
    maxlen = len(list(word2num.keys())[-2]) 
    j = 0
    while j < len(text):
        i = bestLenOf2Tokens(text[j:], word2num, maxlen)
        #print(j,i, text[j:j+i])
        tokens.append(word2num[text[j:j+i]])
        j += i
                
    return tokens        

def detokenize(tokens, num2word):
    text = [num2word[tokens[i]] for i in range(len(tokens))]
    return ''.join(text)
