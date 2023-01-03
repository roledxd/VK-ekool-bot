error = {"ru": "ошибка", "et": "viga", "en": "error"}
settings = {"ru": "настройки", "et": "seaded", "en": "settings"}
account = {"ru": "аккаунт", "et": "konto", "en": "account"}
help = {"ru": "помощь", "et": "abi", "en": "help"}
usage = {"ru": "использование", "et": "kasutamine", "en": "usage"}
no_tasks = {"ru": "заданий нет.", "et": "ülesandeid ei ole.", "en": "no tasks."}
request_error = {"ru": "при выполнении запроса произошла ошибка.", "et": "päringu käivitamisel ilmnes viga",
                 "en": "an error occurred while executing the request"}
invalid_day = {"ru": "Неверно указан день.", "et": "Vigane päev.", "en": "Invalid day."}
days_array = {"ru": "[пн|вт|ср|чт|пт|сб|вс]", "et": "[e|t|k|n|r|l|p]", "en": "[mo|tu|we|th|fr|sa|su]"}
try_ = {"ru": "попробуйте", "et": "proovi", "en": "try"}
again = {"ru": "снова", "et": "uuesti", "en": "again"}
please_wait = {"ru": "пожалуйста, подождите...", "et": "palun oodake...", "en": "please, wait..."}
have_active_account = {"ru": "у вас уже есть активный аккаунт", "et": "teil juba on aktiivne konto",
                       "en": "you already have an active account"}
you_can_sign_out = {"ru": "вы можете закончить сессию аккаунта, использовав команду /signout",
                    "et": "te võite lõpetada konto seanss käsuga /signout",
                    "en": "you can end the account session by using the /signout command"}
username = {"ru": "логин", "et": "kasutajanimi", "en": "username"}
password = {"ru": "пароль", "et": "salasõna", "en": "password"}
wrong_credentials = {"ru": "неверный логин или пароль", "et": "vigane kasutajanimi või salasõna",
                     "en": "invalid username or password"}
no_active_sessions = {"ru": "активных сессий не найдено, вы можете авторизоваться использовав команду /signin",
                      "et": "seansside ei leita, saate sisse logida kasutades käsku /signin",
                      "en": "no active sessions found, you can sign-in using the /signin command"}
success_signout = {"ru": "вы успешно вышли из активного аккаунта", "et": "olete edukalt lahkusid aktiivne konto",
                   "en": "you have successfully logged out of your active account"}
value_alr_using = {"ru": "данное значение уже используется", "et": "see väärtus on juba kasutusel",
                   "en": "this value is already sin use"}
for_ = {"ru": "для", "et": "jaoks", "en": "for"}
tasks = {"ru": "задания", "et": "ülesanded", "en": "tasks"}
grades = {"ru": "оценки", "et": "hinned", "en": "grades"}
to_see_sa_su = {"ru": "для того чтобы посмотреть задания на Субботу и Воскресенье, используйте '/todo сб' и '/todo вс'",
                "et": "selleks, et näha ülesanded Laupäeval ja Pühapäeval, kasutage '/todo l' ja '/todo p'",
                "en": "to view the tasks for Saturday and Sunday, use '/todo sa' and '/todo su'"}
value_set = {"ru": "значение задано", "et": "väärtus on määratud", "en": "the value is set"}
invalid_value = {"ru": "неверное значение", "et": "vigane väärtus", "en": "invalid value"}
available_values = {"ru": "доступные значения", "et": "olemasolevad väärtused", "en": "available values"}

monday = {"ru": "Понедельник", "et": "Esmaspäev", "en": "Monday"}
tuesday = {"ru": "Вторник", "et": "Teisipäev", "en": "Tuesday"}
wednesday = {"ru": "Среда", "et": "Kolmapäev", "en": "Wednesday"}
thursday = {"ru": "Четверг", "et": "Neljapäev", "en": "Thursday"}
friday = {"ru": "Пятница", "et": "Reede", "en": "Friday"}
saturday = {"ru": "Суббота", "et": "Laupäev", "en": "Saturday"}
sunday = {"ru": "Воскресенье", "et": "Pühapäev", "en": "Sunday"}

monday_short = {"ru": "пн", "et": "e", "en": "mo"}
tuesday_short = {"ru": "вт", "et": "t", "en": "tu"}
wednesday_short = {"ru": "ср", "et": "k", "en": "we"}
thursday_short = {"ru": "чт", "et": "n", "en": "th"}
friday_short = {"ru": "пт", "et": "r", "en": "fr"}
saturday_short = {"ru": "сб", "et": "l", "en": "sa"}
sunday_short = {"ru": "вс", "et": "p", "en": "su"}

err_no_groups = {"ru": "Вы не состоите в образовательном учреждении", "et": "Te ei ole haridusasutuse liige",
                 "en": "You are not in an educational institution"}

# help cmd desc
cmd = {
    'help': {"ru": "список команд бота", "et": "botide käskude loend", "en": "bot command list"},
    'sign_in': {"ru": "привязать аккаунт eKool", "et": "lisage eKooli konto", "en": "add eKool account"},
    'sign_out': {"ru": "отвязать аккаунт eKool", "et": "kustuta eKooli konto", "en": "remove eKool account"},
    'lang': {"ru": "сменить язык бота", "et": "muutke boti keelt", "en": "change bot language"},
    'account': {"ru": "ваш аккаунт", "et": "teie konto", "en": "your account"},
    'todo': {"ru": "ваши задания", "et": "teie ülesandeid", "en": "your assignments"},
    'todo_day': {"ru": "ваши задания на конкретный день", "et": "teie konkreetse päeva ülesanded",
                 "en": "your assignments for a specific day"}
}

signed_in = {"ru": "вы успешно авторизовались через eKool ", "et": "olete eKooli kaudu edukalt sisse loginud",
             "en": "you have successfully logged in via eKool"}

err = {
    'error': {"ru": "список команд бота", "et": "botide käskude loend", "en": "bot command list"},
    'request': {"ru": "при выполнении запроса произошла ошибка.", "et": "päringu käivitamisel ilmnes viga",
                "en": "an error occurred while executing the request"},
    'sess_expired': {"ru": "ваша ekool сессия истекла, авторизуйтесь еще раз, используя команду /signin",
                     "et": "teie ekooli seanss on aegunud, logige uuesti sisse, kasutades /signin käsku",
                     "en": "your ekool session has expired, log in again using the / signin command"},
}

account_info = {
    "title": {"ru": "Аккаунт", "et": "Konto", "en": "Account"},
    "name": {"ru": "Имя", "et": "Nimi", "en": "Name"},
    "gender": {"ru": "Пол", "et": "Sugu", "en": "Gender"},
    "age": {"ru": "Возраст", "et": "Vanus", "en": "Age"},
    "premium": {"ru": "Премиум", "et": "Perepakett", "en": "Premium"},
    "roles": {"ru": "Роли", "et": "Rollid", "en": "Roles"},
    "photo": {"ru": "Фото профиля", "et": "Foto", "en": "Profile photo"},
    "language": {"ru": "Язык", "et": "Boti keel", "en": "Bot Language"},
    "joined": {"ru": "Присоединился", "et": "Ühendatud", "en": "Joined"},
    "yes": {"ru": "Да", "et": "Jah", "en": "Yes"},
    "no": {"ru": "Нет", "et": "Ei", "en": "No"},
}

open = {"ru": "открыть", "et": "ava", "en": "open"}

gender = {
    "male": {"ru": "Мужчина", "et": "Mees", "en": "Male"},
    "female": {"ru": "Женщина", "et": "Naine", "en": "Female"},
    "other": {"ru": "Другое", "et": "Teise", "en": "Other"},
}
