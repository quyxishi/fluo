from vkbottle import VKAPIError
from dataclasses import dataclass
from loguru import logger
import aiogram as aiog
import aiohttp as aioh
import threading
import datetime
import vkbottle
import asyncio
import time
import sys
import re
import io


# ~


# *

vk_app_token: str = '<vk standalone-application token>'
tg_bot_token: str = '<telegram bot token>'

# *

vk: vkbottle.API
er: vkbottle.ErrorHandler
bot: aiog.Bot
dp: aiog.Dispatcher

database: dict = {}
locale: str = ''
islistenthreadrunning: bool = False

@dataclass
class mlocales:
    emoji_detective: str = '🕵🏻'
    emoji_man: str = '👨'
    emoji_woman: str = '👩'
    emoji_person: str = '👤'
    # *
    emoji_platform_1: str = '📱'
    emoji_platform_2: str = '📱 (iPhone)'
    emoji_platform_3: str = '📱 (iPad)'
    emoji_platform_4: str = '📱 (Android)'
    emoji_platform_5: str = '📱 (Windows Phone)'
    emoji_platform_6: str = '💻 (Windows 8)'
    emoji_platform_7: str = '💻'
    # *
    en_localeset: str = '🇬🇧 *Language set*'
    ru_localeset: str = '🇷🇺 *Язык установлен*'
    # *
    en_profilelink: str = '🕵🏻 *Send me link to vk profile, like:*\n` * ``https://vk.com/id1`\n` * ``durov`'
    ru_profilelink: str = '🕵🏻 *Отправь мне ссылку на вк профиль, к примеру:*\n` * ``https://vk.com/id1`\n` * ``durov`'
    # *
    en_sendreq: str = '⌛ *Sending request\.\.\.*'
    ru_sendreq: str = '⌛ *Отправляю запрос\.\.\.*'
    en_parseresp: str = '⌛ *Parsing response\.\.\.*'
    ru_parseresp: str = '⌛ *Обрабатываю ответ\.\.\.*'
    # *
    en_usernotexists: str = '❌ *Seems that the user does not exist*'
    ru_usernotexists: str = '❌ *Похоже, что пользователь не существует*'
    # *
    en_online: str = 'online'
    ru_online: str = 'онлайн'
    en_offline: str = 'offline'
    ru_offline: str = 'оффлайн'
    en_onlinelastseen: str = en_online + ', last seen `%s` ago'
    ru_onlinelastseen: str = ru_online + ', последний раз был(а) `%s` назад'
    en_offlinelastseen: str = en_offline + ', last seen `%s` ago'
    ru_offlinelastseen: str = ru_offline + ', последний раз был(а) `%s` назад'
    # *
    en_closed: str = '👁‍🗨 *Closed*: '
    ru_closed: str = '👁‍🗨 *Закрыт*: '
    en_created: str = '👁‍🗨 *Created*: '
    ru_created: str = '👁‍🗨 *Создан*: '
    # *
    en_profilephoto: str = '📷 Photo'
    ru_profilephoto: str = '📷 Фото'
    # *
    en_onlinemenu: str = '🕵🏻 Online'
    ru_onlinemenu: str = '🕵🏻 Онлайн'
    # *
    en_imagereq: str = '⌛ *Requesting image\.\.\.*'
    ru_imagereq: str = '⌛ *Запрашиваю изображение\.\.\.*'
    # *
    en_listenalready: str = '❌ *Listening already running*'
    ru_listenalready: str = '❌ *Отслеживание уже запущено*'
    # *
    en_unabletime: str = '❌ *Unable to retrieve last seen timestamp*'
    ru_unabletime: str = '❌ *Невозможно получить время последнего посещения*'
    # *
    en_listenonline: str = '🕵🏻 Listen for online'
    ru_listenonline: str = '🕵🏻 Отслеживать онлайн'
    # *
    en_onlinemenuheader: str = '*Online menu*\n_Listen for user online with own configuration_'
    ru_onlinemenuheader: str = '*Онлайн меню*\n_Отслеживание онлайна пользователя с собственной конфигурацией_'
    # *
    en_onlinesleep: str = '⌛ *Online sleep time:* '
    ru_onlinesleep: str = '⌛ *Ожидание при онлайне:* '
    en_offlinesleep: str = '⌛ *Offline sleep time:* '
    ru_offlinesleep: str = '⌛ *Ожидание при оффлайне:* '
    # *
    en_cancellisten: str = '❌ Cancel listening'
    ru_cancellisten: str = '❌ Прервать отслеживание'
    # *
    en_postonlinemenuheader: str = '*Online listening started*\n_I will send changes in user online_'
    ru_postonlinemenuheader: str = '*Отслеживание онлайна началось*\n_Отправлю изменения онлайна пользователя_'
    # *
    en_onlinechange: str = '*Online status change:* '
    ru_onlinechange: str = '*Онлайн статус изменился:* '
    en_onlineupdate: str = '✒️ *Online updated manually:* _last seen_ '
    ru_onlineupdate: str = '✒️ *Онлайн обновился вручную:* _последний раз был\(а\)_ '
    # *
    en_onlinewentout: str = '🍂 *User went out from vk:* _last seen_ `%s` _ago_'
    ru_onlinewentout: str = '🍂 *Пользователь вышел из вк:* _последний раз был\(а\)_ `%s` _назад_'
    # *
    en_listeninterrupted: str = '❌ *Listening interrupted*'
    ru_listeninterrupted: str = '❌ *Отслеживание прервано*'
    en_listennotrunning: str = '❌ *Listening is not running*'
    ru_listennotrunning: str = '❌ *Отслеживание не выполняется*'
    # *
    en_refreshonline: str = '🔄 Refresh'
    ru_refreshonline: str = '🔄 Обновить'
    # *
    en_friendsmenu: str = '👤 Friends'
    ru_friendsmenu: str = '👤 Друзья'
    # *
    en_profileclosed: str = '❌ *Profile is closed*'
    ru_profileclosed: str = '❌ *Профиль закрыт*'
    # *
    en_analyzefriends: str = '🕵🏻 Analyze friends'
    ru_analyzefriends: str = '🕵🏻 Анализ друзей'
    # *
    en_friendsmenuheader: str = '*Friends menu*\n_Advanced information about the users friends_'
    ru_friendsmenuheader: str = '*Меню друзей*\n_Расширенная информация о друзьях пользователя_'
    # *
    en_analyzefriendsheader: str = '*Analyze friends*\n_The most common geodata among friends_'
    ru_analyzefriendsheader: str = '*Анализ друзей*\n_Самые распространенные геоданные среди друзей_'
    # *
    en_friendscount: str = '👤 *Friends count:* '
    ru_friendscount: str = '👤 *Количество друзей:* '
    en_country: str = '🌍 *Country:* '
    ru_country: str = '🌍 *Страна:* '
    en_city: str = '🏙️ *City:* '
    ru_city: str = '🏙️ *Город:* '
    en_university: str = '🎓 *University:* '
    ru_university: str = '🎓 *Университет:* '
    en_analysistime: str = '⌛ *Analysis time:* '
    ru_analysistime: str = '⌛ *Время анализа:* '
    # *
    en_searchhidden: str = '🕵🏻 Search for hidden'
    ru_searchhidden: str = '🕵🏻 Поиск скрытых'
    # *
    en_ffreq: str = '⌛ *Getting friends of the users friends\.\.\.*'
    ru_ffreq: str = '⌛ *Получаю друзей друзей пользователя\.\.\.*'
    # *
    en_ffresp: str = '⌛ *Анализирую\.\.\.*'
    ru_ffresp: str = '⌛ *Анализирую\.\.\.*'
    # *
    en_hiddenfriendsheader: str = '*Analyze friends*\n_Hidden user friends_'
    ru_hiddenfriendsheader: str = '*Анализ друзей*\n_Скрытые друзья пользователя_'
    # *
    en_restrictedprofile: str = '❌ *Profile deleted or blocked*'
    ru_restrictedprofile: str = '❌ *Профиль удален либо же заблокирован*'
    # *
    en_unknownerror: str = '❌ *Unknown error: VKAPIError code %s*'
    ru_unknownerror: str = '❌ *Неизвестная ошибка: VKAPIError код %s*'

# ~


def ml(name: str, locale: str) -> str:
    return getattr(mlocales, locale + '_' + name)


def initlogging() -> None: 
    logger.remove(0)
    logger.add(sys.stdout, format='{time:YYYY/MM/DD ~ HH:mm:ss,SSS} ({file}) {level} :: {message}', level='INFO')


def inituser(userid: int) -> None:
    global database

    database.update({userid: {'locale': '', 'listenonlinestatus': False, 'listeningid': 0, 'onlinesleep': 2.0, 'offlinesleep': 10.0}})


async def listenonline(targetid: str) -> dict:
    global vk

    targetinfo: any = await vk.users.get(user_ids=targetid, fields='online, last_seen')
    targetinfo = targetinfo[0]

    targetlastseen: int = targetinfo.last_seen.time
    tmtargetlastseen: time.struct_time = time.localtime(targetlastseen)
    targetlastseentime: str = time.strftime('%H:%M:%S %d/%m/%Y', tmtargetlastseen)

    current = int(time.time())
    currenttime: str = time.strftime('%H:%M:%S %d/%m/%Y', time.localtime(current))

    delta = datetime.timedelta(seconds=current - targetlastseen)

    # TODO: errors check ; user can close online during listening or delete account

    status: dict = {'first_name': targetinfo.first_name,
            'last_name': targetinfo.last_name,
            'online': targetinfo.online,
            'delta': delta,
            'currenttime': currenttime,
            'lastseentime': targetlastseentime,
            'lastseensecond': tmtargetlastseen.tm_sec}

    return status


def listenthread(bot: aiog.Bot, loop: asyncio.AbstractEventLoop) -> None:
    global islistenthreadrunning

    logger.info('open listenthread')

    paramsdatabase: dict = {}

    while "'listenonlinestatus': True" in str(database): # TODO
        prevdatabase: dict = {}
        prevdatabase.update(database)

        for user in prevdatabase:
            if not prevdatabase[user]['listenonlinestatus']:
                continue
            
            if user not in paramsdatabase:
                paramsdatabase.update({user: {'previousonline': -1, 'plastseensecond': -1, 'plastseentime': '', 'wentout': -1, 'timeout': 0}})
            elif time.time() < paramsdatabase[user]['timeout']:
                continue

            # *

            locale: str = prevdatabase[user]['locale']

            onlineinfo: dict = asyncio.run_coroutine_threadsafe(listenonline(prevdatabase[user]['listeningid']), loop).result()

            onlinestatus: int = onlineinfo['online']
            currenttime: str = onlineinfo['currenttime']
            lastseensecond: int = onlineinfo['lastseensecond']
            lastseentime: str = onlineinfo['lastseentime']
            delta: datetime.timedelta = onlineinfo['delta']

            previousonline: int = paramsdatabase[user]['previousonline']
            plastseensecond: int = paramsdatabase[user]['plastseensecond']
            wentout: any = paramsdatabase[user]['wentout']

            if previousonline != -1 and previousonline != onlinestatus:
                emojistatus: str = '🟢' if onlinestatus else '🔴'
                paramsdatabase[user]['wentout'] = False if onlinestatus else True
                asyncio.run_coroutine_threadsafe(bot.send_message(user, f'{emojistatus} {ml("onlinechange", locale)}`{previousonline} -> {onlinestatus}`\n\n` ~ ``{currenttime}`'), loop).result()

            if plastseensecond != -1 and abs(lastseensecond - plastseensecond) not in [0, 1] and previousonline == onlinestatus:
                # NOTE: it is more likely that user sent message
                paramsdatabase[user]['wentout'] = False
                asyncio.run_coroutine_threadsafe(bot.send_message(user, f"{ml('onlineupdate', locale)}`'{paramsdatabase[user]['plastseentime']}' -> '{lastseentime}'`\n\n` ~ ``{currenttime}`"), loop).result()

            if wentout != -1 and delta.seconds >= 62 and not wentout:
                paramsdatabase[user]['wentout'] = True
                asyncio.run_coroutine_threadsafe(bot.send_message(user, f'{ml("onlinewentout", locale) % delta}\n\n` ~ ``{currenttime}`'), loop).result()
                
            paramsdatabase[user]['previousonline'] = onlinestatus
            paramsdatabase[user]['plastseensecond'] = lastseensecond
            paramsdatabase[user]['plastseentime'] = lastseentime

            paramsdatabase[user]['timeout'] = time.time() + (prevdatabase[user]['onlinesleep'] if onlinestatus else prevdatabase[user]['offlinesleep'])
    
    logger.info('close listenthread')

    islistenthreadrunning = False


def commonfromlist(x: list) -> any:
    return max(set(x), key=x.count) if x else 'None'


def inithooks() -> None:
    @er.register_error_handler(VKAPIError[30])
    async def vkclosederror(e: VKAPIError, *args: list) -> None:
        obj: any = args[0].message if args[0].__class__ is aiog.types.CallbackQuery else args[0]
        
        await obj.answer(ml('profileclosed', database[obj.chat.id]['locale']))
    
    @er.register_error_handler(VKAPIError[18])
    async def vkrestrictederror(e: VKAPIError, *args: list) -> None:
        obj: any = args[0].message if args[0].__class__ is aiog.types.CallbackQuery else args[0]

        await obj.answer(ml('restrictedprofile', database[obj.chat.id]['locale']))
    
    @er.register_error_handler(VKAPIError)
    async def vkunknownerror(e: VKAPIError, *args: list) -> None:
        obj: any = args[0].message if args[0].__class__ is aiog.types.CallbackQuery else args[0]

        await obj.answer(ml('unknownerror', database[obj.chat.id]['locale']) % e.code)

    # *

    @dp.message_handler(lambda message: message.chat.id in database and database[message.chat.id]['locale'] != '' and len(re.findall('(vk\.com/|^)([a-zA-Z0-9\._]{3,32}$)', message.text)) != 0)
    @er.catch
    async def link(message: aiog.types.Message) -> None:
        chatid: int = message.chat.id
        locale: str = database[chatid]['locale']

        statusmessage: aiog.types.Message = await message.answer(ml('sendreq', locale))

        profilename: str = re.findall('(vk\.com/|^)([a-zA-Z0-9\._]{3,32}$)', message.text)[0][1]
        profileinfo: list = await vk.users.get(user_ids=profilename, fields='status, online, last_seen')

        if not len(profileinfo):
            await statusmessage.edit_text(ml('usernotexists', locale))
            return

        profileinfo = profileinfo[0]

        await statusmessage.edit_text(ml('parseresp', locale))

        async with aioh.ClientSession() as session:
            async with session.get(f'https://vk.com/foaf.php?id={profileinfo.id}') as foafrequest:
                registrationdate: str = re.findall('<ya:created dc:date="([0-9A-Z:+-]{25})"/>', await foafrequest.text())[0]

        inlinemarkup = aiog.types.InlineKeyboardMarkup()
        profilebutton = aiog.types.InlineKeyboardButton(ml('profilephoto', locale), callback_data=f'photo;{profileinfo.id}')
        vkonlinebutton = aiog.types.InlineKeyboardButton(ml('onlinemenu', locale), callback_data=f'onlinemenu;{profileinfo.id if profileinfo.last_seen is not None else "-1"}') # TODO: check inside call
        friendsbutton = aiog.types.InlineKeyboardButton(ml('friendsmenu', locale), callback_data=f'friendsmenu;{profileinfo.id}')
        refreshbutton = aiog.types.InlineKeyboardButton(ml('refreshonline', locale), callback_data=f'refresh;{profileinfo.id}')
        inlinemarkup.add(profilebutton, vkonlinebutton, friendsbutton, refreshbutton)

        if profileinfo.last_seen is not None:
            delta = datetime.timedelta(seconds=int(time.time()) - profileinfo.last_seen.time)
            lastseentime: str = ml('onlinelastseen', locale) % delta if profileinfo.online else ml('offlinelastseen', locale) % delta
        else:
            lastseentime: str = ml('online', locale) if profileinfo.online else ml('offline', locale)

        await statusmessage.edit_text(f'*{profileinfo.first_name} {profileinfo.last_name}*\n_{profileinfo.status}_\n{lastseentime} {ml(f"platform_{profileinfo.last_seen.platform}", "emoji") if profileinfo.last_seen is not None else ""}\n\n👁‍🗨 *ID:* `{profileinfo.id}`\n{ml("closed", locale)}`{profileinfo.is_closed}`\n{ml("created", locale)}`{registrationdate}`', reply_markup=inlinemarkup, parse_mode='markdown')

    
    @dp.message_handler(lambda message: message.chat.id not in database)
    async def prewelcome(message: aiog.types.Message) -> None:
        inituser(message.chat.id)

        inlinemarkup = aiog.types.InlineKeyboardMarkup()
        rubutton = aiog.types.InlineKeyboardButton('🇷🇺 Russian', callback_data=f'setlang;ru')
        enbutton = aiog.types.InlineKeyboardButton('🇬🇧 English', callback_data=f'setlang;en')
        inlinemarkup.add(rubutton, enbutton)

        await message.answer('🌍 *Choose language*', reply_markup=inlinemarkup)

    @dp.message_handler(lambda message: message.chat.id in database and database[message.chat.id]['locale'] != '')
    async def welcome(message: aiog.types.Message) -> None:
        await message.answer(ml('profilelink', database[message.chat.id]['locale']))  


def initcallbacks() -> None:
    @dp.callback_query_handler(lambda callback_query: callback_query.message.chat.id in database and callback_query.data.startswith('setlang;'))
    async def setlangcall(callback_query: aiog.types.CallbackQuery) -> None:
        global database

        chatid: int = callback_query.message.chat.id
        targetlocale: str = callback_query.data.split(';')[1]

        database[chatid]['locale'] = targetlocale

        await callback_query.message.edit_text(ml('localeset', targetlocale))
        await callback_query.message.answer(ml('profilelink', targetlocale))

    @dp.callback_query_handler(lambda callback_query: callback_query.message.chat.id in database and callback_query.data.startswith('photo;'))
    @er.catch
    async def photocall(callback_query: aiog.types.CallbackQuery) -> None:
        chatid: int = callback_query.message.chat.id
        locale: str = database[chatid]['locale']

        statusmessage: aiog.types.Message = await callback_query.message.answer(ml('imagereq', locale))

        targetid: str = callback_query.data.split(';')[1]
        targetinfo: list = await vk.users.get(user_ids=targetid, fields='photo_max_orig, domain')

        if not len(targetinfo):
            statusmessage.edit_text(ml('usernotexists', locale))
            return

        targetinfo = targetinfo[0]
        targetphotourl: str = targetinfo.photo_max_orig

        # TODO: check: photo is set

        photosize: list = re.findall('size=(.*)&q', targetphotourl)
        photosize = photosize[0] if len(photosize) > 0 else '~x~'

        caption: str = photosize + f'` :: `vk\.com/id{targetid}'

        async with aioh.ClientSession() as session:
            async with session.get(targetphotourl) as photorequest:
                photoio = io.BytesIO(await photorequest.read())

        await bot.send_photo(chatid, photoio, caption)

        photoio.close()
    
    @dp.callback_query_handler(lambda callback_query: callback_query.message.chat.id in database and callback_query.data.startswith('onlinemenu;'))
    async def onlinemenucall(callback_query: aiog.types.CallbackQuery) -> None:
        chatid: int = callback_query.message.chat.id
        locale: str = database[chatid]['locale']

        if database[chatid]['listenonlinestatus']:
            await callback_query.message.answer(ml('listenalready', locale))
            return

        targetid: str = callback_query.data.split(';')[1]

        if targetid == '-1':
            await callback_query.message.answer(ml('unabletime', locale))
            return

        markupinline = aiog.types.InlineKeyboardMarkup()
        listenbutton = aiog.types.InlineKeyboardButton(ml('listenonline', locale), callback_data=f'startlistenonline;{targetid}')
        markupinline.add(listenbutton)

        await callback_query.message.answer(f'{ml("onlinemenuheader", locale)}\n\n👁‍🗨 *ID:* `{targetid}`\n{ml("onlinesleep", locale)}`{database[chatid]["onlinesleep"]}s`\n{ml("offlinesleep", locale)}`{database[chatid]["offlinesleep"]}s`', reply_markup=markupinline)


    @dp.callback_query_handler(lambda callback_query: callback_query.message.chat.id in database and callback_query.data.startswith('startlistenonline;'))
    async def listenonlinecall(callback_query: aiog.types.CallbackQuery) -> None:
        global database
        global islistenthreadrunning

        chatid: int = callback_query.message.chat.id
        locale: str = database[chatid]['locale']
        
        targetid: str = callback_query.data.split(';')[1]

        database[chatid]['listeningid'] = targetid
        database[chatid]['listenonlinestatus'] = True

        markupinline = aiog.types.InlineKeyboardMarkup()
        cancelbutton = aiog.types.InlineKeyboardButton(ml('cancellisten', locale), callback_data=f'interruptlistenonline;')
        markupinline.add(cancelbutton)

        await callback_query.message.edit_text(f'{ml("postonlinemenuheader", locale)}\n\n👁‍🗨 *ID:* `{targetid}`\n{ml("onlinesleep", locale)}`{database[chatid]["onlinesleep"]}s`\n{ml("offlinesleep", locale)}`{database[chatid]["offlinesleep"]}s`', reply_markup=markupinline)

        logger.info(f'start listening: id{targetid}')

        if not islistenthreadrunning:
            aloop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
            islistenthreadrunning = True
            
            lthread = threading.Thread(target=listenthread, args=(bot, aloop))
            lthread.start()

    @dp.callback_query_handler(lambda callback_query: callback_query.message.chat.id in database and callback_query.data.startswith('interruptlistenonline;'))
    async def interruptlisten(callback_query: aiog.types.CallbackQuery) -> None:
        global database

        chatid: int = callback_query.message.chat.id
        locale: str = database[chatid]['locale']

        await callback_query.message.answer(ml('listeninterrupted', locale) if database[chatid]['listenonlinestatus'] else ml('listennotrunning', locale))
        
        database[chatid]['listenonlinestatus'] = False
        logger.info(f'interrupt listening: id{database[chatid]["listeningid"]}')
    
    @dp.callback_query_handler(lambda callback_query: callback_query.message.chat.id in database and callback_query.data.startswith('refresh;'))
    @er.catch
    async def refreshcall(callback_query: aiog.types.CallbackQuery) -> None:
        global vk

        chatid: int = callback_query.message.chat.id
        locale: str = database[chatid]['locale']

        targetid: str = callback_query.data.split(';')[1]
        profileinfo: list = await vk.users.get(user_ids=targetid, fields='status, online, last_seen')

        if not len(profileinfo):
            await callback_query.message.answer(ml('usernotexists', locale))
            return

        profileinfo = profileinfo[0]

        if profileinfo.last_seen is None:
            await callback_query.message.answer(ml('unabletime', locale))
            return

        delta = datetime.timedelta(seconds=int(time.time()) - profileinfo.last_seen.time)
        lastseentime: str = ml('onlinelastseen', locale) % delta if profileinfo.online else ml('offlinelastseen', locale) % delta

        await callback_query.message.answer(f'{mlocales.emoji_detective} *{profileinfo.first_name} {profileinfo.last_name}*` :: `{lastseentime}', 'markdown')
    
    @dp.callback_query_handler(lambda callback_query: callback_query.message.chat.id in database and callback_query.data.startswith('friendsmenu;'))
    async def friendsmenucall(callback_query: aiog.types.CallbackQuery) -> None:
        chatid: int = callback_query.message.chat.id
        locale: str = database[chatid]['locale']

        targetid: str = callback_query.data.split(';')[1]

        markupinline = aiog.types.InlineKeyboardMarkup()
        analyzebutton = aiog.types.InlineKeyboardButton(ml('analyzefriends', locale), callback_data=f'analyzefriends;{targetid}')
        # searchhiddenbutton = aiog.types.InlineKeyboardButton(ml('searchhidden', locale), callback_data=f'searchhidden;{targetid}')
        markupinline.add(analyzebutton) # , searchhiddenbutton)

        await callback_query.message.answer(f'{ml("friendsmenuheader", locale)}\n\n👁‍🗨 *ID:* `{targetid}`', reply_markup=markupinline)

    @dp.callback_query_handler(lambda callback_query: callback_query.message.chat.id in database and callback_query.data.startswith('analyzefriends;'))
    @er.catch
    async def analyzefriendscall(callback_query: aiog.types.CallbackQuery) -> None:
        chatid: int = callback_query.message.chat.id
        locale: str = database[chatid]['locale']
        
        targetid: str = callback_query.data.split(';')[1]

        statusmessage: aiog.types.Message = await callback_query.message.answer(ml('sendreq', locale))
        targetfriends: any = await vk.friends.get(user_id=targetid, fields='city, country, universities')

        await statusmessage.edit_text(ml('parseresp', locale))

        tstart: float = time.time()

        countries: list = []
        cities: list = []
        universities: list = []

        for friend in targetfriends.items:
            if friend.country is not None and re.search('[a-zA-Zа-яА-Я]', friend.country.title):
                countries.append(friend.country.title)

            if friend.city is not None and re.search('[a-zA-Zа-яА-Я]', friend.city.title):
                cities.append(friend.city.title)

            if friend.universities is not None and len(friend.universities) > 0 and re.search('[a-zA-Zа-яА-Я]', friend.universities[0].name):
                universities.append(friend.universities[0].name)

        country: str = commonfromlist(countries)
        city: str = commonfromlist(cities)
        university: str = commonfromlist(universities)

        tend: float = time.time()

        await statusmessage.edit_text(f'{ml("analyzefriendsheader", locale)}\n\n👁‍🗨 *ID:* `{targetid}`\n\n{ml("friendscount", locale)}`{targetfriends.count}`\n{ml("country", locale)}`{country}`\n{ml("city", locale)}`{city}`\n{ml("university", locale)}`{university}`\n{ml("analysistime", locale)}`{round((tend - tstart) * 1000)}ms`')


def main(argc: int, argv: list) -> int:
    global vk
    global er
    global bot
    global dp

    initlogging()

    logger.info('init vkbottle')
    vk = vkbottle.API(token=vk_app_token)
    er = vkbottle.ErrorHandler(True)

    logger.info('init aiogram')
    bot = aiog.Bot(token=tg_bot_token, parse_mode='markdownv2')
    dp = aiog.Dispatcher(bot)

    logger.info('init hooks')
    inithooks()

    logger.info('init callbacks')
    initcallbacks()

    aiog.executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    try:
        status: int = main(len(sys.argv), sys.argv)
    except KeyboardInterrupt:
        status: int = 0
    except Exception as e:
        status: int = 1

        for i in range(1, 6):
            print(f' * ~ {e.__name__}, restarting {i}/5 ...')
            time.sleep(10)

            try:
                status = main()
                break
            except KeyboardInterrupt:
                status = 0
                break
            except Exception:
                pass
    finally:
        sys.exit(status)
