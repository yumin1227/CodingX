import sys
import os
import time
import random
import pygame
from pygame.locals import *
from game_class import *
from tkinter import messagebox
import easygui
import matplotlib.pyplot as plt
import platform

pygame.mixer.pre_init(44100, 16, 2, 4096) 						   #frequency, size, channels, buffersize
pygame.init()

barks = pygame.mixer.Sound("barks.wav")							   #匯入後面會用到的音效
barks.set_volume(0.5)
meow= pygame.mixer.Sound("meow.wav")
meow.set_volume(0.8)
moneyget= pygame.mixer.Sound("moneyget.wav")
moneyget.set_volume(0.5)
ohno= pygame.mixer.Sound("ohno.wav")
ohno.set_volume(0.5)
hospital= pygame.mixer.Sound("hospital.wav")
hospital.set_volume(0.5)

FPS = 60 # frame rate for updating game window 					   #一秒會有60張圖片
GAMECLOCK = pygame.time.Clock()
WINDOWWIDTH = 1250 # Width of game window
WINDOWHEIGHT = 650 # Height of game window
GAMETITLE = 'Monopoly' # Title of game window

# Information of game map
HBOXNUM = 9          #地圖的寬有幾格
VBOXNUM = 5			 #地圖的高有幾格
BOXWIDTH = 90       #一格的寬度
BOXHEIGHT = 90		 #一格的高度

# Game setting
pygame.init()                                                      #初始化pygame
window = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))       #設定視窗大小並顯示       
pygame.display.set_caption(GAMETITLE)     						   #設定遊戲名稱   
font_obj = pygame.font.Font('GenYoGothicTW-Regular.ttf', 15)	   #設定字體→(字體名稱,字體尺寸)
INITMONEY = 9000 # Money that each player gets when game starts   #遊戲會開始會得到的東西
BONUS = 2000 # Money player earns while passing start              #經過起點會獲得的金額
HOSPITAL_POS = 8 # map number of HOSPITAL_POS 					   #醫院在地圖上是第幾個位置
BUILDLIMIT = 3 # Maximum building number on one Location 		   #建築物最多可以蓋幾棟

# UI Size
BTNWIDTH = 125			#GO按鈕的寬度
BTNHEIGHT = 125			#GO按鈕的高度
ARROWWIDTH = 22			#人物寬度
ARROWHEIGHT = 36		#人物高度
DICEWIDTH = 60			#骰子寬度
DICEHEIGHT = 60			#骰子高度
BUILDINGWIDTH = 30		#建築物寬度
BUILDINGHEIGHT = 30		#建築物高度
BLANKWIDTH = 25		
BLANKHEIGHT = 25   	

# Define Color
WHITE = (255,255,255)
BLACK = (0,0,0)

# Game Images 			#匯入地圖的圖片

images_name=['start','forest1','hospital','camping','dog1','dog2','dog3','dog4','dog5','dog6','dog7','dog8','cat1','cat2','cat3','cat4','cat5',
'cat6','cat7','cat8','cat9','cat10','angry1','angry2','fortune1','fortune2']
images_url=['images/start.png','images/forest1.jpg','images/hospital1.png','images/camping.jpg','images/dog1.jpg','images/dog2.jpg',
'images/dog3.jpg','images/dog4.jpg','images/dog5.jpg','images/dog6.jpeg','images/dog7.jpeg','images/dog8.jpeg','images/cat1.jpg',
'images/cat2.jpg','images/cat3.jpg','images/cat4.jpg','images/cat5.jpg','images/cat6.jpg','images/cat7.jpeg','images/cat8.jpeg',
'images/cat9.jpg','images/cat10.jpg','images/angry1.jpg','images/angry2.jpg','images/fortune_1.jpg','images/fortune_2.jpg']
for i in range(len(images_name)):
	IMAGES[images_name[i]]=pygame.transform.scale(pygame.image.load(images_url[i]),(BOXWIDTH,BOXHEIGHT))
IMAGES['background']=pygame.transform.scale(pygame.image.load('images/BG-01.jpg'),(930,570))

UI_IMAGES = { 			#匯入根據使用者操作而會改變的圖片
	'go_btn_down' : pygame.transform.scale(pygame.image.load('images/go_btn_down.png'),(BTNWIDTH,BTNHEIGHT)),
	'go_btn_up' : pygame.transform.scale(pygame.image.load('images/go_btn_up.png'),(BTNWIDTH,BTNHEIGHT)),
	'arrow_up1' : pygame.transform.scale(pygame.image.load('images/person-02-02.png'),(ARROWWIDTH,ARROWHEIGHT)),
	'arrow_down1' : pygame.transform.scale(pygame.image.load('images/person-02-02.png'),(ARROWWIDTH,ARROWHEIGHT)),
	'arrow_left1' : pygame.transform.scale(pygame.image.load('images/person-03-02.png'),(ARROWHEIGHT,ARROWWIDTH)),
	'arrow_right1' : pygame.transform.scale(pygame.image.load('images/person-03-02.png'),(ARROWHEIGHT,ARROWWIDTH)),
	'arrow_up2' : pygame.transform.scale(pygame.image.load('images/person-02-04.png'),(ARROWWIDTH,ARROWHEIGHT)),
	'arrow_down2' : pygame.transform.scale(pygame.image.load('images/person-02-04.png'),(ARROWWIDTH,ARROWHEIGHT)),
	'arrow_left2' : pygame.transform.scale(pygame.image.load('images/person-03-04.png'),(ARROWHEIGHT,ARROWWIDTH)),
	'arrow_right2' : pygame.transform.scale(pygame.image.load('images/person-03-04.png'),(ARROWHEIGHT,ARROWWIDTH)),
	'arrow_up3' : pygame.transform.scale(pygame.image.load('images/person-02-05.png'),(ARROWWIDTH,ARROWHEIGHT)),
	'arrow_down3' : pygame.transform.scale(pygame.image.load('images/person-02-05.png'),(ARROWWIDTH,ARROWHEIGHT)),
	'arrow_left3' : pygame.transform.scale(pygame.image.load('images/person-03-05.png'),(ARROWHEIGHT,ARROWWIDTH)),
	'arrow_right3' : pygame.transform.scale(pygame.image.load('images/person-03-05.png'),(ARROWHEIGHT,ARROWWIDTH)),
	'dice1' : pygame.transform.scale(pygame.image.load('images/dice1.jpeg'),(DICEWIDTH,DICEHEIGHT)),
	'dice2' : pygame.transform.scale(pygame.image.load('images/dice2.jpeg'),(DICEWIDTH,DICEHEIGHT)),
	'dice3' : pygame.transform.scale(pygame.image.load('images/dice3.jpeg'),(DICEWIDTH,DICEHEIGHT)),
	'dice4' : pygame.transform.scale(pygame.image.load('images/dice4.jpeg'),(DICEWIDTH,DICEHEIGHT)),
	'dice5' : pygame.transform.scale(pygame.image.load('images/dice5.jpeg'),(DICEWIDTH,DICEHEIGHT)),
	'dice6' : pygame.transform.scale(pygame.image.load('images/dice6.jpeg'),(DICEWIDTH,DICEHEIGHT)),
	'building1' : pygame.transform.scale(pygame.image.load('images/dog-03.png'),(BUILDINGWIDTH,BUILDINGHEIGHT)),
	'building2' : pygame.transform.scale(pygame.image.load('images/cat02-03.png'),(BUILDINGWIDTH,BUILDINGHEIGHT)),
	'building3' : pygame.transform.scale(pygame.image.load('images/cat02-04.png'),(BUILDINGWIDTH,BUILDINGHEIGHT))
}

FUNCTION = {			#每一格的功能對應到的數字
	'start' : 0,
	'attack' : 1,
	'hospital' : 2,
	'cute' : 3,
	'estate' : 4,
	'fortune' : 5,
}

DIRECT = {				#人物會需要用到的上下左右方向
	'_left' : 0,
	'_right' : 1,
	'_up' : 2,
	'_down' : 3			
}

MESSAGE_BOX_TYPE = {	#跳出來的文字視窗的種類
	'OK' : 0,
	'OK|CANCEL' : 1,
	'YES|NO' : 2
}


def main():
	map_surface, map_pos, game_map, building_pos, arrow_pos, arrow_dir = SetGameMap(HBOXNUM,VBOXNUM)	# Setup game map(def在274行)→(地圖畫布,[地圖左座標,右座標,寬度,長度],建築物位置,箭頭位置,箭頭方向)
	blank_pos = [map_pos[0] - 60,map_pos[1] - 60,map_pos[2] + 120,map_pos[3] + 120]						#地圖背後白色那片畫布的左座標，上座標，寬度，長度
	print(map_pos[2] + 120,map_pos[3] + 120)
	BOXNUM = len(game_map)																			 	#知道總共有幾個格子
	
	##################################################################################################################################################################################
	# Fill content into game map
	##################################################################################################################################################################################

	inp=easygui.enterbox('請輸入三位玩家的姓名(英文)\n          Ex: AAA BBB CCC','Name')					#請玩家輸入姓名
	name=[str(i) for i in inp.split()]																	#將玩家的姓名存到串列中(name)

	location_image_name=['start','cat1','cat3','dog1','fortune2','cat2','cat5','dog2','hospital','dog3','cat4','dog4','forest1','cat6','dog5','cat7','dog8','fortune1','angry1','angry2','cat10','dog7']
	function_name=['start','estate','estate','estate','fortune','estate','estate','estate','hospital','estate','estate','estate','attack','estate','estate','estate','estate','estate','fortune','estate','cute','estate','estate','estate']
	money=[[-1,-1,-1],[3000,1500,1000],[3000,1500,1000],[3000,1500,1000],[3000,1500,1000],[1500,900,800],[3000,1500,1000],[1500,900,800],[-1,-1,-1],[1500,900,800],[3000,1500,1000],[1500,900,800],[-1,-1,-1],[3000,1500,1000],[1500,900,800],[3000,1500,1000],[3000,1500,1000],[1500,900,800],[1500,900,800],[9000,5000,4000],[-1,-1,-1],[9000,5000,4000],[3000,1500,1000],[1500,900,800]]
	location_list = []
	for i in range(len(location_image_name)):        #將地點的照片及資訊加到串列當中→(第幾格,圖片,對應到game_map中的左座標及上座標,該格的功用,花費,加蓋花費,其他人過路費)
    	if i==8:
    		location_list.append(Location(HOSPITAL_POS,IMAGES['hospital'],game_map[HOSPITAL_POS],FUNCTION['hospital'],-1,-1,-1))
		else:
			location_list.append(Location([i],IMAGES[location_image_name[i]],game_map[i],FUNCTION[function[i]],money[i][0],money[i][1],money[i][2]))


			
	for location in location_list:													#把圖片放到地圖上(原本SetGameMap當中return的map_surface只有地圖的空格子+文字)
		location.render(map_surface)												# map_surface最後為一個完整的地圖

	##################################################################################################################################################################################

	##################################################################################################################################################################################
	# Setup Game UI
	##################################################################################################################################################################################

	ui_list = []
	go_btn = Button(UI_IMAGES['go_btn_up'],UI_IMAGES['go_btn_down'],(1050,440))		#匯入按鈕的圖片及控制位置
	ui_list.append(go_btn)															#利用game_class中定義的class來指定button中的變數→ __init__(self,btn_up,btn_down,pos)
	step = 1 																		# Initial dice point

	players = []																	#遊戲人數的串列
	players.append(Player(1,INITMONEY))												#利用game_class中定義的class來指定player中的變數→ __init__(self,num,money)
	players.append(Player(2,INITMONEY))
	players.append(Player(3,INITMONEY))
	player_turn = 1
	PLAYERNUM = len(players)

	game_record = []   																#紀錄每一輪玩家的金錢變化
	for i in range(PLAYERNUM):														#看有幾位玩家就創造幾個空字串，之後會將每一輪的金錢放進去
		game_record.append([])

	offset = []																		#紀錄箭頭
	for i in range(PLAYERNUM):
		offset.append([(0,(ARROWWIDTH + 10)*i),(0,(ARROWWIDTH )*i),((ARROWWIDTH + 10)*i,0),((ARROWWIDTH + 10)*i,0)])

	building_offset = []															#紀錄建築物
	for i in range(BUILDLIMIT):
		building_offset.append([(0,(BUILDINGHEIGHT + 5)*i),(0,(BUILDINGHEIGHT + 5)*i),((BUILDINGWIDTH + 5)*i,0),((BUILDINGWIDTH + 5)*i,0)])

	##################################################################################################################################################################################

	##################################################################################################################################################################################
	# Game loop
	##################################################################################################################################################################################

	while True:																		#死迴圈確保一直顯示
		RecordData(players,game_record,location_list)
		DrawAll(blank_pos,map_pos,map_surface,arrow_pos,arrow_dir,building_pos,building_offset,step,ui_list,location_list,players,offset,name)

		for event in pygame.event.get():             								#遍歷所有事件

			if event.type == pygame.MOUSEBUTTONDOWN:
			
				if go_btn.isHover():
					player_cur = players[player_turn - 1]							#看現在的玩家是哪一位
					player_turn += 1
					if player_turn == len(players):																		
						player_turn = 0
						RecordData(players,game_record,location_list)
						for i in players:
							print('estate:',i.asset)
													
					player_cur.freeze_turn -= 1 									#如果freeze_turn>0，則判斷玩家在醫院當中，凍結步數並且跳出文字視窗告知
					pygame.time.delay(60) 
					if player_cur.freeze_turn > 0:
						pygame.time.delay(60) 
						hospital.play()
						CreateMessageBox(name[player_cur.player_num-1] + ' is in hospital!','hospital!',MESSAGE_BOX_TYPE['OK'])
						continue

					step = random.randint(1,6)										#擲骰子(隨機1~6)
					for i in range(6):												#讓骰子隨機跑
						DrawAll(blank_pos,map_pos,map_surface,arrow_pos,arrow_dir,building_pos,building_offset,i+1,ui_list,location_list,players,offset,name)  #介面只要有更新就將所有東西重新繪製出來
						pygame.display.update()
						

					for i in range(step):											#讓玩家一格一格的跳	
						pass_start = player_cur.Move(1,BOXNUM,BONUS)				#利用game_class當中的Player.Move判斷玩家是否有經過起點，有的話就有bonus+跳出文字視窗
						pygame.time.delay(60) 
						if pass_start is True:
							moneyget.play()
							CreateMessageBox(name[player_cur.player_num-1] + ' pass start and get ' + str(BONUS) + ' cans!','Bonus!',MESSAGE_BOX_TYPE['OK'])
						DrawAll(blank_pos,map_pos,map_surface,arrow_pos,arrow_dir,building_pos,building_offset,step,ui_list,location_list,players,offset,name)
						pygame.display.update()
						GAMECLOCK.tick(3)
						

					# Execute loaction effect
					location = location_list[player_cur.pos]						#看玩家現在在的那一格是哪裡存成location
					attack_flag=0													#拿來判斷玩家是因為被攻擊而走到醫院(1)，或是自己丟骰子走到醫院去(0)，這兩者都要凍結玩家步數
					if location.func == FUNCTION['attack']:							#如果玩家被攻擊的話，要重新繪製視窗(重複168行的東西)
						# Redraw game window
						RecordData(players,game_record,location_list)
						DrawAll(blank_pos,map_pos,map_surface,arrow_pos,arrow_dir,building_pos,building_offset,step,ui_list,location_list,players,offset,name)
						pygame.display.update()

						player_cur.Transport(HOSPITAL_POS)							#將玩家的位置移到醫院那一格
						player_cur.freeze_turn = 2									#讓玩家的凍結格數為2，並且印出文字視窗
						attack_flag=1
						pygame.time.delay(60) 
						hospital.play()
						CreateMessageBox(name[player_cur.player_num-1] + ' is attacked! Go to Hospital!','Go to Hospital!',MESSAGE_BOX_TYPE['OK'])
						GAMECLOCK.tick(2)											#2豪秒內更新視窗

					elif location.func == FUNCTION['hospital']:						#如果走到醫院那格的話，要凍結步數(freeze_turn)
						if not attack_flag:
							player_cur.freeze_turn = 2
							pygame.time.delay(60) 
							hospital.play()
							CreateMessageBox(name[player_cur.player_num-1] + ' is in hospital！','Hospital!',MESSAGE_BOX_TYPE['OK'])

					elif location.func == FUNCTION['cute']:							#如果停在露營那格，玩家的金錢會增加2000
							player_cur.money+=2000
							moneyget.play()					                                                            
							CreateMessageBox(name[player_cur.player_num-1]+' take cuties go to camping. Get 2000 cans.','Go Camping',MESSAGE_BOX_TYPE['OK']		)					

					elif location.func == FUNCTION['fortune']:						#若走到命運格子，要重新繪製地圖
						RecordData(players,game_record,location_list)				
						DrawAll(blank_pos,map_pos,map_surface,arrow_pos,arrow_dir,building_pos,building_offset,step,ui_list,location_list,players,offset,name)
						pygame.display.update()
						
						cans=['4000','5000','6000','700','1000','2000','3000','9000','3000']
						i=random.randint(0,8)
						Lose_Get=random.randint(0,2)

						if Lose_Get == 1 or Lose_Get == 2:							#命運是不好的(lose)	
							story=random.randint(1,6)
							if story == 1:
								ohno.play()
								CreateMessageBox(name[player_cur.player_num-1]+' paid spousal support. Lose '+cans[i]+' cans.','Fortune',MESSAGE_BOX_TYPE['OK'])
								player_cur.money-=int(cans[i])
							elif story == 2:
								ohno.play()                                                           
								CreateMessageBox(name[player_cur.player_num-1]+' bought luxuary stuff. Lose '+cans[i]+' cans.','Fortune',MESSAGE_BOX_TYPE['OK']) 
								player_cur.money-=int(cans[i])
							elif story == 3:
								ohno.play()                                                   			    						
								CreateMessageBox(name[player_cur.player_num-1]+' lost the wallet. Lose '+cans[i]+' cans.','Fortune',MESSAGE_BOX_TYPE['OK'])     
								player_cur.money-=int(cans[i])
							elif story == 4:										#該玩家的一些cans平分給剩下的玩家
								ohno.play()
								CreateMessageBox(name[player_cur.player_num-1]+' lost '+cans[i]+' cans. Others get '+str(int(int(cans[i])/(len(players)-1)))+' cans.','Fortune',MESSAGE_BOX_TYPE['OK'])
								player_cur.money-=int(cans[i])
								for x in players:
									if x != player_cur:
										x.money+=int(int(cans[i])/(len(players)-1))
										print(x,player_cur)
							elif story == 5:										#該玩家每塊地跟貓狗都沒有了
								ohno.play()
								CreateMessageBox(name[player_cur.player_num-1]+' lost all of dogs.','Fortune',MESSAGE_BOX_TYPE['OK'])
								for location in location_list:
									if location.owner==player_cur.player_num:
										location.owner=-1
										location.buildings=0		
							elif story == 6:										#平分大家的錢
								ohno.play()
								CreateMessageBox('Communism!!','Our cans!',MESSAGE_BOX_TYPE['OK'])
								m=0
								for i in players:
									m+=i.money
								for i in players:
									i.money=int(m/3)

						elif Lose_Get ==0:											#命運是好的(get)
							#story=random.randint(1,6)					                                                    					    						
							story=4
							if story == 1:
								moneyget.play()					                                                            
								CreateMessageBox(name[player_cur.player_num-1]+' won the lottery. Get '+cans[i]+' cans.','Fortune',MESSAGE_BOX_TYPE['OK'])		
								player_cur.money+=int(cans[i])
							elif story == 2:
								moneyget.play()                                                            
								CreateMessageBox(name[player_cur.player_num-1]+' got the severance pay. Get '+cans[i]+' cans.','Fortune',MESSAGE_BOX_TYPE['OK'])
								player_cur.money+=int(cans[i])
							elif story == 3:
								moneyget.play() 						
								CreateMessageBox(name[player_cur.player_num-1]+' got the compensation. Get '+cans[i]+' cans.','Fortune',MESSAGE_BOX_TYPE['OK'])
								player_cur.money+=int(cans[i])
							elif story == 4:										#剩下玩家的一些錢給該玩家
								moneyget.play()
								CreateMessageBox(name[player_cur.player_num-1]+' got '+cans[i]+' cans. Others lost '+str(int(int(cans[i])/(len(players)-1)))+' cans.','Fortune',MESSAGE_BOX_TYPE['OK'])
								player_cur.money+=int(cans[i])
								for x in players:
									if x != player_cur:
										x.money-=int(int(cans[i])/(len(players)-1))
							elif story == 5:										#該玩家每塊地的貓狗都會多一隻
								moneyget.play()
								CreateMessageBox('All '+name[player_cur.player_num-1]+'\'s dog gave birth.','Fortune',MESSAGE_BOX_TYPE['OK'])
								for location in location_list:	
									if location.owner==player_cur.player_num and location.buildings<BUILDLIMIT:
										location.buildings+=1
										location.tolls *= location.buildings
							elif story == 6:										#平分大家的錢
								moneyget.play()
								CreateMessageBox('Communism!!','Our cans!',MESSAGE_BOX_TYPE['OK'])
								m=0
								for i in players:
									m+=i.money
								for i in players:
									i.money=int(m/3)
						for j in range(len(players)):								#判斷經過命運之後，是否有玩家破產，若破產即跳出文字視窗，遊戲結束
							if players[j].money<0:
								#players[j].money=0
								RecordData(players,game_record,location_list)
								DrawAll(blank_pos,map_pos,map_surface,arrow_pos,arrow_dir,building_pos,building_offset,step,ui_list,location_list,players,offset,name)
								pygame.display.update()
								ohno.play()                                                           
								CreateMessageBox(name[players[j].player_num-1] + ' has to lose ' + str(cans[i]) + ' cans.\n' + name[players[j].player_num-1] + ' goes bankrupt!','Bankrupt!',MESSAGE_BOX_TYPE['OK']) 
								RecordData(players,game_record,location_list)
								player_cur,location_list=chance(players[j],location_list,game_record,name)  
								
					elif location.func == FUNCTION['estate']:						#如果玩家走到房地產的話，要重新繪製視窗(重複168行的東西)
						# Redraw game window
						RecordData(players,game_record,location_list)
						DrawAll(blank_pos,map_pos,map_surface,arrow_pos,arrow_dir,building_pos,building_offset,step,ui_list,location_list,players,offset,name)
						pygame.display.update()

						if (location.owner == -1) and (player_cur.money >= location.cost):     #判斷該地是否有所有者 & 玩家所擁有的金錢是否大於購買價，都符合的話即跳出文字視窗詢問是否要購買
							pygame.time.delay(60) 
							ans = CreateMessageBox('Do you want to adopt this cuties? (cost ' + str(location.cost) + ' cans)','Purchase Chance!',MESSAGE_BOX_TYPE['YES|NO'])
							if ans is True:											#玩家要購買該地
								meow.play()
								player_cur.money -= location.cost 					#扣掉該地的錢
								location.owner = player_cur.player_num 				#將該地標成玩家的
								location.buildings += 1								#建一個建築物
								print(name[player_cur.player_num-1] + ' has: ' + str(player_cur.money))		#在cmd印出玩家剩下的錢有多少
							else:
								barks.play()
						
						elif (location.owner > 0) and (location.owner != player_cur.player_num) and (players[location.owner - 1].freeze_turn <= 0):		#如果該地的所有者不是該玩家且所有者不在監獄的話
							if location.tolls > player_cur.money:					#路過該地的費用>玩家的錢，跳出玩家破產的文字視窗
								ohno.play()                                             
								CreateMessageBox(name[player_cur.player_num-1] + ' needs to pay ' + str(location.tolls) + ' cans.\n' +name[player_cur.player_num-1]+ ' goes bankrupt!','Bankrupt!',MESSAGE_BOX_TYPE['OK'])
								players[location.owner - 1].money += player_cur.money
								player_cur.money-=location.tolls  					#所有者的錢數+費用
								RecordData(players,game_record,location_list)
								for i in players:
									print(':',i.asset,'player',player_cur.player_num)		#紀錄玩家們的金錢變化
								player_cur,location_list=chance(player_cur,location_list,game_record,name)
																					#遊戲結束並且印出折線圖
							else:
								tolls = location.tolls								#如果玩家可以負擔路過該地的費用的話，印出需付錢的文字視窗
								player_cur.money -= tolls							#玩家的錢數-費用
								players[location.owner - 1].money += tolls			#所有者的錢數+費用
								ohno.play()                                                           
								CreateMessageBox(name[player_cur.player_num-1]+ ' pays ' + str(tolls) + ' cans to ' + name[location.owner-1],'Pay tolls!',MESSAGE_BOX_TYPE['OK'])
								print(name[player_cur.player_num-1] + ' has: ' + str(player_cur.money))				#在cmd印出玩家剩下的錢
								print(name[location.owner-1] + ' has: ' + str(players[location.owner - 1].money))	#在cmd印出其他玩家剩下的錢

						elif (location.owner == player_cur.player_num) and (player_cur.money >= location.extend_cost) and (location.buildings < BUILDLIMIT):	#如果該地的所有者是該玩家且玩家的錢數能負擔加蓋且建築物尚未達到上限的話
							ans = CreateMessageBox('Do you want to support her given birth? (cost ' + str(location.extend_cost) + ' cans)','Extend Chance!',MESSAGE_BOX_TYPE['YES|NO'])	#跳出是否要加蓋一個房子的文字視窗
							if ans is True:											#若玩家要加蓋
								player_cur.money -= location.extend_cost			#玩家的錢數-加蓋的錢
								location.buildings += 1								#該地建築物+1
								location.tolls *= location.buildings 				#該地的費用加成
								print(name[player_cur.player_num-1] + ' has: ' + str(player_cur.money))	#在cmd印出玩家所剩的錢


			elif event.type == QUIT:												#如果單擊關閉視窗，則退出
				sys.exit(0)

		pygame.display.update()			
		GAMECLOCK.tick(FPS)

	##################################################################################################################################################################################


def SetGameMap(h_box,v_box):   		                  								#定義地圖長怎樣(h_box、v_box為格數)
	map_left = WINDOWWIDTH/2 - (h_box/2)*BOXWIDTH		
	map_right = WINDOWWIDTH/2 + (h_box/2)*BOXWIDTH
	map_top = WINDOWHEIGHT/2 - (v_box/2)*BOXHEIGHT
	map_bottom = WINDOWHEIGHT/2 + (v_box/2)*BOXHEIGHT

	map_width = map_right - map_left
	map_height = map_bottom - map_top	
	map_surface = pygame.Surface((map_width,map_height), pygame.SRCALPHA) 			#建立畫布
	print(map_width,map_height)	
	start_left = map_width - BOXWIDTH									  			#一堆奇怪的算式計算長寬
	start_height = map_height - BOXHEIGHT
	end_left = 0
	end_height = 0
	game_map = [None]*(h_box*2 + (v_box - 2)*2)
	building_pos = [None]*(h_box*2 + (v_box - 2)*2)
	arrow_pos = [None]*(h_box*2 + (v_box - 2)*2)
	arrow_dir = [None]*(h_box*2 + (v_box - 2)*2)

	# Draw horizontal boxes on map   #繪製水平方向的格子
	for i in range(h_box):
		#下面那排格子
		rect_left = start_left - i*BOXWIDTH
		rect_top = start_height
		pygame.draw.rect(map_surface,BLACK,[rect_left,rect_top,BOXWIDTH,BOXHEIGHT],3)   #畫製矩形(地圖每一格)→(畫布,顏色,[左座標,上座標,寬度,高度],線寬)
		text = font_obj.render(str(i),True,WHITE,(0,0,0,0))								#文字(每一格的編號)→(文字,平滑值,文字顏色,背景顏色)
		text_rect = text.get_rect()														#獲得文字的矩形大小
		text_rect.center = (rect_left + BOXWIDTH/2,rect_top + BOXHEIGHT/2)				#定義文字方塊的中心點
		map_surface.blit(text,text_rect)												#用blit將文字繪製上去
		game_map[i] = [rect_left, rect_top]												#將每一個格子的左座標，上座標存起來
		building_pos[i] = [rect_left + map_left, rect_top + map_top + BOXHEIGHT]		#將每一個建築物的左座標，上座標存起來
		arrow_pos[i] = [rect_left + map_left, rect_top + map_top + BOXHEIGHT + BLANKHEIGHT]   #將每一個箭頭的左座標，上座標存起來
		arrow_dir[i] = '_down'																  #定義箭頭的方向
		#上面那排格子
		rect_left = end_left + i*BOXWIDTH
		rect_top = end_height
		pygame.draw.rect(map_surface,BLACK,[rect_left,rect_top,BOXWIDTH,BOXHEIGHT],3)
		text = font_obj.render(str(i + h_box + v_box - 2),True,WHITE,(0,0,0,0))
		text_rect = text.get_rect()
		text_rect.center = (rect_left + BOXWIDTH/2,rect_top + BOXHEIGHT/2)
		map_surface.blit(text,text_rect)
		game_map[i + h_box + v_box - 2] = [rect_left,rect_top]
		building_pos[i + h_box + v_box - 2] = [rect_left + map_left, rect_top + map_top - BUILDINGHEIGHT]
		arrow_pos[i + h_box + v_box - 2] = [rect_left + map_left, rect_top + map_top - ARROWHEIGHT - BLANKHEIGHT]
		arrow_dir[i + h_box + v_box - 2] = '_up'

	# Draw vertical boxes on map      #繪製垂直方向的格子
	for i in range(1,v_box - 1):
		#左邊那排格子
		rect_left = start_left
		rect_top = start_height - i*BOXHEIGHT
		pygame.draw.rect(map_surface,BLACK,[rect_left,rect_top,BOXWIDTH,BOXHEIGHT],3)
		text = font_obj.render(str(h_box*2 + (v_box - 2)*2 - i),True,WHITE,(0,0,0,0))
		text_rect = text.get_rect()
		text_rect.center = (rect_left + BOXWIDTH/2,rect_top + BOXHEIGHT/2)
		map_surface.blit(text,text_rect)
		game_map[h_box*2 + (v_box - 2)*2 - i] = [rect_left,rect_top]
		building_pos[h_box*2 + (v_box - 2)*2 - i] = [rect_left + map_left + BOXWIDTH, rect_top + map_top]
		arrow_pos[h_box*2 + (v_box - 2)*2 - i] = [rect_left + map_left + BOXWIDTH + BLANKWIDTH, rect_top + map_top]
		arrow_dir[h_box*2 + (v_box - 2)*2 - i] = '_right'
		#右邊那排格子
		rect_left = end_left
		rect_top = start_height - i*BOXHEIGHT
		pygame.draw.rect(map_surface,BLACK,[rect_left,rect_top,BOXWIDTH,BOXHEIGHT],3)
		text = font_obj.render(str(h_box + i - 1),True,WHITE,(0,0,0,0))
		text_rect = text.get_rect()
		text_rect.center = (rect_left + BOXWIDTH/2,rect_top + BOXHEIGHT/2)
		map_surface.blit(text,text_rect)
		game_map[h_box + i - 1] = [rect_left,rect_top]
		building_pos[h_box + i - 1] = [rect_left + map_left - BUILDINGWIDTH, rect_top + map_top]
		arrow_pos[h_box + i - 1] = [rect_left + map_left - ARROWHEIGHT - BLANKWIDTH, rect_top + map_top]
		arrow_dir[h_box + i - 1] = '_left'

	return map_surface, (map_left, map_top, map_width, map_height), game_map, building_pos, arrow_pos, arrow_dir


def DrawGUI(ui_list):		 							   #利用game_class中定義的button來先判斷是否有點擊到GO按鈕，有或沒有各自繪製出指定的按鈕		
	for ui in ui_list:									
		ui.render(window)
	return


def DrawPlayer(player_list,arrow_pos,arrow_dir,offset):	   #從arrow_pos中找出現在Player對應的箭頭格子及箭頭方向，最後繪製出箭頭
	for player in player_list:
		pos_x = arrow_pos[player.pos][0] + offset[player.player_num - 1][DIRECT[arrow_dir[player.pos]]][0]
		pos_y = arrow_pos[player.pos][1] + offset[player.player_num - 1][DIRECT[arrow_dir[player.pos]]][1]
		player.render(window,UI_IMAGES['arrow' + arrow_dir[player.pos] + str(player.player_num)],(pos_x,pos_y))
	return


def DrawBuildings(location_list,building_pos,building_offset,arrow_dir):	#從Location中找出對應到的建築物位置及方向，最後匯出建築物
	for location in location_list:
		for i in range(location.buildings):
			pos_x = building_pos[location.num][0] + building_offset[i][DIRECT[arrow_dir[location.num]]][0]
			pos_y = building_pos[location.num][1] + building_offset[i][DIRECT[arrow_dir[location.num]]][1]
			window.blit(UI_IMAGES['building' + str(location.owner)],(pos_x,pos_y))


def DrawPlayerData(players,name):								#利用game_class中來計算player的金錢有多少，並且在左上角將資訊繪製出來
	data_offset = 50
	for player in players:
		text = font_obj.render('%5s%s：%d'% (name[player.player_num-1],'\'s cans',player.money),True,WHITE,(0,0,0,0))
		text_rect = text.get_rect()
		text_rect.center = (100,data_offset)
		window.blit(text,text_rect)
		data_offset += 50
	data_offset = 50
	for player in players:
		text = font_obj.render('%5s%s：%d'% (name[player.player_num-1],'\'s asset',player.asset),True,WHITE,(0,0,0,0))
		text_rect = text.get_rect()
		text_rect.center = (1150,data_offset)
		window.blit(text,text_rect)
		data_offset += 50
	return

	
def DrawAll(blank_pos,map_pos,map_surface,arrow_pos,arrow_dir,building_pos,building_offset,step,ui_list,location_list,players,offset,name):  #介面只要有更新就將所有東西重新繪製出來
	window.fill((0,0,0))  														#填充顏色(設定為0，執不執行這行程式碼都一樣)
	pygame.draw.rect(window,WHITE,blank_pos,0)									#把地圖後面的白色矩形畫布繪製出來
	window.blit(IMAGES['background'],(map_pos[0] - 60,map_pos[1] - 60)) 		#將整個地圖畫到視窗上
	window.blit(map_surface,(map_pos[0],map_pos[1])) # Draw game map 			#將整個地圖畫到視窗上
	window.blit(UI_IMAGES['dice' + str(step)],(1080,375))   					#匯入骰子的圖片及控制位置
	DrawGUI(ui_list) # Draw DrawGUI 											#(def在350行)將GO按鈕繪製出來
	DrawPlayer(players,arrow_pos,arrow_dir,offset)								#(def在356行)將箭頭繪製出來
	DrawBuildings(location_list,building_pos,building_offset,arrow_dir)			#(def在364行)將建築物繪製出來
	DrawPlayerData(players,name)														#(def在371行)將玩家資訊(金錢數)繪製出來


def CreateMessageBox(message,title,style):					#繪製跳出來的文字視窗，並且判斷是哪一種的視窗類型，根據使用者的選擇回傳ans並且在cmd印出玩家的選擇

	print(platform.system())
	if platform.system() == 'Windows':
		if style == MESSAGE_BOX_TYPE['OK']:
			ans = easygui.msgbox(message,title)
		elif style == MESSAGE_BOX_TYPE['OK|CANCEL']:
			ans = easygui.ccbox(message,title)
		elif style == MESSAGE_BOX_TYPE['YES|NO']:
			ans = easygui.ynbox(message,title)
	elif platform.system() == 'Darwin':
		print(platform.system())
		r = os.system("osascript -e \'Tell application \"System Events\" to display dialog \" "+ message +" \" with title \" "+ title +" \"\'")
		ans = True if r == 0 else False
	print(ans)
	return ans


def RecordData(players,game_record,location_list):			#紀錄每一倫玩家的資產變化(資產包含現金、土地、貓狗數 → 皆化成數值)
	for player in players:
		player.asset=0
		for loc in location_list:
			if loc.owner==player.player_num:
				player.asset+= (loc.buildings-1)*loc.extend_cost+loc.cost
		player.asset+=player.money
		game_record[player.player_num - 1].append(player.asset)
	return


def chance(players,location,game_record,name):
	if players.asset<0:
		CreateMessageBox(name[players.player_num-1]+' goes Bankrupt.','Bankrupt',MESSAGE_BOX_TYPE['OK'])		
		GameOver(game_record,name)
	else:
		CreateMessageBox(name[players.player_num-1]+' sold all the pets.','Bankrupt',MESSAGE_BOX_TYPE['OK'])
		for loc in location:
			if loc.owner == players.player_num:
				players.money+=(loc.buildings-1)*loc.extend_cost+loc.cost
				loc.buildings=0
				loc.owner=-1
		if players.money<0:
			GameOver(game_record,name)
		return(players,location)


def GameOver(game_record,name):								#有人破產之後，用圖表表示出遊戲中各玩家的金錢變化折線圖
	print('gg')
	index = list(range(1,len(game_record[0]) + 1))
	player_num = 1
	for player_data in game_record:
		plt.plot(index,player_data,label = name[player_num-1])
		player_num += 1
	plt.title('Total asset')
	plt.legend()
	plt.show()
	terminate()


def terminate():											#在印完折線圖之後，完全退出遊戲
	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	path='b.mp3'											#將音樂加至遊戲的bgm
	pygame.mixer.init()
	pygame.mixer.music.load(path)
	pygame.mixer.music.play(-1)
	tiltle=easygui.msgbox(msg='準備好進入寵物當家們的世界了嗎?',title='寵物當家',ok_button='等不及了')		#在遊戲加上前導的文字
	msg=easygui.msgbox(msg='歡迎來到寵物們的世界，在這張地圖裡，人人都是貓奴、狗奴，可愛的貓貓和狗狗們，在這個世界中都有屬於自己的領地。',title='寵物當家')
	msg=easygui.msgbox(msg='當你走進他們的領地，可以送上罐頭食物，讓浪浪跟你回家，當你想讓整個家更加完整，可以多添貓寶寶或狗寶寶，一旦毛小孩認定了一個主人，對於外來者的侵略，小心出於防備而被咬，失去身上的罐頭，讓浪浪有個家吧 ! 也要小心突發的攻擊喔！',title='寵物當家')
	main()
	