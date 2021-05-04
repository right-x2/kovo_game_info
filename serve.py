# -*- coding: utf8 -*- 
import requests
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
#options.add_argument("headless")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!

driver = webdriver.Chrome('/Users/kimjungwoo/Downloads/chromedriver',chrome_options=options)

def get_list():
    list = []
    for i in range(1,7):
        driver.get(f'https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=017&yymm=&s_part=2&r_round={i}')
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml') 
        table = soup.find_all("tr",{"class":"end"})
        
    
        for j in table:
            temp = j.find_all("td")
            if((temp[1].get_text()).isdigit()==True):
                list.append(temp[1].get_text())
    return list


driver.implicitly_wait(3)
game_list = []
lst = []
row_lst = []
round = 0
game_count = 0
game_list = get_list()
print(game_list)
for game_idx in range(len(game_list)):
    if(game_idx%15==0):
        round = round + 1
    driver.get(f'https://www.kovo.co.kr/media/popup_result.asp?season=017&g_part=201&r_round={round}&g_num={game_list[game_idx]}')
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml') 
    soup.find("td",{"class":"first"})
    home_team = soup.find("td",{"class":"first team"}).find("span",{"class":"team"}).get_text()
    away_team = soup.find("td",{"class":"last team"}).find("span",{"class":"team"}).get_text()
    score_list = []
    list = driver.find_elements_by_class_name('num')
    set_len = int(list[0].text)+int(list[1].text)
    #print(set_len)

    for set in range(1,1+set_len):
        driver.get(f'https://www.kovo.co.kr/media/popup_result.asp?season=017&g_part=201&r_round={round}&g_num={game_list[game_idx]}&r_set={set}')
    
        text_list = driver.find_elements_by_class_name('txt_left')
        #print("-----------")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml') 

        text_list = soup.find("div",{"class":"wrp_con"}).find_all("li")
        if(len(text_list[1].find("span",{"class":"txt txt_left"}).get_text())==0):
            serve = "right"
        else:
            serve = "left"
        
        #print(text_list)
        home_score = 0
        away_score = 0
        succes = 0
        fail = 0
        player_list =[]
        flag = 0
        sflag = 0
        row_count = 0
        for idx in range(len(text_list)):
            txt = text_list[idx].find("span",{"class": f"txt_{serve}"}).get_text().rstrip()
            if(text_list[idx].find("span",{"class":"score_left"}).get_text().isdigit()==True and text_list[idx].find("span",{"class":"score_right"}).get_text().isdigit()==True):
                sflag = 0
                if(home_score<int(text_list[idx].find("span",{"class": "score_left"}).get_text())):
                    if(serve=="right"):
                        serve = "left"
                        if(flag==4):
                            temp = [team_name,server_name,0,save,0,0,my_score,opp_score,my_score-opp_score,set]
                            lst.append(temp)
                            row_temp = [team_name,server_name,row_count]
                            row_lst.append(row_temp)
                            flag = 0
                            row_count = 0
                        elif(flag==3):
                            temp = [team_name,server_name,0,save,0,0,my_score,opp_score,my_score-opp_score,set]
                            lst.append(temp)
                            row_temp = [team_name,server_name,row_count]
                            row_lst.append(row_temp)
                            flag = 0
                            row_count = 0   
                    else:
                        if(flag==4 or flag==3):
                            row_count = row_count +1
                            temp = [team_name,server_name,1,save,0,0,my_score,opp_score,my_score-opp_score,set]
                            lst.append(temp)
                            flag = 2
                elif(away_score<int(text_list[idx].find("span",{"class": "score_right"}).get_text())):
                    if(serve=="left"):
                        serve = "right" 
                        if(flag==4):
                            temp = [team_name,server_name,0,save,0,0,my_score,opp_score,my_score-opp_score,set]
                            lst.append(temp)
                            row_temp = [team_name,server_name,row_count]
                            row_lst.append(row_temp)
                            flag = 0
                            row_count = 0
                        elif(flag==3):
                            temp = [team_name,server_name,0,save,0,0,my_score,opp_score,my_score-opp_score,set]
                            lst.append(temp)
                            row_temp = [team_name,server_name,row_count]
                            row_lst.append(row_temp)
                            flag = 0
                            row_count = 0                   
                    else:
                        if(flag==4 or flag==3):
                            temp = [team_name,server_name,1,save,0,0,my_score,opp_score,my_score-opp_score,set]
                            lst.append(temp)
                            flag = 2
                            row_count = row_count +1
                else:
                    if(txt[-2:]=="투입"):
                        player_name = txt[txt.find(".")+1:txt.find(" ")]
                        player_list.append(player_name)
                        flag = 1
                        #print("------"+player_name)
                home_score = int(text_list[idx].find("span",{"class":f"score_left"}).get_text())
                away_score = int(text_list[idx].find("span",{"class":f"score_right"}).get_text())
                if(serve=="left"):
                    team_name = home_team
                    my_score = home_score
                    opp_score = away_score
                    opp_str = "right"
                else:
                    team_name = away_team
                    my_score = away_score
                    opp_score = home_score
                    opp_str = "left"
                #print(f"{home_score} : {away_score}")
                #print(position_num)
            elif(flag==1 and txt.find("서브")>=0):
                server_name = txt[txt.find(".")+1:txt.find(" ")]
                sflag = 0
                #print(server_name)
                for name in player_list:
                    if(name==server_name):
                        flag = 2
                player_list = []
                if(flag==2):
                    #print(str(len(txt))+"----"+txt)
                    if(txt[-2:]=="서브"):
                        sflag = 1
                    elif(txt[-2:]=="득점"):
                        temp = [team_name,server_name,1,0,1,0,my_score,opp_score,my_score-opp_score,set]
                        lst.append(temp)
                        row_count = row_count + 1
                    else:
                        temp = [team_name,server_name,0,0,0,1,my_score,opp_score,my_score-opp_score,set]
                        lst.append(temp)
                        row_temp = [team_name,server_name,row_count]
                        row_lst.append(row_temp)
                        row_count = 0
                        flag = 0
                else:
                    flag = 0
            elif(flag==2):
                #print(txt)
                if(sflag ==0 and txt.find("서브")>=0):
                    if(txt[-2:]=="서브"):
                        sflag = 1
                        continue
                    elif(txt[-2:]=="득점"):
                        temp = [team_name,server_name,1,0,1,0,my_score,opp_score,my_score-opp_score,set]
                        lst.append(temp)
                        row_count = row_count + 1
                    else:
                        temp = [team_name,server_name,0,0,0,1,my_score,opp_score,my_score-opp_score,set]
                        lst.append(temp)
                        row_temp = [team_name,server_name,row_count]
                        row_lst.append(row_temp)
                        flag = 0
                        row_count = 0
                    
                elif(sflag==1):
                    txt_temp = text_list[idx].find("span",{"class":f"txt_{opp_str}"}).get_text().rstrip()
                    if(txt_temp[-2:]=="정확"):
                        save = 1
                    else:
                        save = 0
                    sflag = 0
                    flag = 3
            elif(flag==1 and txt[-2:]=="투입"):
                player_name = txt[txt.find("."):txt.find(" ")]
                player_list.append(player_name)
            elif(flag==3):
                if(len(txt)>0):
                    flag=4
#print(lst)
df1 = pd.DataFrame(data = np.array(lst),columns=["팀","이름","기대득점","리시브정확도","서브득점","서브범실","팀 점수","상대 점수","점수차이","SET"])
df2 = pd.DataFrame(data = np.array(row_lst),columns=["팀","이름","연속득점"])
df1.to_csv("/Users/kimjungwoo/Downloads/serve3.csv")
df2.to_csv("/Users/kimjungwoo/Downloads/row_serve3.csv")
                        

        

        





