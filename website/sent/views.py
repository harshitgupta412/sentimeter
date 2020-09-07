from django.shortcuts import render, redirect
from django.http import JsonResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .models import Data, Keys
import datetime
from decimal import *
def get_data():
    # scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./sent/Sentdex.json')
    client = gspread.authorize(creds)
    sheet = client.open('Data Sheet') 
    return sheet
    # keyword_list_sheet = sheet.worksheet('') # List of keywords is name of subsheet
    # keyword_list=keyword_list_sheet.col_values(1)
    # display_name_list=keyword_list_sheet.row_values(2)
#The above two lines contain example of how you can read a row or a column. 

def reload(request):
    print('reloading')
    sheet = get_data()
    keys = sheet.worksheet('List Of Keywords').col_values(2)
    twitter = sheet.worksheet('Twitter').get_all_values()[1:]
    reddit = sheet.worksheet('Reddit').get_all_values()[1:]
    news = sheet.worksheet('News').get_all_values()[1:]
    overall = sheet.worksheet('Overall').get_all_values()[1:]
    for k in Keys.objects.all():
        k.delete()
    print(reddit)
    for i in range(len(keys)):
        key = Keys(keyword=keys[i])
        key.save()
        v_last_o = 100
        v_last_t = 100
        v_last_r = 100
        v_last_n = 100

        for j in range(len(overall)):
            if Decimal(twitter[j][2*i+2])!=0:
                v_last_t = Decimal(twitter[j][2*i+2])
            if Decimal(news[j][2*i+2])!=0:
                v_last_n = Decimal(news[j][2*i+2])
            if Decimal(reddit[j][2*i+2])!=0:
                v_last_r =Decimal(reddit[j][2*i+2])
            if Decimal(overall[j][2*i+2])!=0:
                v_last_o =Decimal(overall[j][2*i+2])
            
            data = Data(keys = key,
             date=datetime.datetime.strptime(overall[j][0], "%Y-%m-%d"),
             twitter=Decimal(twitter[j][2*i+1]),
             reddit=Decimal(reddit[j][2*i+1]),
             news=Decimal(news[j][2*i+1]),
             overall=Decimal(overall[j][2*i+1]),
             v_twitter=v_last_t,
             v_reddit=v_last_r,
             v_news=v_last_n,
             v_overall=v_last_o,
             )
            data.save()
    print('reload ended')
    return redirect('main')

def main(request):
    l = []
    for k in Keys.objects.all():
        dic = {}
        dic['sent'] = k.data_set.all().order_by('-date')[0]
        dic['last'] = k.data_set.all().order_by('-date')[1]
        dic['key'] = k
        l.append(dic)
        
    # print(last_data)
    context = {
        'data': l
    }
    return render(request, 'sent/main.html',context = context)

def fetchgraph(request):
    key_id = request.POST.get('id')
    key = Keys.objects.filter(pk = key_id).first()
    data = {
        'key': key.keyword,
        'overall': [],
        'v_over': [],
        'twitter': [],
        'v_twit': [],
        'reddit': [],
        'v_reddit': [],
        'news': [],
        'v_news': [],
    }
    for d in key.data_set.all():
        data['overall'].append([d.date, d.overall])
        data['v_over'].append([d.date, d.v_overall])
        data['news'].append([d.date, d.news])
        data['v_news'].append([d.date, d.v_news])
        data['twitter'].append([d.date, d.twitter])
        data['v_twit'].append([d.date, d.v_twitter])
        data['reddit'].append([d.date, d.reddit])
        data['v_reddit'].append([d.date, d.v_reddit])
    
    return JsonResponse(data)