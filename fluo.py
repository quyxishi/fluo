from dataclasses import dataclass
from telebot import types
from vk_api import *
import threading
import datetime
import requests
import telebot
import logging
import time
import sys
import re
import io


# * ~ configuration

# TODO: guide

vk_app_token = '<vk standalone-application token>'
tg_bot_token = '<telegram bot token>'

# *


# TODO: rewrite on aiogram
# TODO: settings ; online menu pref
# TODO: func for mlocales ; rework mlocales

database = {}
locale = ''
islistenthreadrunning = False

rqtimestamp = 0
rqcount = 0

@dataclass
class mlocales:
    emoji_detective = '🕵🏻'
    # *
    en_localeset = '🇬🇧 *Language set*'
    ru_localeset = '🇷🇺 *Язык установлен*'
    # *
    en_profilelink = '🕵🏻 *Send me link to vk profile, like:*\n` * ``https://vk.com/id1`\n` * ``durov`'
    ru_profilelink = '🕵🏻 *Отправь мне ссылку на вк профиль, к примеру:*\n` * ``https://vk.com/id1`\n` * ``durov`'
    # *
    en_sendreq = '⌛ *Sending request...*'
    ru_sendreq = '⌛ *Отправляю запрос...*'
    en_parseresp = '⌛ *Parsing response...*'
    ru_parseresp = '⌛ *Обрабатываю ответ...*'
    # *
    en_usernotexists = '❌ *Seems that the user does not exist*'
    ru_usernotexists = '❌ *Похоже, что пользователь не существует*'
    # *
    en_online = 'online'
    ru_online = 'онлайн'
    en_offline = 'offline'
    ru_offline = 'оффлайн'
    en_onlinelastseen = en_online + ', last seen `%s` ago'
    ru_onlinelastseen = ru_online + ', последний раз был(а) `%s` назад'
    en_offlinelastseen = en_offline + ', last seen `%s` ago'
    ru_offlinelastseen = ru_offline + ', последний раз был(а) `%s` назад'
    # *
    en_closed = '👁‍🗨 *Closed*: '
    ru_closed = '👁‍🗨 *Закрыт*: '
    en_created = '👁‍🗨 *Created*: '
    ru_created = '👁‍🗨 *Создан*: '
    # *
    en_profilephoto = '📷 Photo'
    ru_profilephoto = '📷 Фото'
    # *
    en_onlinemenu = '🕵🏻 Online'
    ru_onlinemenu = '🕵🏻 Онлайн'
    # *
    en_imagereq = '⌛ *Requesting image...*'
    ru_imagereq = '⌛ *Запрашиваю изображение...*'
    # *
    en_listenalready = '❌ *Listening already running*'
    ru_listenalready = '❌ *Прослушивание уже запущено*'
    # *
    en_unabletime = '❌ *Unable to retrieve last seen timestamp*'
    ru_unabletime = '❌ *Невозможно получить время последнего посещения*'
    # *
    en_listenonline = '🕵🏻 Listen for online'
    ru_listenonline = '🕵🏻 Прослушивать онлайн'
    # *
    en_onlinemenuheader = '*Online menu*\n_Listen for user online with own configuration_'
    ru_onlinemenuheader = '*Онлайн меню*\n_Прослушивание онлайна пользователя с собственной конфигурацией_'
    # *
    en_onlinesleep = '⌛ *Online sleep time:* '
    ru_onlinesleep = '⌛ *Ожидание при онлайне:* '
    en_offlinesleep = '⌛ *Offline sleep time:* '
    ru_offlinesleep = '⌛ *Ожидание при оффлайне:* '
    # *
    en_cancellisten = '❌ Cancel listening'
    ru_cancellisten = '❌ Прервать прослушивание'
    # *
    en_postonlinemenuheader = '*Online listening started*\n_I will send changes in user online_'
    ru_postonlinemenuheader = '*Прослушивание онлайна началось*\n_Отправлю изменения онлайна пользователя_'
    # *
    en_onlinechange = '*Online status change:* '
    ru_onlinechange = '*Онлайн статус изменился:* '
    en_onlineupdate = '✒️ *Online updated manually:* _last seen_ '
    ru_onlineupdate = '✒️ *Онлайн обновился вручную:* _последний раз был(а)_ '
    # *
    en_onlinewentout = '🍂 *User went out from vk:* _last seen_ `%s` _ago_'
    ru_onlinewentout = '🍂 *Пользователь вышел из вк:* _последний раз был(а)_ `%s` _времени назад_'
    # *
    en_listeninterrupted = '❌ *Listening interrupted*'
    ru_listeninterrupted = '❌ *Прослушивание прервано*'
    en_listennotrunning = '❌ *Listening is not running*'
    ru_listennotrunning = '❌ *Прослушивание не выполняется*'
    # *
    en_refreshonline = '🔄 Refresh'
    ru_refreshonline = '🔄 Обновить'
    # *
    en_friendsmenu = '👤 Friends'
    ru_friendsmenu = '👤 Друзья'
    # *
    en_profileclosed = '❌ *Profile is closed*'
    ru_profileclosed = '❌ *Профиль закрыт*'
    # *
    en_analyzefriends = '🕵🏻 Analyze friends'
    ru_analyzefriends = '🕵🏻 Анализ друзей'
    # *
    en_friendsmenuheader = '*Friends menu*\n_Advanced information about the users friends_'
    ru_friendsmenuheader = '*Меню друзей*\n_Расширенная информация о друзьях пользователя_'
    # *
    en_analyzefriendsheader = '*Analyze friends*\n_The most common geodata among friends_'
    ru_analyzefriendsheader = '*Анализ друзей*\n_Самые распространненые геоданные среди друзей_'
    # *
    en_friendscount = '👤 *Friends count:* '
    ru_friendscount = '👤 *Количество друзей:* '
    en_country = '🌍 *Country:* '
    ru_country = '🌍 *Страна:* '
    en_city = '🏙️ *City:* '
    ru_city = '🌃 *Город:* '
    en_university = '🎓 *University:* '
    ru_university = '🎓 *Университет:* '
    en_analysistime = '⌛ *Analysis time:* '
    ru_analysistime = '⌛ *Время анализа:* '


def initlogging() -> logging.Logger:
    logformat = '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: %(message)s'

    logging.basicConfig(level=logging.INFO, format=logformat)
    LOG = logging.getLogger('fluo')

    return LOG


def initvkapi(access_token: str) -> vk_api.VkApiMethod:
    session = vk_api.VkApi(token=access_token)
    session._auth_token()

    return session.get_api()


def inituser(userid: int) -> None:
    global database

    database.update({userid: {'langaskmessageid': 0, 'locale': '', 'onlinemenumessageid': 0, 'listenonlinestatus': False, 'listeningid': 0, 'onlinesleep': 2.0, 'offlinesleep': 10.0}})


def listenonline(targetid: str) -> dict:
    global vk
    global rqtimestamp
    global rqcount

    # *

    deltatimestamp = time.time() - rqtimestamp

    if deltatimestamp < 1.0 and rqcount == 3:
        time.sleep(1.0 - deltatimestamp)
        rqcount = 0

    rqtimestamp = time.time()
    rqcount += 1

    # *

    targetinfo = vk.users.get(user_ids=targetid, fields='online, last_seen')[0]

    targetlastseen = targetinfo['last_seen']['time']
    tmtargetlastseen = time.localtime(targetlastseen)
    targetlastseentime = time.strftime('%H:%M:%S %d/%m/%Y', tmtargetlastseen)

    current = int(time.time())
    currenttime = time.strftime('%H:%M:%S %d/%m/%Y', time.localtime(current))

    delta = datetime.timedelta(seconds=current - targetlastseen)

    # TODO: errors check ; user can close online during listening or delete account

    status = {'first_name': targetinfo['first_name'],
            'last_name': targetinfo['last_name'],
            'online': targetinfo['online'],
            'delta': delta,
            'currenttime': currenttime,
            'lastseentime': targetlastseentime,
            'lastseensecond': tmtargetlastseen.tm_sec}

    return status


def listenthread(bot: telebot.TeleBot) -> None:
    global islistenthreadrunning

    LOG.info('open listenthread')

    paramsdatabase = {}

    while "'listenonlinestatus': True" in str(database): # TODO
        prevdatabase = {}
        prevdatabase.update(database)

        for user in prevdatabase:
            if not prevdatabase[user]['listenonlinestatus']:
                continue
            
            if user not in paramsdatabase:
                paramsdatabase.update({user: {'previousonline': -1, 'plastseensecond': -1, 'plastseentime': '', 'wentout': -1, 'timeout': 0}})
            elif time.time() < paramsdatabase[user]['timeout']:
                continue

            # *

            onlineinfo = listenonline(prevdatabase[user]['listeningid'])

            onlinestatus = onlineinfo['online']
            currenttime = onlineinfo['currenttime']
            lastseensecond = onlineinfo['lastseensecond']
            lastseentime = onlineinfo['lastseentime']
            delta = onlineinfo['delta']

            previousonline = paramsdatabase[user]['previousonline']
            plastseensecond = paramsdatabase[user]['plastseensecond']
            wentout = paramsdatabase[user]['wentout']

            if previousonline != -1 and previousonline != onlinestatus:
                emojistatus = '🟢' if onlinestatus else '🔴'
                paramsdatabase[user]['wentout'] = False if onlinestatus else True
                bot.send_message(user, f'{emojistatus} {mlocales.en_onlinechange if locale == "en" else mlocales.ru_onlinechange}`{previousonline} -> {onlinestatus}`\n\n` ~ ``{currenttime}`')

            if plastseensecond != -1 and abs(lastseensecond - plastseensecond) not in [0, 1] and previousonline == onlinestatus:
                # NOTE: it is more likely that user sent message
                paramsdatabase[user]['wentout'] = False
                bot.send_message(user, f"{mlocales.en_onlineupdate if locale == 'en' else mlocales.ru_onlineupdate}`'{paramsdatabase[user]['plastseentime']}' -> '{lastseentime}'`\n\n` ~ ``{currenttime}`")

            if wentout != -1 and delta.seconds >= 62 and not wentout:
                paramsdatabase[user]['wentout'] = True
                bot.send_message(user, f'{mlocales.en_onlinewentout % delta if locale == "en" else mlocales.ru_onlinewentout % delta}\n\n` ~ ``{currenttime}`')
                
            paramsdatabase[user]['previousonline'] = onlinestatus
            paramsdatabase[user]['plastseensecond'] = lastseensecond
            paramsdatabase[user]['plastseentime'] = lastseentime

            paramsdatabase[user]['timeout'] = time.time() + (prevdatabase[user]['onlinesleep'] if onlinestatus else prevdatabase[user]['offlinesleep'])
    
    LOG.info('close listenthread')

    islistenthreadrunning = False


def commonfromlist(x: list) -> any:
    return max(set(x), key=x.count) if x else 'None'


def inithooks(bot: telebot.TeleBot) -> None:
    @bot.message_handler(func=lambda message: message.chat.id in database and database[message.chat.id]['locale'] != '' and len(re.findall('(vk\.com/|^)([a-zA-Z0-9\._]{3,32}$)', message.text)) != 0)
    def link(message) -> None:
        global vk

        chatid = message.chat.id
        locale = database[chatid]['locale']

        statusmessage = bot.send_message(chatid, mlocales.en_sendreq if locale == 'en' else mlocales.ru_sendreq)

        profilename = re.findall('(vk\.com/|^)([a-zA-Z0-9\._]{3,32}$)', message.text)[0][1]
        profileinfo = vk.users.get(user_ids=profilename, fields='status, online, last_seen')

        if len(profileinfo) == 0:
            bot.edit_message_text(mlocales.en_usernotexists if locale == 'en' else mlocales.ru_usernotexists, chatid, statusmessage.id)
            return

        profileinfo = profileinfo[0]

        bot.edit_message_text(mlocales.en_parseresp if locale == 'en' else mlocales.ru_parseresp, chatid, statusmessage.id)

        foafrequest = requests.get(f'https://vk.com/foaf.php?id={profileinfo["id"]}')
        registrationdate = str(re.findall(b'<ya:created dc:date="[0-9A-Z:+-]{25}"\/>', foafrequest.content)[0], 'utf-8').split('"')[1]

        inlinemarkup = types.InlineKeyboardMarkup()
        profilebutton = types.InlineKeyboardButton(mlocales.en_profilephoto if locale == 'en' else mlocales.ru_profilephoto, callback_data=f'photo;{profileinfo["id"]}')
        vkonlinebutton = types.InlineKeyboardButton(mlocales.en_onlinemenu if locale == 'en' else mlocales.ru_onlinemenu, callback_data=f'onlinemenu;{profileinfo["id"] if "last_seen" in profileinfo else "-1"}')
        friendsbutton = types.InlineKeyboardButton(mlocales.en_friendsmenu if locale == 'en' else mlocales.ru_friendsmenu, callback_data=f'friendsmenu;{profileinfo["id"] if not profileinfo["is_closed"] else "-1"}')
        refreshbutton = types.InlineKeyboardButton(mlocales.en_refreshonline if locale == 'en' else mlocales.ru_refreshonline, callback_data=f'refresh;{profileinfo["id"]}')
        inlinemarkup.add(profilebutton, vkonlinebutton, friendsbutton, refreshbutton)

        if 'last_seen' in profileinfo:
            delta = datetime.timedelta(seconds=int(time.time()) - profileinfo['last_seen']['time'])
            lastseentime = str(mlocales.en_onlinelastseen % delta if locale == 'en' else mlocales.ru_onlinelastseen % delta) if profileinfo['online'] else str(mlocales.en_offlinelastseen % delta if locale == 'en' else mlocales.ru_offlinelastseen % delta)
        else:
            lastseentime = str(mlocales.en_online if locale == 'en' else mlocales.ru_online) if profileinfo['online'] else str(mlocales.en_offline if locale == 'en' else mlocales.ru_offline)

        bot.edit_message_text(f'*{profileinfo["first_name"]} {profileinfo["last_name"]}*\n_{profileinfo["status"]}_\n{lastseentime}\n\n👁‍🗨 *ID:* `{profileinfo["id"]}`\n{mlocales.en_closed if locale == "en" else mlocales.ru_closed}`{profileinfo["is_closed"]}`\n{mlocales.en_created if locale == "en" else mlocales.ru_created}`{registrationdate}`', chatid, statusmessage.id, reply_markup=inlinemarkup)

    @bot.message_handler(func=lambda message: message.chat.id in database and database[message.chat.id]['locale'] != '' and message.content_type == 'text' and message.text.startswith('/settings'))
    def settings(message) -> None:
        return # TODO

    @bot.message_handler(func=lambda message: message.chat.id not in database)
    def prewelcome(message) -> None:
        global database

        chatid = message.chat.id

        inituser(chatid)

        inlinemarkup = types.InlineKeyboardMarkup()
        rubutton = types.InlineKeyboardButton('🇷🇺 Russian', callback_data=f'setlang;ru')
        enbutton = types.InlineKeyboardButton('🇬🇧 English', callback_data=f'setlang;en')
        inlinemarkup.add(rubutton, enbutton)

        askmessage = bot.send_message(chatid, '🌍 *Choose language*', reply_markup=inlinemarkup)

        database[chatid]['langaskmessageid'] = askmessage.id

    @bot.message_handler(func=lambda message: message.chat.id in database and database[message.chat.id]['locale'] != '')
    def welcome(message) -> None:
        chatid = message.chat.id
        bot.send_message(chatid, mlocales.en_profilelink if database[chatid]['locale'] == 'en' else mlocales.ru_profilelink)


def initcallbacks(bot: telebot.TeleBot) -> None:
    @bot.callback_query_handler(func=lambda call: call.message.chat.id in database and call.data.startswith('refresh;'))
    def refreshcall(call) -> None:
        global vk

        chatid = call.message.chat.id
        locale = database[chatid]['locale']

        targetid = call.data.split(';')[1]
        profileinfo = vk.users.get(user_ids=targetid, fields='status, online, last_seen')

        if len(profileinfo) == 0:
            bot.send_message(chatid, mlocales.en_usernotexists if locale == 'en' else mlocales.ru_usernotexists)
            return

        profileinfo = profileinfo[0]

        if 'last_seen' not in profileinfo:
            bot.send_message(chatid, mlocales.en_unabletime if locale == 'en' else mlocales.ru_unabletime)
            return

        delta = datetime.timedelta(seconds=int(time.time()) - profileinfo['last_seen']['time'])
        lastseentime = str(mlocales.en_onlinelastseen % delta if locale == 'en' else mlocales.ru_onlinelastseen % delta) if profileinfo['online'] else str(mlocales.en_offlinelastseen % delta if locale == 'en' else mlocales.ru_offlinelastseen % delta)

        bot.send_message(chatid, f'{mlocales.emoji_detective} *{profileinfo["first_name"]} {profileinfo["last_name"]}*` :: `{lastseentime}')

    @bot.callback_query_handler(func=lambda call: call.message.chat.id in database and call.data.startswith('setlang;'))
    def setlangcall(call) -> None:
        global vk
        global database

        chatid = call.message.chat.id
        targetlocale = call.data.split(';')[1]

        database[chatid]['locale'] = targetlocale

        bot.edit_message_text(mlocales.en_localeset if targetlocale == 'en' else mlocales.ru_localeset, chatid, database[chatid]['langaskmessageid'])
        bot.send_message(chatid, mlocales.en_profilelink if targetlocale == 'en' else mlocales.ru_profilelink)

    @bot.callback_query_handler(func=lambda call: call.message.chat.id in database and call.data.startswith('photo;'))
    def photocall(call) -> None:
        global vk

        chatid = call.message.chat.id
        locale = database[chatid]['locale']

        requestmessage = bot.send_message(chatid, mlocales.en_imagereq if locale == 'en' else mlocales.ru_imagereq)

        targetid = call.data.split(';')[1]
        targetinfo = vk.users.get(user_ids=targetid, fields='photo_max_orig, domain')

        if len(targetinfo) == 0:
            bot.edit_message_text(mlocales.en_usernotexists if locale == 'en' else mlocales.ru_usernotexists, chatid, requestmessage.id)
            return

        targetinfo = targetinfo[0]
        targetphotourl = targetinfo['photo_max_orig']

        photosize = re.findall('size=(.*)&q', targetphotourl)
        photosize = photosize[0] if len(photosize) > 0 else '~x~'

        caption = photosize + f'` :: `vk.com/{targetinfo["domain"]}'

        request = requests.get(targetphotourl, timeout=4)
        photoio = io.BytesIO(request.content)

        bot.send_photo(chatid, photoio, caption=caption)

        photoio.close()

    @bot.callback_query_handler(func=lambda call: call.message.chat.id in database and call.data.startswith('onlinemenu;'))
    def onlinemenucall(call) -> None:
        global database

        chatid = call.message.chat.id
        locale = database[chatid]['locale']

        if database[chatid]['listenonlinestatus']:
            bot.send_message(chatid, mlocales.en_listenalready if locale == 'en' else mlocales.ru_listenalready)
            return

        targetid = call.data.split(';')[1]

        if targetid == '-1':
            bot.send_message(chatid, mlocales.en_unabletime if locale == 'en' else mlocales.ru_unabletime)
            return

        markupinline = types.InlineKeyboardMarkup()
        listenbutton = types.InlineKeyboardButton(mlocales.en_listenonline if locale == 'en' else mlocales.ru_listenonline, callback_data=f'startlistenonline;{targetid}')
        markupinline.add(listenbutton)

        message = bot.send_message(chatid, f'{mlocales.en_onlinemenuheader if locale == "en" else mlocales.ru_onlinemenuheader}\n\n👁‍🗨 *ID:* `{targetid}`\n{mlocales.en_onlinesleep if locale == "en" else mlocales.ru_onlinesleep}`{database[chatid]["onlinesleep"]}s`\n{mlocales.en_offlinesleep if locale == "en" else mlocales.ru_offlinesleep}`{database[chatid]["offlinesleep"]}s`', reply_markup=markupinline)

        database[chatid]['onlinemenumessageid'] = message.id

    @bot.callback_query_handler(func=lambda call: call.message.chat.id in database and call.data.startswith('friendsmenu;'))
    def friendsmenucall(call) -> None:
        chatid = call.message.chat.id
        locale = database[chatid]['locale']

        targetid = call.data.split(';')[1]

        if targetid == '-1':
            bot.send_message(chatid, mlocales.en_profileclosed if locale == 'en' else mlocales.ru_profileclosed)
            return
        
        markupinline = types.InlineKeyboardMarkup()
        analyzebutton = types.InlineKeyboardButton(mlocales.en_analyzefriends if locale == 'en' else mlocales.ru_analyzefriends, callback_data=f'analyzefriends;{targetid}')
        markupinline.add(analyzebutton)

        bot.send_message(chatid, f'{mlocales.en_friendsmenuheader if locale == "en" else mlocales.ru_friendsmenuheader}\n\n👁‍🗨 *ID:* `{targetid}`', reply_markup=markupinline)

    @bot.callback_query_handler(func=lambda call: call.message.chat.id in database and call.data.startswith('startlistenonline;'))
    def listenonlinecall(call) -> None:
        global LOG
        global database
        global islistenthreadrunning

        chatid = call.message.chat.id
        locale = database[chatid]['locale']
        
        targetid = call.data.split(';')[1]

        database[chatid]['listeningid'] = targetid
        database[chatid]['listenonlinestatus'] = True

        markupinline = types.InlineKeyboardMarkup()
        cancelbutton = types.InlineKeyboardButton(mlocales.en_cancellisten if locale == 'en' else mlocales.ru_cancellisten, callback_data=f'interruptlistenonline;')
        markupinline.add(cancelbutton)

        bot.edit_message_text(f'{mlocales.en_postonlinemenuheader if locale == "en" else mlocales.ru_postonlinemenuheader}\n\n👁‍🗨 *ID:* `{targetid}`\n{mlocales.en_onlinesleep if locale == "en" else mlocales.ru_onlinesleep}`{database[chatid]["onlinesleep"]}s`\n{mlocales.en_offlinesleep if locale == "en" else mlocales.ru_offlinesleep}`{database[chatid]["offlinesleep"]}s`', chatid, database[chatid]['onlinemenumessageid'], reply_markup=markupinline)

        LOG.info(f'start listening: id{targetid}')

        if not islistenthreadrunning:
            islistenthreadrunning = True
            lthread = threading.Thread(target=listenthread, args=(bot,))
            lthread.start()

    @bot.callback_query_handler(func=lambda call: call.message.chat.id in database and call.data.startswith('analyzefriends;'))
    def analyzefriendscall(call) -> None:
        global vk
        global LOG

        chatid = call.message.chat.id
        locale = database[chatid]['locale']
        
        targetid = call.data.split(';')[1]

        statusmessage = bot.send_message(chatid, mlocales.en_sendreq if locale == 'en' else mlocales.ru_sendreq)
        targetfriends = vk.friends.get(user_id=targetid, fields='city, country, universities')

        # TODO: errors check

        bot.edit_message_text(mlocales.en_parseresp if locale == 'en' else mlocales.ru_parseresp, chatid, statusmessage.id)

        tstart = time.time()
        countries, cities, universities = [], [], []

        for friend in targetfriends['items']:
            if 'country' in friend and re.search('[a-zA-Zа-яА-Я]', friend['country']['title']):
                countries.append(friend['country']['title'])

            if 'city' in friend and re.search('[a-zA-Zа-яА-Я]', friend['city']['title']):
                cities.append(friend['city']['title'])

            if 'universities' in friend and len(friend['universities']) > 0 and re.search('[a-zA-Zа-яА-Я]', friend['universities'][0]['name']):
                universities.append(friend['universities'][0]['name'])

        country, city, university = commonfromlist(countries), commonfromlist(cities), commonfromlist(universities)
        tend = time.time()

        bot.edit_message_text(f'{mlocales.en_analyzefriendsheader if locale == "en" else mlocales.ru_analyzefriendsheader}\n\n👁‍🗨 *ID:* `{targetid}`\n{mlocales.en_friendscount if locale == "en" else mlocales.ru_friendscount}`{targetfriends["count"]}`\n{mlocales.en_country if locale == "en" else mlocales.ru_country}`{country}`\n{mlocales.en_city if locale == "en" else mlocales.ru_city}`{city}`\n{mlocales.en_university if locale == "en" else mlocales.ru_university}`{university}`\n{mlocales.en_analysistime if locale == "en" else mlocales.ru_analysistime}`{round((tend - tstart) * 1000)}ms`', chatid, statusmessage.id)

    @bot.callback_query_handler(func=lambda call: call.message.chat.id in database and call.data.startswith('interruptlistenonline;'))
    def interruptlisten(call) -> None:
        global database

        # NOTE: workerthreads limit is set to 2.

        chatid = call.message.chat.id
        locale = database[chatid]['locale']

        bot.send_message(chatid, str(mlocales.en_listeninterrupted if locale == 'en' else mlocales.ru_listeninterrupted) if database[chatid]['listenonlinestatus'] else str(mlocales.en_listennotrunning if locale == 'en' else mlocales.ru_listennotrunning))
        database[chatid]['listenonlinestatus'] = False

        LOG.info(f'interrupt listening: {database[chatid]["listeningid"]}')


def main() -> int:
    global LOG
    global vk

    LOG = initlogging()

    LOG.info('init vk-api')

    vk = initvkapi(vk_app_token)

    LOG.info('init telebot')

    bot = telebot.TeleBot(tg_bot_token, parse_mode='markdown')

    LOG.info('init callbacks')

    initcallbacks(bot)

    LOG.info('init hooks')

    inithooks(bot)

    bot.infinity_polling()


if __name__ == '__main__':
    try:
        status = main()
    except KeyboardInterrupt:
        status = 0
    except Exception as e:
        status = 1

        for i in range(1, 6):
            print(f' * ~ {e.__name__}, restarting {i}/5 ...')
            time.sleep(10)

            try:
                status = main()
                break
            except Exception:
                pass
    finally:
        sys.exit(status)
