import main
import ekool
import sqlite3
import datetime
import json
import vk_api
import AssignmentTimeframe
import math
import Assignment
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
	id integer PRIMARY KEY,
	userId int NOT NULL,
	logged_in bit DEFAULT 0,
	access_token text DEFAULT NULL,
	refresh_token text DEFAULT NULL,
	joined date,
	language_code char(2) DEFAULT "ru",
	eula bit DEFAULT 0
);
''')
conn.commit()


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def get_day_from_id(id):
    if id == "mo":
        return 0
    if id == "tu":
        return 1
    if id == "we":
        return 2
    if id == "th":
        return 3
    if id == "fr":
        return 4
    if id == "sa":
        return 5
    if id == "su":
        return 6
    else:
        return None


def getDayNameById(id):
    if id == "mo":
        return "Понедельник"
    elif id == "tu":
        return "Вторник"
    elif id == "we":
        return "Среда"
    elif id == "th":
        return "Четверг"
    elif id == "fr":
        return "Пятница"
    elif id == "sa":
        return "Суббота"
    elif id == "su":
        return "Воскресенье"
    else:
        return None

def getCurrDayId(day):
    day = day.lower()
    if day == "monday":
        return "mo"
    elif day == "tuesday":
        return "tu"
    elif day == "wednesday":
        return "we"
    elif day == "thursday":
        return "th"
    elif day == "friday":
        return "fr"
    elif day == "saturday":
        return "sa"
    elif day == "sunday":
        return "su"
    else:
        return None

def getWeekNameById(id):
    if id == "next":
        return "Следующая"
    elif id == "this":
        return "Текущая"
    elif id == "previous":
        return "Предыдущая"
    else:
        return None


def getUser(uid):
    cur.execute('SELECT * FROM users WHERE (userId=?)', (uid,))
    user = cur.fetchone()
    if user is None:
        cur.execute('INSERT INTO users (userId, logged_in, access_token, refresh_token, joined) VALUES (?,?,?,?,?)',
                    (uid, 0, None, None, datetime.date.today()))
        conn.commit()
        return getUser(uid)
    else:
        return user


def updateUser(uid, param, value):
    cur.execute('''UPDATE users SET ''' + param + ''' = ? WHERE userId = ?''', (value, uid))
    conn.commit()
    return getUser(uid)


def processCommand(event, isBotEventType=False):
    if isBotEventType:
        event_obj = event.object
        uid = event_obj.user_id
        command = event_obj.payload.get('type')
        args = [event_obj.payload.get('param')]
    else:
        event_obj = event.obj
        uid = event_obj.message["from_id"]
        text = event.message["text"].split()
        command = text[0].lower()
        text.pop(0)
        args = text

    user = getUser(uid)
    # help
    if command in ['помощь', 'команды', 'help', 'commands']:
        response = "ℹ️ Список команд и помощь по боту можно посмотреть по ссылке:\nhttps://vk.com/@ekool_bot-help"
        return {"error": None, "response": response, "keyboard": None}
    # login
    if command in ['вход', 'войти', 'login']:
        if user[2] != 1:
            if len(args) != 2:
                return {"error": "Неверное использование.\nИспользование:\nвойти ЛОГИН ПАРОЛЬ", "keyboard": None}
            else:
                obj = ekool.bot_login(args[0], args[1])
                if obj["logged_in"] is False:
                    return {"error": "Вход в eKool не удался. Возможно вы указали неверный логин или пароль.",
                            "keyboard": None}
                else:
                    updateUser(uid, "logged_in", 1)
                    updateUser(uid, "access_token", obj["access_token"])
                    updateUser(uid, "refresh_token", obj["refresh_token"])
                    response = "✔️ Успешный вход в аккаунт eKool!\nДоступ к профилю можно получить командой 'профиль'.\n\n⚠️ Рекомендуется удалять сообщения, в которых вы указывали ваши данные для входа."

                    return {"error": None, "response": response, "keyboard": None}
        else:
            ekool_data = ekool.get_person_data(user[3])
            return {"error": f"Уже существует активная сессия ({ekool_data['name1']} {ekool_data['name2']})\nИспользуйте команду 'выйти', чтобы завершить её.",
                    "keyboard": None}
    # logout
    if command in ['выход', 'выйти', 'logout']:
        if user[2] != 0:
            updateUser(uid, "logged_in", 0)
            updateUser(uid, "access_token", None)
            updateUser(uid, "refresh_token", None)
            response = "✔️ Сессия eKool завершена!"
            return {"error": None, "response": response, "keyboard": None}
        else:
            return {"error": "Нет активных сессий eKool.\nВы можете войти, используя команду 'войти'.",
                    "keyboard": None}

    # logout
    if command in ['deletable-msg']:
        keyboard = VkKeyboard(inline=True, one_time=False)
        keyboard.add_callback_button(label="Удалить", color=VkKeyboardColor.NEGATIVE, payload={"type": "delete_msg"})
        return {"error": None, "response": "Удаляемое сообщение", "keyboard": keyboard.get_keyboard()}

    # get grades for role
    if command == "get_grades":
        if user[2] != 0:
            ekool_data = ekool.get_person_data(access_token=user[3])
            response = None
            for role in ekool_data['roles']:
                if len(args) == 0:
                    return {"error": "Не задан ID роли.", "response": response, "keyboard": None}
                if role["studentId"] == args[0]:
                    response = f"📖 Оценки {role['firstName']} ({role['schoolName']})\nФункция пока недоступна."
            if response is not None:
                return {"error": None, "response": response, "keyboard": None}
            else:
                return {"error": "В вашем аккаунте нет такой роли.", "response": response, "keyboard": None}
        else:
            return {"error": "Нет активных сессий eKool.\nВы можете войти, используя команду 'войти'.",
                    "keyboard": None}

    # get todos for role
    if command == "get_todo":
        if user[2] != 0:
            ekool_data = ekool.get_person_data(access_token=user[3])
            keyboard = None
            response = None
            for role in ekool_data['roles']:
                if len(args) == 0:
                    return {"error": "Не задан ID роли.", "response": response, "keyboard": None}
                if role["studentId"] == args[0]:
                    response = f"📖 Задания для {role['firstName']} ({role['schoolName']})"
                    weeks = [{"id": "previous", "name": "Предыдущая неделя", "color": VkKeyboardColor.SECONDARY},
                             {"id": "this", "name": "Текущая неделя", "color": VkKeyboardColor.PRIMARY},
                             {"id": "next", "name": "Следующая неделя", "color": VkKeyboardColor.SECONDARY}]
                    kb = VkKeyboard(inline=True, one_time=False)
                    for i, week in enumerate(weeks):
                        if i:
                            kb.add_line()
                        kb.add_callback_button(label=week['name'], color=week['color'],
                                               payload={"type": "get_todo_week",
                                                        "param": f"{week['id']}:{role['studentId']}"})
                    keyboard = kb.get_keyboard()
            if response is not None:
                return {"error": None, "response": response, "keyboard": keyboard}
            else:
                return {"error": "В вашем аккаунте нет такой роли.", "response": response, "keyboard": None}
        else:
            return {"error": "Нет активных сессий eKool.\nВы можете войти, используя команду 'войти'.",
                    "keyboard": None}

    # get week todos for role
    if command == "get_todo_week":
        if user[2] != 0:
            args = args[0].split(":")
            ekool_data = ekool.get_person_data(access_token=user[3])
            keyboard = None
            response = None
            for role in ekool_data['roles']:
                if len(args) == 0:
                    return {"error": "Не задана неделя и ID роли.", "response": response, "keyboard": None}

                if role["studentId"] == int(args[1]):
                    if args[0] in ["previous", "this", "next"] and getWeekNameById(args[0]) is not None:
                        response = f"📖 Задания для {role['firstName']} ({role['schoolName']})\n📅 {getWeekNameById(args[0])} неделя"
                        days = [{"id": "mo", "name": "Понедельник", "color": VkKeyboardColor.PRIMARY},
                                {"id": "tu", "name": "Вторник", "color": VkKeyboardColor.PRIMARY},
                                {"id": "we", "name": "Среда", "color": VkKeyboardColor.PRIMARY},
                                {"id": "th", "name": "Четверг", "color": VkKeyboardColor.PRIMARY},
                                {"id": "fr", "name": "Пятница", "color": VkKeyboardColor.PRIMARY},
                                {"id": "sa", "name": "Суббота", "color": VkKeyboardColor.NEGATIVE},
                                {"id": "su", "name": "Воскресенье", "color": VkKeyboardColor.NEGATIVE}]
                        kb = VkKeyboard(inline=True, one_time=False)
                        for i, day in enumerate(days):
                            if i & i % 2 != 0:
                                kb.add_line()
                            color = day['color']
                            if args[0] == "this" and getCurrDayId(datetime.datetime.today().strftime("%A")) == day['id']:
                                color = VkKeyboardColor.POSITIVE
                            kb.add_callback_button(label=day['name'], color=color,
                                                       payload={"type": "get_todo_day",
                                                                "param": f"{args[0]}:{day['id']}:{role['studentId']}"})
                        keyboard = kb.get_keyboard()
                    else:
                        return {"error": "Выбран неверный ID недели.", "response": None, "keyboard": None}
            if response is not None:
                return {"error": None, "response": response, "keyboard": keyboard}
            else:
                return {"error": "В вашем аккаунте нет такой роли.", "response": response, "keyboard": None}
        else:
            return {"error": "Нет активных сессий eKool.\nВы можете войти, используя команду 'войти'.",
                    "keyboard": None}

    # get day todos for role
    if command == "get_todo_day":
        if user[2] != 0:
            args = args[0].split(":")
            ekool_data = ekool.get_person_data(access_token=user[3])
            keyboard = None
            response = None
            for role in ekool_data['roles']:
                if len(args) == 0:
                    return {"error": "Не задан день и ID роли.", "response": response, "keyboard": None}

                if role["studentId"] == int(args[2]):
                    if args[0] in ["previous", "this", "next"] and getWeekNameById(args[0]) is not None:
                        if args[1] in ["mo", "tu", "we", "th", "fr", "sa", "su"] and getDayNameById(args[1]) is not None and get_day_from_id(args[1]) is not None:
                            this_monday = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
                            if args[0] == "previous":
                                start_delta = this_monday + datetime.timedelta(days=get_day_from_id(args[1]), weeks=-1)
                            elif args[0] == "this":
                                start_delta = this_monday + datetime.timedelta(days=get_day_from_id(args[1]), weeks=0)
                            elif args[0] == "next":
                                start_delta = this_monday + datetime.timedelta(days=get_day_from_id(args[1]), weeks=1)
                            else:
                                return {"error": "Выбран неверный ID недели.", "response": None, "keyboard": None}

                            todos = ekool.get_assignments_for_timeframe(startingDate=start_delta, endDate=start_delta, access_token=user[3], student_id=role['studentId'])
                            assignments = todos.assignments
                            sep = "----------------------------------\n"
                            todo_content = ""
                            keyboard = None
                            kb = None
                            attachments = []
                            if len(assignments) > 0:
                                for i, assignment in enumerate(assignments):
                                    files_content = ""
                                    is_done = "❌"
                                    if assignment.is_done:
                                        is_done = "✔"
                                    if i:
                                        todo_content += sep
                                    if assignment.teacher_attachments is not None:
                                        files_content = "\n\n🔗 Файлы учителя:\n"
                                        for i, attachment in enumerate(assignment.teacher_attachments):
                                            if i:
                                                files_content += "\n"
                                            attachments.append(attachment)
                                            files_content += f"{i+1}. {attachment['fileName']} ({convert_size(attachment['size'])})"
                                    todo_content += f"{is_done} {assignment.subject_name} • {assignment.title}\n{assignment.content}{files_content}\n"

                                if len(attachments) != 0:
                                    kb = VkKeyboard(one_time=False, inline=True)
                                    for i, attachment in enumerate(attachments):
                                        if i:
                                            kb.add_line()
                                        kb.add_callback_button(label=f"{attachment['fileName']} ({convert_size(attachment['size'])})",color=VkKeyboardColor.PRIMARY, payload={"type": "open_link","link": f"https://ekool.eu{attachment['url']}"})

                                    if kb is not None:
                                        keyboard = kb.get_keyboard()
                                todo_content += sep
                            todo_content = todo_content.replace('</strong>', '').replace('<strong>', '').replace('&laquo;', '«').replace('&quot;', '"').replace('&raquo;', '»').replace('<br />', '\n').replace('&nbsp;', '').replace('<body>', '').replace('<p>', '\n').replace('<br>', '\n').replace('<br>', '').replace('</ol>', '').replace('<ol>', '').replace('</body>', '').replace('</p>', '').replace('</li>', '').replace('<li>', '').replace('</a>',' ').replace('" target="_blank">',' ').replace('<a href="','')
                            if len(todo_content) == 0:
                                todo_content = "Заданий не назначено."
                            response = f"📖 Задания для {role['firstName']} ({role['schoolName']})\n📅 {getWeekNameById(args[0])} неделя, {getDayNameById(args[1])}\n{sep}{todo_content}"
                        else:
                            return {"error": "Выбран неверный ID дня.", "response": None, "keyboard": None}
                    else:
                        return {"error": "Выбран неверный ID недели.", "response": None, "keyboard": None}
            if response is not None:
                return {"error": None, "response": response, "keyboard": keyboard}
            else:
                return {"error": "В вашем аккаунте нет такой роли.", "response": response, "keyboard": None}
        else:
            return {"error": "Нет активных сессий eKool.\nВы можете войти, используя команду 'войти'.",
                    "keyboard": None}

    # get absences for role
    if command == "get_absences":
        if user[2] != 0:
            ekool_data = ekool.get_person_data(access_token=user[3])
            response = None
            for role in ekool_data['roles']:
                if len(args) == 0:
                    return {"error": "Не задан ID роли.", "response": response, "keyboard": None}
                if role["studentId"] == args[0]:
                    absences = ekool.get_absences(access_token=user[3], student_id=role['studentId'])
                    abs_content = ""
                    for i, absence in enumerate(absences):
                        if i:
                            abs_content += "\n"
                        abs_content += f"[{absence['code']}] {absence['lessonDate']}: {absence['subjectName']} ({absence['lessonNumber']})"
                    response = f"📖 Отсутствия {role['firstName']} за 3 месяца ({role['schoolName']})\n{abs_content}"
            if response is not None:
                return {"error": None, "response": response, "keyboard": None}
            else:
                return {"error": "В вашем аккаунте нет такой роли.", "response": response, "keyboard": None}
        else:
            return {"error": "Нет активных сессий eKool.\nВы можете войти, используя команду 'войти'.",
                    "keyboard": None}

    # get-role (for btn payload)
    if command == "get_role":
        if user[2] != 0:
            ekool_data = ekool.get_person_data(access_token=user[3])
            response = None
            error = "В вашем аккаунте нет такой роли."
            for role in ekool_data['roles']:
                if len(args) == 0:
                    return {"error": "Не задан ID роли.", "response": response, "keyboard": None}
                if role["studentId"] == args[0]:
                    new_grades = ""
                    new_todo = ""
                    new_abs = ""
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    if role["timetableUrl"] is not None:
                        keyboard.add_callback_button(
                            label="📅 Расписание",
                            color=VkKeyboardColor.SECONDARY,
                            payload={"type": "open_link", "link": role['timetableUrl']}
                        )
                        keyboard.add_line()

                    if role['newGrades'] > 0:
                        new_grades = f" ({role['newGrades']} новых)"
                    keyboard.add_callback_button(
                        label="Оценки" + new_grades,
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": "get_grades", "param": role['studentId']}
                    )
                    keyboard.add_line()
                    if role['newTodos'] > 0:
                        new_todo = f" ({role['newTodos']} новых)"
                    keyboard.add_callback_button(
                        label="Задания" + new_todo,
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": "get_todo", "param": role['studentId']}
                    )
                    keyboard.add_line()
                    if role['newAbsences'] > 0:
                        new_abs = f" ({role['newAbsences']} новых)"
                    keyboard.add_callback_button(
                        label="Отсутствия" + new_abs,
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": "get_absences", "param": role['studentId']}
                    )
                    response = f"👥 {role['schoolName']}\n👤 {role['firstName']} {role['lastName']}"
            if response is not None:
                return {"error": None, "response": response, "keyboard": keyboard.get_keyboard()}
            else:
                return {"error": error, "response": response, "keyboard": None}
        else:
            return {"error": "Нет активных сессий eKool.\nВы можете войти, используя команду 'войти'.",
                    "keyboard": None}

    # profile
    if command in ['профиль', 'аккаунт', 'account', 'profile']:
        main_data = f"📅 Первое появление: {user[5]}"
        ekool_sess_data = "⚠️ Нет активных сессий."
        keyboard_use = None
        if user[2] != 0:
            ekool_data = ekool.get_person_data(access_token=user[3])
            ekool_sess_data = f"👤 {ekool_data['name1']} {ekool_data['name2']} ({ekool_data['adData']['age'][0]})\n👥 Доступные роли: {len(ekool_data['roles'])}"
            keyboard = VkKeyboard(one_time=False, inline=True)
            keyboard.add_callback_button(
                label=f"Роли",
                color=VkKeyboardColor.PRIMARY,
                payload={"type": "roles", "param": None}
            )
            keyboard_use = keyboard.get_keyboard()
        response = f"Ваш профиль:\n{main_data}\n\nСессия eKool:\n{ekool_sess_data}"
        return {"error": None, "response": response, "keyboard": keyboard_use}
    # roles
    if command in ['роли', 'roles']:
        if user[2] != 0:
            ekool_data = ekool.get_person_data(access_token=user[3])
            if len(ekool_data['roles']) > 0:
                response = f"👥 Доступные роли ({len(ekool_data['roles'])})"
                keyboard = VkKeyboard(one_time=False, inline=True)
                for i, role in enumerate(ekool_data['roles']):
                    if i:
                        keyboard.add_line()
                    keyboard.add_callback_button(
                        label=f"{str(role['schoolName'])} ({role['firstName']} {role['lastName'][0]})",
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": "get_role", "param": role['studentId']}
                    )

                return {"error": None, "response": response, "keyboard": keyboard.get_keyboard()}
            else:
                return {"error": None, "response": f"👥 У вас нет ни одной роли.", "keyboard": None}
        else:
            return {"error": "Нет активных сессий eKool.", "keyboard": None}

    # not found
    else:
        return {
            "error": "Команда не найдена, список команд и помощь по боту можно посмотреть по ссылке:\nhttps://vk.com/@ekool_bot-help",
            "keyboard": None}
