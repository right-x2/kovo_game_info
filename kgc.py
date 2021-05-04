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

driver.implicitly_wait(3)
game_list = [4,12,17,24,34,41,51,57,65,69,76,84,89,96,102,113,115,121,130,137,151,156,161,172,179,185,188,191,196,200]
lst = []
all_players =[" ","지민경","하효림","염혜선","이예솔","노란","박은진","고민지","나현수","오지영","채선아","최은지","한송이","디우프"," ","이선우","고의정","정호영","이솔아"," ","서유경"]
players_position = [" ","레프트","세터","세터","레프트","리베로","센터","레프트","센터","리베로","레프트","레프트","센터","라이트"," ","레프트","레프트","센터","세터"," ","레프트"]
round = 0
for game_idx in range(len(game_list)):
    if(game_idx%5==0):
        round = round + 1
    driver.get(f'https://www.kovo.co.kr/media/popup_result.asp?season=017&g_part=201&r_round={round}&g_num={game_list[game_idx]}')
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml') 
    soup.find("td",{"class":"first"})
    print(soup.find("td",{"class":"first team"}).find("span",{"class":"team"}))
    if(soup.find("td",{"class":"first team"}).find("span",{"class":"team"}).get_text()=="KGC인삼공사"):
        opp_team_name = soup.find("td",{"class":"last team"}).find("span",{"class":"team"}).get_text()
        my_team = "left"
        opp_team = "right"
        home = my_team
        away = opp_team
    else:
        opp_team_name = soup.find("td",{"class":"first team"}).find("span",{"class":"team"}).get_text()
        my_team = "right"
        opp_team = "left"
        home = opp_team
        away = my_team
    score_list = []
    list = driver.find_elements_by_class_name('num')
    set_len = int(list[0].text)+int(list[1].text)
    #print(set_len)

    print(f"{round}라운드 vs{opp_team_name}")
    for set in range(1,1+set_len):
        driver.get(f'https://www.kovo.co.kr/media/popup_result.asp?season=017&g_part=201&r_round={round}&g_num={game_list[game_idx]}&r_set={set}')
    
        text_list = driver.find_elements_by_class_name('txt_left')
        #print("-----------")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml') 

        text_list = soup.find("div",{"class":"wrp_con"}).find_all("li")
        players = []
        if(home==my_team):
            position_num = [5,6,1,4,3,2]
        else:
            position_num = [2,3,4,1,6,5]  
        player_list = soup.find_all("ul",{"class":f"p_{my_team}"})
        if(len(text_list[1].find("span",{"class":"txt txt_left"}).get_text())==0):
            serve = "right"
        else:
            serve = "left"
        
        for li in player_list:
            temp = li.find_all("li")
            for ply in temp:
                players.append(ply.get_text())


        
        #print(text_list)
        my_score = 0
        opp_score = 0
        succes = 0
        fail = 0
        list =[]
        for idx in range(len(text_list)):
            
            txt = text_list[idx].find("span",{"class":f"txt_{my_team}"}).get_text().rstrip()
            if(txt[-2:]=="교체"):
                player_idx = int(txt[:txt.find(".")])
                player_name = all_players[player_idx].strip()
                sub_txt = text_list[idx+1].find("span",{"class":f"txt_{my_team}"}).get_text()
                sub_idx = int(sub_txt[:sub_txt.find(".")])
                sub_name = all_players[sub_idx].strip()
            # print(sub_name)
                #print(player_idx)
                players[players.index(player_name)] = sub_name
                continue
            if(text_list[idx].find("span",{"class":f"score_{my_team}"}).get_text().isdigit()==True and text_list[idx].find("span",{"class":f"score_{opp_team}"}).get_text().isdigit()==True):
                #print(serve)
                #print(players)
                #print(position_num)
                if(opp_score<int(text_list[idx].find("span",{"class":f"score_{opp_team}"}).get_text())):
                    if(serve==my_team):
                        serve = opp_team

                if(my_score<int(text_list[idx].find("span",{"class":f"score_{my_team}"}).get_text())):
                    if(serve==opp_team):
                        serve = my_team 
                        for num in range(6):
                            if(position_num[num]==1):
                                position_num[num] = 6
                            else:
                                position_num[num] = position_num[num]-1  
                
                my_score = int(text_list[idx].find("span",{"class":f"score_{my_team}"}).get_text())
                opp_score = int(text_list[idx].find("span",{"class":f"score_{opp_team}"}).get_text())
                #print(f"{my_score} : {opp_score}")
                #print(position_num)
            if(len(txt)==0):
                continue
            if(txt[0:2]=="11"):
                print(txt)
            if(txt[0]=="2"):
                #print(txt[2:8])
 
                if(txt[2:8]=="하효림 세트"):
                    if(txt[-2:]=="성공"):
                        succes = succes+1
                        my_pos_num = position_num[players.index("하효림")]
                        op_txt = text_list[idx+1].find("span",{"class":f"txt_{my_team}"}).get_text()
                        op_idx = int(op_txt[:op_txt.find(".")])
                        op_name = all_players[op_idx].strip()
                        op_pos_num =  position_num[players.index(op_name)]
                        op_pos = players_position[op_idx]
                        op_type = op_txt[op_txt.find(" ")+1:op_txt.find("성")]
                        #print(f"{op_name} {op_pos_num} {op_pos}")
                        temp = [round,opp_team_name,set,my_pos_num,op_pos_num,op_pos,op_name,op_type,"성공","성공",my_score,opp_score,my_score-opp_score]
                        lst.append(temp)
                    elif(txt[-2:]=="세트"):
                        fail = fail + 1
                        my_pos_num = position_num[players.index("하효림")]
                        op_txt = text_list[idx+1].find("span",{"class":f"txt_{my_team}"}).get_text()
                        if(len(op_txt)==0):
                            continue
                        op_idx = int(op_txt[:op_txt.find(".")])
                        op_name = all_players[op_idx].strip()
                        op_pos_num =  position_num[players.index(op_name)]
                        op_pos = players_position[op_idx]
                        temp_txt = text_list[idx+2].find("span",{"class":f"txt_{opp_team}"}).get_text()
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
                        temp = [round,opp_team_name,set,my_pos_num,op_pos_num,op_pos,op_name,op_type,"실패",fail_type,my_score,opp_score,my_score-opp_score]
                        lst.append(temp)

        #print(f"성공: {succes} 실패: {fail}")
#print(lst)
df1 = pd.DataFrame(data = np.array(lst),columns=["라운드","상대팀","SET","포지션번호","공격수 포지션번호","공격수 포지션","공격수","공격유형","세트성공여부","실패유형","팀 점수","상대팀 점수","점수차이"])
df1.to_csv("/Users/kimjungwoo/Downloads/kgc_hyorim.csv")
                        

        

        





