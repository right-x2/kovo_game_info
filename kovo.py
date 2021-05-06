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

    print(f"{round}라운드 {home_team}vs{away_team}")
    for set in range(1,1+set_len):
        driver.get(f'https://www.kovo.co.kr/media/popup_result.asp?season=017&g_part=201&r_round={round}&g_num={game_list[game_idx]}&r_set={set}')
    
        text_list = driver.find_elements_by_class_name('txt_left')
        #print("-----------")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml') 

        text_list = soup.find("div",{"class":"wrp_con"}).find_all("li")
        home_players = []
        away_players = []
        home_position_num = [5,6,1,4,3,2]
        away_position_num = [2,3,4,1,6,5]  
        home_player_list = soup.find_all("ul",{"class":f"p_left"})
        away_player_list = soup.find_all("ul",{"class":f"p_right"})
        
        if(len(text_list[1].find("span",{"class":"txt txt_left"}).get_text())==0):
            serve = "right"
        else:
            serve = "left"
        
        for li in home_player_list:
            temp = li.find_all("li")
            for ply in temp:
                home_players.append(ply.get_text().rstrip())
        for li in away_player_list:
            temp = li.find_all("li")
            for ply in temp:
                away_players.append(ply.get_text().rstrip())


        
        #print(text_list)
        home_score = 0
        away_score = 0
        succes = 0
        fail = 0
        list =[]
        count = 0
        for idx in range(len(text_list)):
            
            home_txt = text_list[idx].find("span",{"class":f"txt_left"}).get_text().rstrip()
            away_txt = text_list[idx].find("span",{"class":f"txt_right"}).get_text().rstrip()
            if(home_txt[-2:]=="교체"):
                player_name = home_txt[home_txt.find(".")+1:home_txt.find(" ")]
                sub_txt = text_list[idx+1].find("span",{"class":f"txt_left"}).get_text()
                sub_name = sub_txt[sub_txt.find(".")+1:sub_txt.find(" ")]
                home_players[home_players.index(player_name)] = sub_name
                continue
            
            if(away_txt[-2:]=="교체"):
                player_name = away_txt[away_txt.find(".")+1:away_txt.find(" ")]
                sub_txt = text_list[idx+1].find("span",{"class":f"txt_right"}).get_text()
                sub_name = sub_txt[sub_txt.find(".")+1:sub_txt.find(" ")]
                away_players[away_players.index(player_name)] = sub_name
                continue
            
            if(text_list[idx].find("span",{"class":"score_left"}).get_text().isdigit()==True and text_list[idx].find("span",{"class":f"score_right"}).get_text().isdigit()==True):
                #print(serve)
                #print(players)
                #print(position_num)
                if(home_score<int(text_list[idx].find("span",{"class":"score_left"}).get_text())):
                    if(serve=="right"):
                        serve = "left"
                        for num in range(6):
                            if(home_position_num[num]==1):
                                home_position_num[num] = 6
                            else:
                                home_position_num[num] = home_position_num[num]-1  

                if(away_score<int(text_list[idx].find("span",{"class":f"score_right"}).get_text())):
                    if(serve=="left"):
                        serve = "right"
                        for num in range(6):
                            if(away_position_num[num]==1):
                                away_position_num[num] = 6
                            else:
                                away_position_num[num] = away_position_num[num]-1  
                
                home_score = int(text_list[idx].find("span",{"class":"score_left"}).get_text())
                away_score = int(text_list[idx].find("span",{"class":"score_right"}).get_text())
                #print(f"{home_score} : {away_score}")
                #print(position_num)
 
            if(home_txt.find("세트")> -1):
                if(home_txt[-2:]=="성공"):
                    succes = succes+1
                    setter = home_txt[home_txt.find(".")+1:home_txt.find(" ")]
                    if(setter not in home_players):
                        continue
                    setter_pos_num = home_position_num[home_players.index(setter)]
                    op_txt = text_list[idx+1].find("span",{"class":f"txt_left"}).get_text()
                    op_name = op_txt[op_txt.find(".")+1:op_txt.find(" ")].rstrip()
                    if(op_name not in home_players):
                        continue
                    op_pos_num =  home_position_num[home_players.index(op_name)]
                    op_type = op_txt[op_txt.find(" ")+1:op_txt.find("성")]
                    temp = [round,home_team,away_team,set,setter,setter_pos_num,op_name,op_pos_num,op_type,"성공","성공",home_score,away_score,home_score-away_score]
                    lst.append(temp)
                elif(home_txt[-2:]=="세트"):
                    fail = fail + 1
                    setter = home_txt[home_txt.find(".")+1:home_txt.find(" ")]
                    if(setter not in home_players):
                        continue
                    setter_pos_num = home_position_num[home_players.index(setter)]
                    op_txt = text_list[idx+1].find("span",{"class":f"txt_left"}).get_text()
                    if(len(op_txt)==0):
                        continue
                    op_txt = text_list[idx+1].find("span",{"class":f"txt_left"}).get_text()
                    op_name = op_txt[op_txt.find(".")+1:op_txt.find(" ")].rstrip()
                    if(op_name not in home_players):
                        continue
                    op_pos_num =  home_position_num[home_players.index(op_name)]
                    temp_txt = text_list[idx+2].find("span",{"class":f"txt_right"}).get_text()
                    if(temp_txt=="팀득점"):
                        fail_txt = op_txt[int(op_txt.find(" "))+1:]
                        mid_idx = int(fail_txt.find(" "))
                        op_type = fail_txt[:mid_idx]
                        fail_type = fail_txt[mid_idx+1:]
                    else:
                        op_type = op_txt[op_txt.find(" ")+1:]
                        fail_txt = temp_txt[temp_txt.find(" ")+1:]
                        if(fail_txt=="블로킹 성공 득점"):
                            fail_type = "블로킹 차단 실점"
                        else:
                            fail_type = fail_txt[:fail_txt.find(" ")]
                        #print(f"{op_name} {op_pos_num} {op_pos}")
                    temp = [round,home_team,away_team,set,setter,setter_pos_num,op_name,op_pos_num,op_type,"실패",fail_type,home_score,away_score,home_score-away_score]
                    lst.append(temp)
            
            elif(away_txt.find("세트")> -1):
                if(away_txt[-2:]=="성공"):
                    succes = succes+1
                    setter = away_txt[away_txt.find(".")+1:away_txt.find(" ")]
                    if(setter not in away_players):
                        continue
                    setter_pos_num = away_position_num[away_players.index(setter)]
                    op_txt = text_list[idx+1].find("span",{"class":"txt_right"}).get_text()
                    op_name = op_txt[op_txt.find(".")+1:op_txt.find(" ")].rstrip()
                    if(op_name not in away_players):
                        continue
                    op_pos_num =  away_position_num[away_players.index(op_name)]
                    op_type = op_txt[op_txt.find(" ")+1:op_txt.find("성")]
                    temp = [round,away_team,home_team,set,setter,setter_pos_num,op_name,op_pos_num,op_type,"성공","성공",away_score,home_score,away_score-home_score]
                    lst.append(temp)
                elif(away_txt[-2:]=="세트"):
                    fail = fail + 1
                    setter = away_txt[away_txt.find(".")+1:away_txt.find(" ")]
                    if(setter not in away_players):
                        continue
                    setter_pos_num = away_position_num[away_players.index(setter)]
                    op_txt = text_list[idx+1].find("span",{"class":"txt_right"}).get_text()
                    if(len(op_txt)==0):
                        continue
                    op_txt = text_list[idx+1].find("span",{"class":"txt_right"}).get_text()
                    op_name = op_txt[op_txt.find(".")+1:op_txt.find(" ")].rstrip()
                    if(op_name not in away_players):
                        continue
                    op_pos_num =  away_position_num[away_players.index(op_name)]
                    temp_txt = text_list[idx+2].find("span",{"class":"txt_left"}).get_text()
                    if(temp_txt=="팀득점"):
                        fail_txt = op_txt[int(op_txt.find(" "))+1:]
                        mid_idx = int(fail_txt.find(" "))
                        op_type = fail_txt[:mid_idx]
                        fail_type = fail_txt[mid_idx+1:]
                    else:
                        op_type = op_txt[op_txt.find(" ")+1:]
                        fail_txt = temp_txt[temp_txt.find(" ")+1:]
                        if(fail_txt=="블로킹 성공 득점"):
                            fail_type = "블로킹 차단 실점"
                        else:
                            fail_type = fail_txt[:fail_txt.find(" ")]
                        #print(f"{op_name} {op_pos_num} {op_pos}")
                    temp = [round,away_team,home_team,set,setter,setter_pos_num,op_name,op_pos_num,op_type,"실패",fail_type,away_score,home_score,away_score-home_score]
                    lst.append(temp)
            if(txt_temp[-2:]=="정확"):
                save = 1
            else:
                save = 0
df1 = pd.DataFrame(data = np.array(lst),columns=["라운드","팀","상대팀","SET","세터이름","세터 포지션번호","공격수이름","공격수 포지션번호","공격유형","세트성공여부","실패유형","팀 점수","상대팀 점수","점수차이"])
df1.to_csv("/Users/kimjungwoo/Downloads/gs_setter.csv")
