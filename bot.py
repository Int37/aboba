import pickle
from telebot import types
import telebot
from telebot import apihelper
import codecs
import random
import os
api ='967616104:AAGZtHKTzTtqPs683LP0D0900lNmOqSrEjY'
while(True):
    try:
        #указываем функции
        def change_num(text):
            cmap={'0':'0️⃣', '1':'1️⃣', '2':'2️⃣', '3':'3️⃣', '4':'4️⃣', '5':'5️⃣', '6':'6️⃣', '7':'7️⃣', '8':'8️⃣', '9':'9️⃣', '10':'🔟'}
            res=''
            for i in text:
                if (i in cmap):
                    res+=cmap[i]
                else:
                    res+=i
            return res


        class Place(object):
            def __init__(self,father,name,descr,pic,aid=0):
                self.name = name
                self.descr = descr
                self.pic = pic
                self.father = father
                self.aid=aid
            def text(self):
                text = self.name + '\n'
                text += self.descr
                return text
            def get_val_comm(self):
                return [0 ]
            def __getitem__(self, key) :
                if(key == 0):
                    return self.father
            def send(self,chat):
                global bot
                img = open(self.pic, 'rb')
                bot.send_photo(chat, img, caption=self.text())

        def send_default_command(chat):
            bot.send_message(chat, "команда не найдена")
        class Menu(object ):
            def __init__(self,name,header,father,aid=0):
                self.items = []
                self.name = name
                self.father = father
                self.header = header
                self.aid=aid
            def __getitem__(self, key) :
                if(key == 0):
                    return self.father
                return self.items[key-1]
            def remove(self,i):
                return self.items.pop(i-1)
            def append(self,a):
                self.items.append(a)
            def text(self):
                text = self.header + '\n'
                for i in range(len(self.items)):
                    text += str(i+1) + ' '+self.items[i].name + '\n'
                return text
            def get_val_comm(self):
                return list(range(len(self.items)+1))
            def send(self,chat):
                global bot
                send_message(chat, self.text())
        def change_name(curr,message):
            users_state[message.chat.id].name= message.text
        def change_describ(curr,message):
            users_state[message.chat.id].descr= message.text
        def change_photo(curr,message):
            send_message(message.chat.id,"Пришлите фото!")
        def change_header_menu(curr,message):
            users_state[message.chat.id].name= message.text
        def change_header(curr,message):
            users_state[message.chat.id].header= message.text
        def remove_other_item(item,main):
            for i,j in users_state.items():
                if(j.name==item.name):
                    users_state[i]= main.father
                    send_message(i,"меню было удалено")
                    main.father.send(i)
            if(item.__class__.__name__ == 'Menu' and  len(item.items) != 0) :
                for i in item.items:
                    remove_other_item(i,main)
            if(item.__class__.__name__ == 'Place' and item.pic != "pic/default_pic.png"):
                try:
                    os.remove(item.pic)
                except Exception as e:
                    pass


                    
                
            
        def remove_item(curr,message):
            try:
                command = int(message.text)
            except  Exception:
                send_default_command(message.chat.id)
                return 0
            if command in range(1,len(users_state[message.chat.id].items)+1):

                item=users_state[message.chat.id].remove(command)
                remove_other_item(item,item)


            else :      
                send_default_command(message.chat.id)
        def add_item(curr,message):
            try:
                command = int(message.text)
            except  Exception:
                send_default_command(message.chat.id)

                return 0
            if(command == 1):
                users_state[message.chat.id].append(Menu("Default","Default",users_state[message.chat.id]))
            if(command == 2):
                users_state[message.chat.id].append(Place(users_state[message.chat.id],"Default Name","Deffault_desctription ","pic/default_pic.png"))
        def send_message(chat,text):
            text += '\n\n0 назад ' 
            text = change_num(text)
            bot.send_message(chat,text)
        bot = telebot.TeleBot(api)


        place_redact = Menu('start',"Что вы хотите изменить",1,aid=1)
        place_redact.father = place_redact
        place_redact.append(Menu("Изменить фото", "Скидывайте фотографию",place_redact,aid=11))
        place_redact.append(Menu("Изменить описание","Присылайте описание",place_redact,aid =12))
        place_redact.append(Menu("Изменить Название","Присылайте имя",place_redact,aid=13))


        menu_redact = Menu('start',"Что вы хотите изменить",1,aid=2)
        menu_redact.father = menu_redact
        menu_redact.append(Menu("Изменить Заголовок этого меню в меню выше", "Скидывайте заголовок",menu_redact,aid=21))
        menu_redact.append(Menu("Удалить подменю этого меню","Присылайте номер",menu_redact,aid=22))
        menu_redact.append(Menu("Изменить Заголовок ","Присылайте Загловок",menu_redact,aid=23))
        menu_redact.append(Menu("Добавить подменю этого меню","Выберите тип меню \n 1) Menu \n 2) Place",menu_redact,aid =24))
        type_admin_menu = {"Place": place_redact,"Menu": menu_redact}
        menu2func={11:change_photo,
                   12:change_describ,
                   13: change_name,
                   21:change_header_menu,
                   23:change_header,
                   22:remove_item,
                   24:add_item
                   }
        if( os.path.isfile('save.pickle') ):
            with open('save.pickle', 'rb') as f:
                users_state,admin_state,admin_list,start_menu  = pickle.load(f)
      
        else:
            
            start_menu = Menu('start',"Выберете город",1)
            start_menu.father = start_menu
            start_menu.append(Menu('Харьков',"Интересные места",start_menu))
            start_menu.append(Menu("Киев",'Инетесные места',start_menu))
            start_menu[1].append(Place(start_menu[1],'kachlka','ochen krutoe mesto','pic/iz1.jpg'))
            users_state={}
            admin_state={}
            admin_list=[345413757,154540924]

        @bot.message_handler(content_types=['photo'])
        def photo(message):
            try:
                curr_menu = users_state[message.chat.id]
            except KeyError:
                users_state[message.chat.id] = start_menu
                curr_menu = start_menu
                curr_menu.send(message.chat.id)
                return 0
            if(message.chat.id in admin_state and admin_state[message.chat.id].aid == 11):
                fileID = message.photo[-1].file_id
                file_info = bot.get_file(fileID)
                downloaded_file = bot.download_file(file_info.file_path)

                name = "pic/" + str(random.randint(0,100000000000))
                while(os.path.isfile(name)):
                    name = "pic/" + str(random.randint(0,100000000000))
                    
                with open(name, 'wb') as new_file:
                    new_file.write(downloaded_file)  
                curr_menu.pic = name
                curr_admin_menu = admin_state[message.chat.id]
                admin_state[message.chat.id] = curr_admin_menu.father
                admin_state[message.chat.id].send(message.chat.id)

        def сommand_manager(message,command,curr_menu,state) :
            global start_menu


            val_command=curr_menu.get_val_comm()

            if(command in val_command):
                state[message.chat.id] = curr_menu[command]
                curr_menu = curr_menu[command]
                curr_menu.send(message.chat.id)
            else:
                send_default_command(message.chat.id)        
        def active_function_manager(message,curr_menu,admin_state):
            curr_admin_menu = admin_state[message.chat.id]
            if curr_admin_menu.aid in menu2func:
                menu2func[curr_admin_menu.aid](curr_admin_menu,message)
                bot.send_message(message.chat.id,"Команда сделана")
                admin_state[message.chat.id] = curr_admin_menu.father
                admin_state[message.chat.id].send(message.chat.id)
                return 0

            try:
                command = int(message.text)
            except  Exception:
                send_default_command(message.chat.id)
                return 0
            if(curr_admin_menu.aid in [1,2] and command ==0   ):
                admin_state.pop(message.chat.id)
                curr_menu.send(message.chat.id)
                return 0
            сommand_manager(message,command,curr_admin_menu,admin_state)

        def admin_manager(message,command,curr_menu):
            global admin_state
            try:
                curr_admin_menu = admin_state[message.chat.id]
            except KeyError:
                admin_state[message.chat.id] = type_admin_menu[curr_menu.__class__.__name__]
                type_admin_menu[curr_menu.__class__.__name__].father = curr_menu

                admin_state[message.chat.id].send(message.chat.id)
                return 0

        @bot.message_handler(commands=['command'])
        def send_command(message):
            text = "/start - вернуться в начало \n"
            if message.chat.id in admin_list:
                text = text + "/admin id - дать пользователю права администратора \n"
                text = text + "/deadmin id - забрать у  пользователя права администратора \n"
                text = text + "/save - сохранить все \n"
                text = text + "-1 - редактирование текущего меню \n"
            send_message(message.chat.id,text)
        @bot.message_handler(commands=['admin'])
        def give_admin(message):
            if message.chat.id in admin_list:
                text= message.text
                text =text.replace("/admin"," ")
                try:
                    user = int(text)
                    admin_list.append(user)
                except  Exception:
                    send_default_command(message.chat.id)
                    return 0
                
        @bot.message_handler(commands=['deadmin'])
        def del_admin(message):
            if message.chat.id in admin_list:
                text= message.text
            
                text =text.replace("/deadmin"," ")
                try:
                    user = int(text)
                    print(user)
                    for i in range(len(admin_list)):
                        if(admin_list[i]== user):
                            break
                    print(i)
                    admin_list.pop(i)
                except  Exception as e:
                    print(e)
                    send_message(message.chat.id,"Пользователь не был удален,неверный ид")
                    return 0

                       
        @bot.message_handler(commands=['save'])
        def save_all(message):
            if (message.chat.id in admin_list):
                a= (users_state,admin_state,admin_list,start_menu)
                with open('save.pickle', 'wb') as handle:
                    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
        @bot.message_handler(commands=['start'])
        def go_to_start(message):
            if(message.chat.id not in admin_state ):
                users_state[message.chat.id] = start_menu
                curr_menu = start_menu
                curr_menu.send(message.chat.id)

        @bot.message_handler(content_types=["text"])
        def messages(message):
            global users_state
            try:
                curr_menu = users_state[message.chat.id]
            except KeyError:
                users_state[message.chat.id] = start_menu
                curr_menu = start_menu
                curr_menu.send(message.chat.id)
                return 0

            if(message.chat.id in admin_state):
                active_function_manager(message,curr_menu,admin_state)
                return 0

            try:
                command = int(message.text)
            except  Exception:
                send_default_command(message.chat.id)
                return 0

            if((command == -1 or message.chat.id in admin_state) and message.chat.id in admin_list):
                admin_manager(message,command,curr_menu)
            else:
                сommand_manager(message,command,curr_menu,users_state)


        bot.polling(none_stop=True)       
    except  Exception as e:
        print(e)
        a= (users_state,
        admin_state,
        admin_list,
        start_menu)
        with open('save.pickle', 'wb') as handle:
            pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
        bot.polling(none_stop=True)       