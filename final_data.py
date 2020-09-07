import GetOldTweets3 as got
import pandas as pd
#from twitter_scraper import Profile
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import schedule
import newspaper
from newspaper import Config, Article, Source
import pandas as pd

#import nltk
from langdetect import detect
from psaw import PushshiftAPI
import praw
import datetime as dt
import numpy as np


def TwitterDataGatherer(keyword,start_date,end_date,max_tweets=0,top_tweets=True):
    df=pd.DataFrame()
    tweetCriteria=got.manager.TweetCriteria().setQuerySearch(keyword).setSince(start_date).setUntil(end_date).setMaxTweets(max_tweets).setTopTweets(top_tweets)
    tweets=got.manager.TweetManager.getTweets(tweetCriteria)
    text_tweets=[tweet.text for tweet in tweets]
    retweets_tweets=[tweet.retweets for tweet in tweets]
    favorites_tweets=[tweet.favorites for tweet in tweets]
    date_tweets=[tweet.date for tweet in tweets]
    df['date']=date_tweets
    df['title']=text_tweets
    df['content']=''
    df['retweets']=retweets_tweets
    df['favorites']=favorites_tweets
    return df

def listToLower(list1):
    list_new=list1
    for i in range(len(list1)):
        list_new[i]=list1[i].lower()
    return list_new

def NewsGatherer(keywords,newspaper_link,number_of_news,total_news) :
    #Pass list of keywords and number of news to scrape
    #Pass allk keywords in lowercase
    df=pd.DataFrame()
    df['title']=None
    df['content']=None
    df['Summary']=None
    df['Keywords']=None
    df['Date']=None
    df['Name of Newspaper']=None
    newspaper_link=newspaper_link
    keywords=keywords
    config = Config()
    config.fetch_images=False
    config.memoize_articles=False
    paper=newspaper.build(newspaper_link,config=config)
    print('Created Newspaper')
    for keyword in keywords :
        print(keyword)
        news_counter=0
        total_counter=0
        for i in range(len(paper.articles)):
            #print(i)
            if total_counter <=total_news :
                if news_counter<=number_of_news:
                    article=paper.articles[i]
                    try :
                        article.download()
                        article.parse()
                        article.nlp()
                        language_article=detect(article.text)
                        keyword_list=listToLower(article.keywords)
                        if language_article=='en':
                            if article.publish_date :
                                if (keyword in keyword_list) or (keyword in (article.title).lower()) or (keyword in (article.text).lower()) :
                                    df=df.append({'title':article.title,'content':article.text,'Summary':article.summary,'Keywords':article.keywords,'Date':article.publish_date,'Name of Newspaper':str(newspaper_link)},ignore_index=True)
                                    news_counter+=1
                                    print(news_counter)
                            #print(article.title,str(newspaper_link))
                            total_counter+=1
                        else :
                            print(language_article)
                    except :
                        print('error',i)
                        pass
                else :
                    break
            else :
                break
    df['upvote ratio']=1
    return df

#create an app on reddit and replace these details
reddit = praw.Reddit(
    client_id = "*********",
    client_secret = '******************',
    password = '************',
    username = '*********************',
    user_agent = 'sentiment analysis'
)

api = PushshiftAPI(reddit)
# for submission in subreddit.hot(limit=10):
start_epoch=int(dt.datetime(2017, 1, 1).timestamp())
def redditsearch(key):
    gen = api.search_submissions(q=key, limit=100, before = start_epoch)
    result  = list(gen)
    data = [[submission.title, submission.selftext, submission.upvote_ratio] for submission in result]
    df = pd.DataFrame(data, columns=['title', 'content', 'upvote ratio'])
    return df


def TwitterDataFinal(keyword,from_date,to_date,max_tweets=0,top_tweets=True):
    print(keyword)
    # Dates in YYYY-MM-DD
    # max_tweets should not be more then 75
    #df_m=TwitterDataGather(keyword,date_from=from_date,date_to=to_date,max_tweets=max_tweets,TopTweets=top_tweets,lower=lower,higher=higher)
    df_m=TwitterDataGatherer(keyword,start_date=from_date,end_date=to_date,max_tweets=max_tweets,top_tweets=top_tweets)
    df_m['retweets']=df_m['retweets']+2
    df_m['favorites']=df_m['favorites']+2
    #df_m['Followers']=df_m['Followers']+2
    df_m['retweets']=df_m['retweets'].astype(float)
    df_m['favorites']=df_m['favorites'].astype(float)
    #df_m['Verified']=df_m['Verified'].astype(float)
    #df_m['Verified']=df_m['Verified']+2
    #df_m['Followers']=df_m['Followers'].astype(float)
    #df_m['Followers']=np.log(df_m['Followers'])
    #df_m['Followers']=df_m['Followers']*(1/2)
    df_m['retweets']=np.log(df_m['retweets'])
    df_m['retweets']=df_m['retweets']*(2)
    df_m['upvote ratio']=None
    df_m['upvote ratio']=df_m['retweets']*np.log(df_m['favorites'])
    return df_m

news_links=['https://economictimes.indiatimes.com/','https://www.thehindu.com/','https://edition.cnn.com/india','https://edition.cnn.com/','https://www.firstpost.com/']

# import flair
# from flair.data import Sentence

# def sentiment_flair(df):
#     fid = flair.models.TextClassifier.load('en-sentiment')
#     data = []
#     for _,s in df.iterrows():
#         dic_title = Sentence(s['title'])
#         fid.predict(dic_title)
#         dic = {'title': s['title'], 'title_score': (dic_title.labels[0].score), 'title_label':dic_title.labels[0].value , 'upvote': s['upvote ratio']}
#         if len(s['content']) !=0:
#             dic_text  = Sentence(s['content'])
#             fid.predict(dic_text)
#             dic['text_score'] = dic_text.labels[0].score
#             if dic_text.labels[0].value == 'NEGATIVE':
#                 dic['text_score']*=-1
#         if dic_title.labels[0].value == 'NEGATIVE':
#             dic['title_score']*=-1
#         data.append(dic)
#     return pd.DataFrame.from_dict(data)

import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_nltk(df):
    sid = SentimentIntensityAnalyzer()
    data = []
    for _,s in df.iterrows():
        print(s)
        dic_title = sid.polarity_scores(s['title'])
        if s['content']:
            dic_text  = sid.polarity_scores(s['content'])
        dic={}
        for i in dic_title.keys():
            dic[i] = dic_title[i]+dic_text[i]
        dic['sentence'] = s['title']
        dic['upvote'] = s['upvote ratio']
        print(dic_text.labels[0].score,dic_text.labels[0].value, dic_title)
        data.append(dic)
    return pd.DataFrame.from_dict(data)


def scorer(df):
    df=sentiment_nltk(df)
    if 'text_score' in df.columns :
        df['Net Sentiment'] = None
        for i in range(len(df)):
            if df.loc[i,'text_score']:
                df.loc[i,'Net Sentiment']=df.loc[i,'text_score']
            else :
                df.loc[i,'Net Sentiment']=df.loc[i,'title_score']
    else :
        df['Net Sentiment']=df['title_score']
    sum_of_sentiments=(df['Net Sentiment']*df['upvote']).sum()
    sum_of_weights=df['upvote'].sum()
    net_sentiment=(100*sum_of_sentiments/sum_of_weights)
    return [net_sentiment,len(df)]

def top_row_updater(sheet,top_row):
    for i in range(len(top_row)):
        sheet.update_cell(1,i+1,top_row[i])
def job():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Sentdex.json')
    client = gspread.authorize(creds)
    sheet = client.open('Data Sheet')
    keyword_list_sheet = sheet.worksheet('List Of Keywords')
    twitter_sheet=sheet.worksheet('Twitter')
    reddit_sheet=sheet.worksheet('Reddit')
    news_sheet=sheet.worksheet('News')
    overall_sheet=sheet.worksheet('Overall')
    keyword_list=keyword_list_sheet.col_values(1)
    display_name_list=keyword_list_sheet.col_values(2)
    top_list=['Date']
    for i in range(len(display_name_list)):
        top_list=top_list+[display_name_list[i] + ' Sentiment']
        top_list=top_list + [display_name_list[i]+' Volume']
    top_row=top_list

    now=dt.datetime.now()
    yesterday=now-dt.timedelta(days=1)
    day_before_yesterday=now - dt.timedelta(days=2)
    today_date='{0}-{1}-{2}'.format(now.year,now.month,now.day)
    twitter_data_list=[today_date]
    reddit_data_list=[today_date]
    news_data_list=[today_date]
    overall_data_list=[today_date]
    for keyword in keyword_list :
        start_date='{0}-{1}-{2}'.format(day_before_yesterday.year,day_before_yesterday.month,day_before_yesterday.day)
        end_date='{0}-{1}-{2}'.format(yesterday.year,yesterday.month,yesterday.day)
        df=TwitterDataFinal(keyword,start_date,end_date,500,top_tweets=True)
        try :
            list_result=scorer(df)
            print(keyword+' Twitter Done')
        except :
            list_result=[0,0]
            print(keyword +' Twitter Issue')
        twitter_result=list_result
        twitter_data_list=twitter_data_list + twitter_result
        try :
            df=redditsearch(keyword)
            reddit_result=scorer(df)
        except:
            reddit_result=[0,0]
        list_result=list_result + reddit_result
        reddit_data_list=reddit_data_list + reddit_result
        df=pd.DataFrame()
        try :
            for news_link in news_links :
                df=df.append(NewsGatherer([keyword],news_link,20,200),ignore_index=True)
            news_result=scorer(df)
        except :
            news_result=[0,0]
        list_result=list_result + news_result
        news_data_list=news_data_list + news_result
        news_volumes=list_result[5]
        mean_of_all=(list_result[1] + list_result[3])/2
        list_result[5]=mean_of_all
        net_sentiment=(list_result[0]*list_result[1] + list_result[2]*list_result[3] + list_result[4]*list_result[5])/(list_result[1]+list_result[3]+list_result[5])
        net_volume=list_result[1] + list_result[3] + list_result[5]
        list_result=list_result + [net_sentiment,net_volume,news_volumes]
        overall_data_list=overall_data_list+[net_sentiment,net_volume]
    top_row_updater(twitter_sheet,top_row)
    top_row_updater(reddit_sheet,top_row)
    top_row_updater(news_sheet,top_row)
    top_row_updater(overall_sheet,top_row)
    twitter_sheet.insert_row(twitter_data_list,2)
    reddit_sheet.insert_row(reddit_data_list,2)
    news_sheet.insert_row(news_data_list,2)
    overall_sheet.insert_row(overall_data_list,2)



    print('Done !')
    return


schedule.every().day.at("00:00").do(job)
while True:

    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
