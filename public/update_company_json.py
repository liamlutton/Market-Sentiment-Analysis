import paralleldots
import unicodedata
import bs4
from bs4 import BeautifulSoup as soup
from six.moves import urllib
import json
import sys


print("test")
# Setting your API key
paralleldots.set_api_key("NlSzhn0HmhTaBrK9ufzeKMoyMbJI4uGBYpJkSLXz1uo")

# Viewing your API key
print("Our API key: " + paralleldots.get_api_key())

# Test getting emotion output from a string

def getEmotionsDicFromText(input):
    text = input

    emotionsDic = paralleldots.emotion(text);
    emotionsUnicode = emotionsDic[u'emotion'][u'probabilities']

    emotionsStringDic  = {}

    for emotion in emotionsUnicode:
        emotionsStringDic[unicodedata.normalize('NFKD', emotion).encode('ascii', 'ignore')] = emotionsUnicode[emotion]

    return emotionsStringDic

def getNewsList(search_query):

    news_url="https://news.google.com/rss/search?q={" + search_query.replace(' ', '_') + "_stock}"
    Client=urllib.request.urlopen(news_url)
    xml_page=Client.read()
    Client.close()

    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    return news_list;

    # Print news title, url and publish date
    for news in news_list:
        #print(type(news_list))
        print(news.title.text)
        print(news.link.text)
        print(news.pubDate.text)
        print("-"*60)

#Get the first 5 title strings

def getTitlesArr(search_query, num):
    newsList = getNewsList(search_query);

    firstTitles = []

    for news in range(num):
        firstTitles.append(unicodedata.normalize('NFKD', newsList[news].title.text).encode('ascii', 'ignore'))

    return firstTitles

def getUrlArr(search_query, num):
    newsList = getNewsList(search_query)

    UrlArr = []

    for news in range(num):
        UrlArr.append(unicodedata.normalize('NFKD', newsList[news].link.text).encode('ascii', 'ignore'))

    return UrlArr

def getPercentPositive(dic):
    #for str in dic.keys():
    #    print(str)
    return (dic['Excited'] + dic['Happy'])

def getPercentNegative(dic):
    return (dic['Angry'] + dic['Sad'] + dic['Fear'] + dic['Bored'])

def getEmotionPercentage(dic, emotion_name):
    return dic[emotion_name]

def getDictArrFromStringArr(titlesArr):
    dictArr = []
    for title in titlesArr:
        dictArr.append(getEmotionsDicFromText(title))
    return dictArr

def getAveragePercentageDict(dictArr):
    averagePercentDict = {}
    for emotion in dictArr[0]:

        totalPercent = 0

        for dic in dictArr:
            totalPercent += dic[emotion]

        averagePercentDict[emotion] = float(round((totalPercent / len(dictArr)) * 1000)) / 10

    return averagePercentDict

def getAveragePositiveEmotions(dictArr):
    return getPercentPositive(getAveragePercentageDict(dictArr))

def getAverageNegativeEmotions(dictArr):
    return getPercentNegative(getAveragePercentageDict(dictArr))

def createJSON(nameOfCompany, articleNum):
    titlesArr = getTitlesArr(nameOfCompany, articleNum)
    urlArr = getUrlArr(nameOfCompany, articleNum)

    dictArr = getDictArrFromStringArr(titlesArr)

    averagePercentageDict = {}

    averagePercentageDict["emotions"] = getAveragePercentageDict(dictArr)

    averagePercentageDict["companyName"] = nameOfCompany

    averagePercentageDict["numberArticlesAnalyzed"] = articleNum

    percentPositive = getAveragePositiveEmotions(dictArr)
    percentNegative = getAverageNegativeEmotions(dictArr)

    averagePercentageDict["percentPositive"] = percentPositive
    averagePercentageDict["percentNegative"] = percentNegative

    averagePercentageDict["titles"] = titlesArr

    averagePercentageDict["links"] = urlArr

    jsonOutput = json.dumps(averagePercentageDict)

    obj = open('public/data.json', 'w')
    obj.write(jsonOutput)
    obj.close

    print("Created json file")
    return jsonOutput

# Run with input parameter
print(sys.argv)
unformattedInput = sys.argv[1];

result = [x.strip() for x in unformattedInput.split(',')]

companyName = result[0]
numArticles = int(float(result[1]))

print("ran script and created json with input "
+ companyName + " and " + str(numArticles) + " articles.")

createJSON(companyName, numArticles)
