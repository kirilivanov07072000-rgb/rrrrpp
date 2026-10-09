<<<<<<< HEAD
import streamlit as st
import random
import time
from datetime import datetime

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="EduCasino Ultimate Edition", page_icon="🎰", layout="centered")

# --- ИНИЦИАЛИЗА СОСТОЯНИЯ ---
if "coins" not in st.session_state:
    st.session_state.coins = 150
if "score" not in st.session_state:
    st.session_state.score = 0

# Элементы состояния для Статистики и Достижений
if "cases_opened" not in st.session_state:
    st.session_state.cases_opened = 0
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0
if "roulette_spins" not in st.session_state:
    st.session_state.roulette_spins = 0
if "last_daily_claim" not in st.session_state:
    st.session_state.last_daily_claim = None
if "last_work_time" not in st.session_state:
    st.session_state.last_work_time = 0  # Кулдаун подработки (timestamp)

# Расширенная система ачивок
ACHIEVEMENTS_LIST = {
    "first_win": {"title": "🌱 Первый шаг", "desc": "Дать 1 правильный ответ", "reward": 25},
    "case_master": {"title": "📦 Любитель коробок", "desc": "Открыть 5 кейсов", "reward": 50},
    "case_addict": {"title": "💼 Кейсоголик", "desc": "Открыть 25 кейсов", "reward": 150},
    "high_roller": {"title": "💰 Магнат", "desc": "Накопить 500 монет", "reward": 100},
    "millionaire": {"title": "👑 Рокфеллер", "desc": "Накопить 1500 монет", "reward": 300},
    "scholar": {"title": "🎓 Эрудит", "desc": "Разблокировать 6+ дисциплин", "reward": 120},
    "polymath": {"title": "🏛️ Профессор", "desc": "Разблокировать 12+ дисциплин", "reward": 300},
    "roulette_fan": {"title": "🎡 Рисковый игрок", "desc": "Сделать 10 спинов в рулетке", "reward": 75},
    "smart_mind": {"title": "🧠 Гений", "desc": "Дать 10 правильных ответов", "reward": 100},
    "workaholic": {"title": "💼 Трудоголик", "desc": "Выполнить 5 подработок", "reward": 50},
}

if "achievements" not in st.session_state:
    st.session_state.achievements = {k: False for k in ACHIEVEMENTS_LIST.keys()}
if "claimed_achievements" not in st.session_state:
    st.session_state.claimed_achievements = {k: False for k in ACHIEVEMENTS_LIST.keys()}
if "work_completed" not in st.session_state:
    st.session_state.work_completed = 0

ACHIEVEMENT_THEMES = {
    "🏆 Золотая Лига (Golden League)": {
        "bg": "#1a1608", "sidebar": "#26200c", "btn_start": "#854d0e", "btn_end": "#ca8a04", "accent": "#facc15", "card": "#332a10"
    },
    "💎 Алмазный Ранг (Diamond Rank)": {
        "bg": "#0b192c", "sidebar": "#112238", "btn_start": "#1e3a8a", "btn_end": "#2563eb", "accent": "#60a5fa", "card": "#172a45"
    },
    "🌌 Неоновый Азарт (Neon Cyber)": {
        "bg": "#180828", "sidebar": "#230c3a", "btn_start": "#701a75", "btn_end": "#c026d3", "accent": "#f0abfc", "card": "#2e104d"
    },
    "⚔️ Темный Рыцарь (Dark Legend)": {
        "bg": "#111827", "sidebar": "#1f2937", "btn_start": "#374151", "btn_end": "#4b5563", "accent": "#9ca3af", "card": "#1f2937"
    }
}

if "theme_name" not in st.session_state:
    st.session_state.theme_name = "🏆 Золотая Лига (Golden League)"

if "multiplier_level" not in st.session_state:
    st.session_state.multiplier_level = 1
if "insurance_unlocked" not in st.session_state:
    st.session_state.insurance_unlocked = False

if "unlocked_cats" not in st.session_state:
    st.session_state.unlocked_cats = [
        "🇬🇧 Английский язык (Популярно)", 
        "🇪🇸 Испанский язык (Популярно)", 
        "➕ Арифметика (Популярно)"
    ]

if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "current_rarity" not in st.session_state:
    st.session_state.current_rarity = None
if "current_options" not in st.session_state:
    st.session_state.current_options = None

if "work_q" not in st.session_state:
    st.session_state.work_q = None
if "work_options" not in st.session_state:
    st.session_state.work_options = None

# --- ПРИМЕНЕНИЕ ДИНАМИЧЕСКОЙ ТЕМЫ ---
active_theme = ACHIEVEMENT_THEMES[st.session_state.theme_name]

st.markdown(f"""
<style>
    .stApp {{ background-color: {active_theme['bg']}; color: #e0f2f1; }}
    [data-testid="stSidebar"] {{ background-color: {active_theme['sidebar']}; border-right: 1px solid {active_theme['btn_start']}; }}
    .stButton>button {{
        background: linear-gradient(135deg, {active_theme['btn_start']} 0%, {active_theme['btn_end']} 100%);
        color: #ffffff; border: 1px solid {active_theme['accent']}; border-radius: 8px; font-weight: bold; transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, {active_theme['btn_end']} 0%, {active_theme['accent']} 100%);
        box-shadow: 0px 0px 10px {active_theme['accent']};
    }}
    [data-testid="stMetricValue"] {{ color: {active_theme['accent']} !important; }}
    .stAlert {{ background-color: {active_theme['card']}; color: #e0f2f1; border: 1px solid {active_theme['btn_start']}; }}
    
    .case-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        overflow: hidden;
        padding: 20px;
        background: {active_theme['card']};
        border-radius: 12px;
        border: 2px solid {active_theme['accent']};
        position: relative;
    }}
    .case-card {{
        min-width: 130px;
        height: 100px;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}
    .pointer {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 12px solid transparent;
        border-right: 12px solid transparent;
        border-top: 18px solid #ff4757;
        z-index: 10;
    }}
</style>
""", unsafe_allow_html=True)

# --- КОНФИГУРАЦИЯ ---
CATEGORY_SETTINGS = {
    "🇬🇧 Английский язык (Популярно)": {"cost": 10, "reward_mult": 1.0, "pop": "🔥 Мейнстрим (100% популярность)"},
    "🇪🇸 Испанский язык (Популярно)": {"cost": 10, "reward_mult": 1.0, "pop": "🔥 Мейнстрим (95% популярность)"},
    "➕ Арифметика (Популярно)": {"cost": 15, "reward_mult": 1.2, "pop": "🔥 Мейнстрим (90% популярность)"},
    "🇩🇪 Немецкий язык": {"cost": 25, "reward_mult": 1.6, "pop": "📊 Умеренно (65% популярность)"},
    "🇫🇷 Французский язык": {"cost": 30, "reward_mult": 1.8, "pop": "📊 Умеренно (60% популярность)"},
    "📐 Алгебра и Геометрия": {"cost": 35, "reward_mult": 2.0, "pop": "📊 Умеренно (50% популярность)"},
    "⚡ Классическая Физика": {"cost": 45, "reward_mult": 2.5, "pop": "📊 Умеренно (40% популярность)"},
    "💻 Программирование Python": {"cost": 60, "reward_mult": 3.0, "pop": "📊 Умеренно (35% популярность)"},
    "🇯🇵 Японский язык (Иероглифы)": {"cost": 80, "reward_mult": 4.0, "pop": "🌟 Редкое (20% популярность)"},
    "🏺 Древнегреческая Мифология": {"cost": 100, "reward_mult": 5.0, "pop": "🌟 Редкое (15% популярность)"},
    "🏛️ Латинский язык (Мертвый язык)": {"cost": 130, "reward_mult": 6.5, "pop": "🔮 Экзотика (8% популярность)"},
    "📜 Философия и Логика": {"cost": 160, "reward_mult": 8.0, "pop": "🔮 Экзотика (5% популярность)"},
    "⚛️ Квантовая Физика": {"cost": 220, "reward_mult": 12.0, "pop": "☣️ Нишевое (2% популярность)"},
    "🛸 Клингонский язык (Вымышленный)": {"cost": 300, "reward_mult": 18.0, "pop": "💎 Ультра-экзотика (<1% популярность)"},
    "💀 Dark Souls Математика": {"cost": 400, "reward_mult": 25.0, "pop": "👑 Абсолютный раритет (0.1%)"},
}

RARITY = {
    "Common": {"name": "Обычный ⚪", "color": "#64748b", "base_coins": 15, "weight": 50},
    "Rare": {"name": "Редкий 🔵", "color": "#0284c7", "base_coins": 40, "weight": 30},
    "Epic": {"name": "Эпический 🟣", "color": "#9333ea", "base_coins": 100, "weight": 14},
    "Legendary": {"name": "Легендарный 🟡", "color": "#eab308", "base_coins": 300, "weight": 6},
}

SECRET_QUESTION = {"q": "Кто убил Лёшу Зеленого?", "options": ["Вовочка", "Вовочка", "Вовочка"], "a": "Вовочка"}

QUESTIONS = {
    "🇬🇧 Английский язык (Популярно)": {
        "Common": [
            {"q": "Как переводится 'Apple'?", "options": ["Яблоко", "Груша", "Банан"], "a": "Яблоко"},
            {"q": "Выберите правильный вариант: She ___ happy.", "options": ["is", "are", "am"], "a": "is"},
            {"q": "Как сказать 'Собака' по-английски?", "options": ["Dog", "Cat", "Bird"], "a": "Dog"}
        ],
        "Rare": [
            {"q": "Синоним слова 'Meticulous':", "options": ["Careful", "Fast", "Lazy"], "a": "Careful"},
            {"q": "Антоним слова 'Generous':", "options": ["Stingy", "Kind", "Brave"], "a": "Stingy"},
            {"q": "Прошедшее время от глагола 'Catch':", "options": ["Caught", "Catched", "Cot"], "a": "Caught"}
        ],
        "Epic": [
            {"q": "Значение идиомы 'Spill the beans':", "options": ["Раскрыть секрет", "Рассыпать еду", "Испортить праздник"], "a": "Раскрыть секрет"},
            {"q": "Синоним слова 'Ubiquitous':", "options": ["Omnipresent", "Rare", "Hidden"], "a": "Omnipresent"},
            {"q": "Перевод фразового глагола 'To call off':", "options": ["Отменить", "Позвонить", "Вызвать"], "a": "Отменить"}
        ],
        "Legendary": [
            {"q": "Значение 'Bite the bullet':", "options": ["Принять трудное решение", "Выстрелить", "Сдаться"], "a": "Принять трудное решение"},
            {"q": "Что означает выражение 'Barking up the wrong tree'?", "options": ["Искать не там", "Шуметь в лесу", "Обижать животных"], "a": "Искать не там"},
            {"q": "Что значит 'Burn the midnight oil'?", "options": ["Усердно работать ночью", "Устроить пожар", "Тратить ресурсы"], "a": "Burn the midnight oil"}
        ]
    },
    "🇪🇸 Испанский язык (Популярно)": {
        "Common": [
            {"q": "Как переводится 'Hola'?", "options": ["Привет", "Пока", "Спасибо"], "a": "Привет"},
            {"q": "Как сказать 'Спасибо' по-испански?", "options": ["Gracias", "Por favor", "De nada"], "a": "Gracias"},
            {"q": "Перевод слова 'Gato':", "options": ["Кот", "Собака", "Птица"], "a": "Кот"}
        ],
        "Rare": [
            {"q": "Как сказать 'Завтра' по-испански?", "options": ["Mañana", "Ayer", "Hoy"], "a": "Mañana"},
            {"q": "Перевод слова 'Hermano':", "options": ["Брат", "Сестра", "Отец"], "a": "Брат"},
            {"q": "Форма глагола ser для 'Мы' (Nosotros):", "options": ["Somos", "Sois", "Son"], "a": "Somos"}
        ],
        "Epic": [
            {"q": "Форма Subjuntivo от глагола hablar (yo):", "options": ["Hable", "Hablo", "Hablaría"], "a": "Hable"},
            {"q": "Перевод фразы 'Por si acaso':", "options": ["На всякий случай", "Наконец-то", "По ошибке"], "a": "На всякий случай"},
            {"q": "Значение слова 'Desarrollo':", "options": ["Развитие", "Ошибка", "Завершение"], "a": "Развитие"}
        ],
        "Legendary": [
            {"q": "Что значит 'Estar en las nubes'?", "options": ["Витать в облаках", "Быть злым", "Летать"], "a": "Витать в облаках"},
            {"q": "Перевод идиомы 'Costar un ojo de la cara':", "options": ["Стоить бешеных денег", "Смотреть внимательно", "Быть красивым"], "a": "Стоить бешеных денег"},
            {"q": "Что означает 'Tomar el pelo'?", "options": ["Морочить голову", "Стричь волосы", "Уважать"], "a": "Морочить голову"}
        ]
    },
    "➕ Арифметика (Популярно)": {
        "Common": [
            {"q": "Сколько будет 7 × 8?", "options": ["56", "54", "64"], "a": "56"},
            {"q": "Результат выражения 144 ÷ 12:", "options": ["12", "14", "10"], "a": "12"},
            {"q": "Сколько будет 45 + 37?", "options": ["82", "80", "85"], "a": "82"}
        ],
        "Rare": [
            {"q": "Чему равен 15% от 200?", "options": ["30", "25", "35"], "a": "30"},
            {"q": "Найдите квадрат числа 14:", "options": ["196", "186", "206"], "a": "196"},
            {"q": "Результат: 2⁵ =", "options": ["32", "64", "16"], "a": "32"}
        ],
        "Epic": [
            {"q": "Чему равен ∛216?", "options": ["6", "8", "4"], "a": "6"},
            {"q": "Найдите НОК чисел 12 и 18:", "options": ["36", "72", "24"], "a": "36"},
            {"q": "Результат: 7! ÷ 5! =", "options": ["42", "35", "56"], "a": "42"}
        ],
        "Legendary": [
            {"q": "Найдите НОД чисел 84 и 126:", "options": ["42", "21", "14"], "a": "42"},
            {"q": "Сумма первых 10 натуральных чисел:", "options": ["55", "50", "60"], "a": "55"},
            {"q": "Чему равен остаток от деления 2¹⁰⁰ на 3?", "options": ["1", "2", "0"], "a": "1"}
        ]
    },
    "🇩🇪 Немецкий язык": {
        "Common": [
            {"q": "Как переводится 'Guten Tag'?", "options": ["Добрый день", "Доброе утро", "До свидания"], "a": "Добрый день"},
            {"q": "Как сказать 'Кот' по-немецки?", "options": ["Katze", "Hund", "Vogel"], "a": "Katze"},
            {"q": "Артикль женского рода в немецком:", "options": ["die", "der", "das"], "a": "die"}
        ],
        "Rare": [
            {"q": "Как переводится глагол 'Verstehen'?", "options": ["Понимать", "Слышать", "Смотреть"], "a": "Понимать"},
            {"q": "Прошедшее время (Partizip II) от 'machen':", "options": ["gemacht", "gemachen", "machte"], "a": "gemacht"},
            {"q": "Что значит 'Аптека' на немецком?", "options": ["Apotheke", "Bibliothek", "Krankenhaus"], "a": "Apotheke"}
        ],
        "Epic": [
            {"q": "Какой предлог требует Dativ?", "options": ["mit", "durch", "für"], "a": "mit"},
            {"q": "Перевод слова 'Sehenswoerdigkeit':", "options": ["Достопримечательность", "Предсказание", "Безопасность"], "a": "Достопримечательность"},
            {"q": "Форма Präteritum от 'sein' (ich):", "options": ["war", "bin", "gewesen"], "a": "war"}
        ],
        "Legendary": [
            {"q": "Значение идиомы 'Da liegt der Hund begraben':", "options": ["Вот где собака зарыта", "Собака спит", "Начать сначала"], "a": "Вот где собака зарыта"},
            {"q": "Что означает 'Um den heißen Brei herumreden'?", "options": ["Ходить вокруг да около", "Готовить еду", "Быстро говорить"], "a": "Ходить вокруг да около"},
            {"q": "Перевод 'Schadenfreude':", "options": ["Злорадство", "Сочувствие", "Обида"], "a": "Злорадство"}
        ]
    },
    "🇫🇷 Французский язык": {
        "Common": [
            {"q": "Как сказать 'Привет' по-французски?", "options": ["Salut", "Bonjour", "Merci"], "a": "Salut"},
            {"q": "Перевод слова 'Chat':", "options": ["Кот", "Собака", "Птица"], "a": "Кот"},
            {"q": "Как будет 'Спасибо'?", "options": ["Merci", "S'il vous plaît", "Pardon"], "a": "Merci"}
        ],
        "Rare": [
            {"q": "Как переводится 'Aujourd'hui'?", "options": ["Сегодня", "Завтра", "Вчера"], "a": "Сегодня"},
            {"q": "Форма глагола être для 'Nous':", "options": ["sommes", "êtes", "sont"], "a": "sommes"},
            {"q": "Что значит 'La maison'?", "options": ["Дом", "Машина", "Улица"], "a": "Дом"}
        ],
        "Epic": [
            {"q": "Форма Subjonctif от 'avoir' (que j'___):", "options": ["aie", "avais", "aurai"], "a": "aie"},
            {"q": "Перевод выражения 'C'est la vie':", "options": ["Такова жизнь", "Это мечта", "Всё хорошо"], "a": "Такова жизнь"},
            {"q": "Что означает 'Écureuil'?", "options": ["Белка", "Заяц", "Волк"], "a": "Белка"}
        ],
        "Legendary": [
            {"q": "Значение идиомы 'Avoir le coup de foudre':", "options": ["Влюбиться с первого взгляды", "Испугаться грозы", "Быстро побежать"], "a": "Влюбиться с первого взгляды"},
            {"q": "Что значит 'Poser un lapin'?", "options": ["Продинамить (не прийти)", "Подарить кролика", "Сделать фокус"], "a": "Продинамить (не прийти)"},
            {"q": "Перевод идиомы 'Appeler un chat un chat':", "options": ["Называть вещи своими именами", "Звать кота", "Шуметь"], "a": "Называть вещи своими именами"}
        ]
    },
    "📐 Алгебра и Геометрия": {
        "Common": [
            {"q": "Чему равна сумма углов треугольника?", "options": ["180°", "360°", "90°"], "a": "180°"},
            {"q": "Дискриминант уравнения x² - 4x + 3 = 0:", "options": ["4", "16", "8"], "a": "4"},
            {"q": "Площадь прямоугольника со сторонами a и b:", "options": ["S = a · b", "S = 2(a + b)", "S = a² + b²"], "a": "S = a · b"}
        ],
        "Rare": [
            {"q": "Гипотенуза треугольника с катетами 3 и 4:", "options": ["5", "7", "6"], "a": "5"},
            {"q": "Найдите корни уравнения x² - 9 = 0:", "options": ["±3", "3", "81"], "a": "±3"},
            {"q": "Чему равна площадь круга радиуса R?", "options": ["πR²", "2πR", "πD"], "a": "πR²"}
        ],
        "Epic": [
            {"q": "Чему равен sin(30°)?", "options": ["1/2", "√3/2", "√2/2"], "a": "1/2"},
            {"q": "Формула объема шара радиуса R:", "options": ["(4/3)πR³", "4πR²", "πR³"], "a": "(4/3)πR³"},
            {"q": "Вершина параболы y = (x - 2)² + 5:", "options": ["(2, 5)", "(-2, 5)", "(2, -5)"], "a": "(2, 5)"}
        ],
        "Legendary": [
            {"q": "Чему равен log₂32?", "options": ["5", "4", "6"], "a": "5"},
            {"q": "Производная функции f(x) = x³:", "options": ["3x²", "x²", "3x"], "a": "3x²"},
            {"q": "Теорема косинусов для стороны c:", "options": ["c² = a² + b² - 2ab·cos(γ)", "c² = a² + b² + 2ab·cos(γ)", "c = a + b - cos(γ)"], "a": "c² = a² + b² - 2ab·cos(γ)"}
        ]
    },
    "⚡ Классическая Физика": {
        "Common": [
            {"q": "Единица измерения силы в СИ:", "options": ["Ньютон", "Джоуль", "Ватт"], "a": "Ньютон"},
            {"q": "Формула 2-го закона Ньютона:", "options": ["F = m·a", "F = m·v", "E = m·c²"], "a": "F = m·a"},
            {"q": "Ускорение свободного падения на Земле ≈", "options": ["9.8 м/с²", "5.2 м/с²", "12.4 м/с²"], "a": "9.8 м/с²"}
        ],
        "Rare": [
            {"q": "Формула кинетической энергии:", "options": ["E = (m·v²)/2", "E = m·g·h", "P = U·I"], "a": "E = (m·v²)/2"},
            {"q": "Закон Ома для участка цепи:", "options": ["I = U / R", "U = I / R", "R = U · I"], "a": "I = U / R"},
            {"q": "В чем измеряется электрическая емкость?", "options": ["Фарад", "Генри", "Тесла"], "a": "Фарад"}
        ],
        "Epic": [
            {"q": "Формула периода колебаний математического маятника:", "options": ["T = 2π√(l/g)", "T = 2π√(m/k)", "T = 1/f"], "a": "T = 2π√(l/g)"},
            {"q": "Закон Стефана-Больцмана определяет излучение:", "options": ["Абсолютно черного тела", "Газов", "Металлов"], "a": "Абсолютно черного тела"},
            {"q": "Чему равна скорость света в вакууме?", "options": ["3·10⁸ м/с", "3·10⁶ м/с", "1.5·10⁸ м/с"], "a": "3·10⁸ м/с"}
        ],
        "Legendary": [
            {"q": "Уравнение состояния идеального газа (Менделеева-Клапейрона):", "options": ["P·V = (m/M)·R·T", "P·V = const", "V/T = const"], "a": "P·V = (m/M)·R·T"},
            {"q": "Формула циклической частоты для LC-контура (Томсона):", "options": ["ω = 1 / √(L·C)", "T = 2π·L·C", "f = L / C"], "a": "ω = 1 / √(L·C)"},
            {"q": "Что утверждает второй закон термодинамики?", "options": ["Энтропия замкнутой системы не убывает", "Энергия сохраняется", "Абсолютный ноль достижим"], "a": "Энтропия замкнутой системы не убывает"}
        ]
    },
    "💻 Программирование Python": {
        "Common": [
            {"q": "Как вывести текст в консоль Python?", "options": ["print()", "console.log()", "System.out.println()"], "a": "print()"},
            {"q": "Какой тип данных у числа 3.14?", "options": ["float", "int", "str"], "a": "float"},
            {"q": "Как начинается комментарий в Python?", "options": ["#", "//", "/*"], "a": "#"}
        ],
        "Rare": [
            {"q": "Результат выражения 10 // 3:", "options": ["3", "3.33", "1"], "a": "3"},
            {"q": "Какой метод добавляет элемент в конец списка?", "options": ["append()", "push()", "add()"], "a": "append()"},
            {"q": "Что делает ключевое слово `len()`?", "options": ["Возвращает длину объекта", "Удаляет объект", "Сортирует"], "a": "Возвращает длину объекта"}
        ],
        "Epic": [
            {"q": "Какая структура данных является неизменяемой?", "options": ["tuple", "list", "dict"], "a": "tuple"},
            {"q": "Сложность поиска элемента по ключу в dict:", "options": ["O(1)", "O(n)", "O(log n)"], "a": "O(1)"},
            {"q": "Результат кода `[x*2 for x in range(3)]`:", "options": ["[0, 2, 4]", "[2, 4, 6]", "[0, 1, 2]"], "a": "[0, 2, 4]"}
        ],
        "Legendary": [
            {"q": "Что делает декоратор `@staticmethod`?", "options": ["Убирает передачу self/cls", "Делает метод приватным", "Кэширует результат"], "a": "Убирает передачу self/cls"},
            {"q": "Какова область видимости переменных в генераторах (PEP 289)?", "options": ["Локальная для генератора", "Глобальная", "Функциональная"], "a": "Локальная для генератора"},
            {"q": "Что такое GIL в CPython?", "options": ["Global Interpreter Lock", "General Input Loop", "Global Integrated Layer"], "a": "Global Interpreter Lock"}
        ]
    },
    "🇯🇵 Японский язык (Иероглифы)": {
        "Common": [
            {"q": "Что означает иероглиф 日?", "options": ["Солнце / День", "Луна", "Дерево"], "a": "Солнце / День"},
            {"q": "Что означает иероглиф 人?", "options": ["Человек", "Огонь", "Вода"], "a": "Человек"},
            {"q": "Как переводится 'Arigatou'?", "options": ["Спасибо", "Привет", "Простите"], "a": "Спасибо"}
        ],
        "Rare": [
            {"q": "Чтение иероглифа 水 (Вода):", "options": ["Mizu", "Ki", "Hi"], "a": "Mizu"},
            {"q": "Что означает иероглиф 山?", "options": ["Гора", "Река", "Поле"], "a": "Гора"},
            {"q": "Слоговая азбука для заимствованных слов:", "options": ["Катакана", "Хирагана", "Кандзи"], "a": "Катакана"}
        ],
        "Epic": [
            {"q": "Значение иероглифа 猫:", "options": ["Кошка", "Собака", "Тигр"], "a": "Кошка"},
            {"q": "Перевод слова 'Sakura' (桜):", "options": ["Вишня", "Сосна", "Бамбук"], "a": "Вишня"},
            {"q": "Что означает иероглиф 電 (Дэн)?", "options": ["Электричество", "Гром", "Огонь"], "a": "Электричество"}
        ],
        "Legendary": [
            {"q": "Что означает фразеологизм 一期一会 (Ichigo Ichie)?", "options": ["Один раз в жизни (уникальная встреча)", "Семь раз отмерь", "Быстротечность времени"], "a": "Один раз в жизни (уникальная встреча)"},
            {"q": "Чтение сочетания 忍者:", "options": ["Ninja", "Samurai", "Geisha"], "a": "Ninja"},
            {"q": "Что означает выражение 四面楚歌 (Shimenchoka)?", "options": ["Окружен врагами со всех сторон", "Успех во всем", "Красота природы"], "a": "Окружен врагами со всех сторон"}
        ]
    },
    "🏺 Древнегреческая Мифология": {
        "Common": [
            {"q": "Кто являлся верховным богом Олимпа?", "options": ["Зевс", "Посейдон", "Аид"], "a": "Зевс"},
            {"q": "Бог морей в древнегреческой мифологии:", "options": ["Посейдон", "Арес", "Гефест"], "a": "Посейдон"},
            {"q": "Герой, совершивший 12 подвигов:", "options": ["Геракл", "Персей", "Тесей"], "a": "Геракл"}
        ],
        "Rare": [
            {"q": "Богиня мудрости и справедливой войны:", "options": ["Афина", "Афродита", "Артемида"], "a": "Афина"},
            {"q": "Кто победил Минотавра в Лабиринте?", "options": ["Тесей", "Персей", "Ясон"], "a": "Тесей"},
            {"q": "Страж подземного царства Аида (трехглавый пес):", "options": ["Цербер", "Сфинкс", "Химера"], "a": "Цербер"}
        ],
        "Epic": [
            {"q": "Титанида, держащая небесный свод:", "options": ["Атлант", "Прометей", "Эпиметей"], "a": "Атлант"},
            {"q": "Кто передал огонь людям вопреки воле Зевса?", "options": ["Прометей", "Гефест", "Гермес"], "a": "Прометей"},
            {"q": "Перевозчик душ через реку Стикс:", "options": ["Харон", "Танатос", "Гермес"], "a": "Харон"}
        ],
        "Legendary": [
            {"q": "Имя матери Ахиллеса (нереиды):", "options": ["Фетида", "Амфитрита", "Галатея"], "a": "Фетида"},
            {"q": "Чудовище, превращавшее смотравших на нее в камень:", "options": ["Медуза Горгона", "Сцилла", "Ехидна"], "a": "Медуза Горгона"},
            {"q": "Кто был отцом Дедала?", "options": ["Евпалам", "Метион", "Эрехтей"], "a": "Евпалам"}
        ]
    },
    "🏛️ Латинский язык (Мертвый язык)": {
        "Common": [
            {"q": "Как переводится 'Veni, vidi, vici'?", "options": ["Пришел, увидел, победил", "Жизнь коротка", "Через тернии к звездам"], "a": "Пришел, увидел, победил"},
            {"q": "Перевод слова 'Aqua':", "options": ["Вода", "Земля", "Воздух"], "a": "Вода"},
            {"q": "Что значит 'Terra'?", "options": ["Земля", "Небо", "Огонь"], "a": "Земля"}
        ],
        "Rare": [
            {"q": "Перевод выражения 'Carpe diem':", "options": ["Лови момент", "Помни о смерти", "Знание — сила"], "a": "Лови момент"},
            {"q": "Значение фразы 'Cogito, ergo sum':", "options": ["Я мыслю, следовательно, я существую", "Век живи — век учись", "Свет во тьме"], "a": "Я мыслю, следовательно, я существую"},
            {"q": "Перевод слова 'Vita':", "options": ["Жизнь", "Смерть", "Судьба"], "a": "Жизнь"}
        ],
        "Epic": [
            {"q": "Перевод крылатого выражения 'Per aspera ad astra':", "options": ["Через тернии к звездам", "О времена, о нравы", "Суровый закон"], "a": "Через тернии к звездам"},
            {"q": "Что означает 'Alma mater'?", "options": ["Мать-кормилица (университет)", "Доброе сердце", "Древняя мудрость"], "a": "Мать-кормилица (университет)"},
            {"q": "Перевод выражения 'Homo homini lupus est':", "options": ["Человек человеку волк", "Человек разумный", "Друг познается в беде"], "a": "Человек человеку волк"}
        ],
        "Legendary": [
            {"q": "Значение выражения 'Memento mori':", "options": ["Помни о смерти", "Учись побеждать", "Любовь всё побеждает"], "a": "Помни о смерти"},
            {"q": "Перевод выражения 'Si vis pacem, para bellum':", "options": ["Хочешь мира — готовься к войне", "Мир во всем мире", "Победа или смерть"], "a": "Хочешь мира — готовься к войне"},
            {"q": "Что значит 'In vino veritas, in aqua sanitas'?", "options": ["Истина в вине, здоровье в воде", "Вино освежает ум", "Вода чистит душу"], "a": "Истина в вине, здоровье в воде"}
        ]
    },
    "📜 Философия и Логика": {
        "Common": [
            {"q": "Автор афоризма 'Я знаю, что ничего не знаю':", "options": ["Сократ", "Платон", "Аристотель"], "a": "Сократ"},
            {"q": "Формальное правило мышления с 2 посылками и 1 выводом:", "options": ["Силлогизм", "Аксиома", "Гипотеза"], "a": "Силлогизм"},
            {"q": "Философ, основавший Академию в Афинах:", "options": ["Платон", "Сократ", "Эпикур"], "a": "Платон"}
        ],
        "Rare": [
            {"q": "Направление, проповедующее стойкость к страданиям:", "options": ["Стоицизм", "Гедонизм", "Кинизм"], "a": "Стоицизм"},
            {"q": "Принцип 'Бритва Оккама' призывает:", "options": ["Не плодить сущности без необходимости", "Сомневаться во всем", "Искать первопричину"], "a": "Не плодить сущности без необходимости"},
            {"q": "Кто написал труд 'Поэтика' и 'Метафизика'?", "options": ["Аристотель", "Гераклит", "Демокрит"], "a": "Аристотель"}
        ],
        "Epic": [
            {"q": "Автор концепции 'Категорического императива':", "options": ["Иммануил Кант", "Фридрих Ницше", "Гегель"], "a": "Иммануил Кант"},
            {"q": "Философское учение, признающее материю первичной:", "options": ["Материализм", "Идеализм", "Дуализм"], "a": "Материализм"},
            {"q": "Кто написал произведение 'Так говорил Заратустра'?", "options": ["Фридрих Ницше", "Артур Шопенгауэр", "Мартин Хайдеггер"], "a": "Фридрих Ницше"}
        ],
        "Legendary": [
            {"q": "Что такое 'Апория' в философии (например, Зенона)?", "options": ["Трудноразрешимая логическая проблема", "Научный закон", "Вид доказательства"], "a": "Трудноразрешимая логическая проблема"},
            {"q": "Автор мыслительного эксперимента 'Кот Шрёдингера' в философии науки:", "options": ["Эрвин Шрёдингер", "Карл Поппер", "Томас Кун"], "a": "Эрвин Шрёдингер"},
            {"q": "Что обозначает понятие 'Вещь в себе' (Ding an sich) у Канта?", "options": ["Объект, независимый от нашего восприятия", "Внутренний мир человека", "Материальный предмет"], "a": "Объект, независимый от нашего восприятия"}
        ]
    },
    "⚛️ Квантовая Физика": {
        "Common": [
            {"q": "Минимальная неделимая порция энергии:", "options": ["Квант", "Атом", "Электрон"], "a": "Квант"},
            {"q": "Частица света называется:", "options": ["Фотон", "Протон", "Нейтрон"], "a": "Фотон"},
            {"q": "Заряд электрона:", "options": ["Отрицательный", "Положительный", "Нейтральный"], "a": "Отрицательный"}
        ],
        "Rare": [
            {"q": "Принцип неопределенности сформулировал:", "options": ["Гейзенберг", "Бор", "Эйнштейн"], "a": "Гейзенберг"},
            {"q": "Явление прохождения частицы через потенциальный барьер:", "options": ["Туннельный эффект", "Дифракция", "Интерференция"], "a": "Туннельный эффект"},
            {"q": "Уравнение, описывающее изменение квантового состояния:", "options": ["Уравнение Шрёдингера", "Уравнение Максвелла", "Закон Ньютона"], "a": "Уравнение Шрёдингера"}
        ],
        "Epic": [
            {"q": "Свойство квантовых систем находиться в нескольких состояниях одновременно:", "options": ["Суперпозиция", "Запутаность", "Когерентность"], "a": "Суперпозиция"},
            {"q": "Парадокс квантовой связи на расстоянии (EPR):", "options": ["Квантовая запутанность", "Теорема Белла", "Декогеренция"], "a": "Квантовая запутанность"},
            {"q": "Гипотеза де Бройля утверждает, что:", "options": ["Материя обладает корпускулярно-волновым дуализмом", "Свет — только волна", "Атом неделим"], "a": "Материя обладает корпускулярно-волновым дуализмом"}
        ],
        "Legendary": [
            {"q": "Неравенства Белла позволяют проверить:", "options": ["Наличие скрытых параметров", "Массу фотона", "Скорость расширения Вселенной"], "a": "Наличие скрытых параметров"},
            {"q": "Какая константа связывает энергию фотона с его частотой?", "options": ["Постоянная Планка", "Постоянная Авогадро", "Постоянная Больцмана"], "a": "Постоянная Планка"},
            {"q": "Что утверждает теорема о запрете клонирования?", "options": ["Нельзя создать точную копию неизвестного квантового состояния", "Нельзя копировать ДНК", "Запрещено дублирование фотонов"], "a": "Нельзя создать точную копию неизвестного квантового состояния"}
        ]
    },
    "🛸 Клингонский язык (Вымышленный)": {
        "Common": [
            {"q": "Из какой вселенной взяты клингоны?", "options": ["Star Trek", "Star Wars", "Babylon 5"], "a": "Star Trek"},
            {"q": "Боевой клич / Приветствие клингонов ('nuqneH'):", "options": ["Чего тебе?", "Привет!", "Мир вам"], "a": "Чего тебе?"},
            {"q": "Создатель клингонского языка:", "options": ["Марк Окранд", "Дж. Р. Р. Толкин", "Джордж Лукас"], "a": "Марк Окранд"}
        ],
        "Rare": [
            {"q": "Как на клингонском будет 'Успех / Победа'?", "options": ["Qapla'", "Maj", "pItlh"], "a": "Qapla'"},
            {"q": "Традиционный оружие клингонского воина:", "options": ["Бат'лет (Bat'leth)", "Бластер", "Световой меч"], "a": "Бат'лет (Bat'leth)"},
            {"q": "Родная планета клингонов:", "options": ["Qo'noS", "Vulcan", "Romulus"], "a": "Qo'noS"}
        ],
        "Epic": [
            {"q": "Как сказать 'Сегодня хороший день, чтобы умереть'?", "options": ["Heghlu'meH QaQ jajvam", "Qapla' batlh", "nuqneH jaj"], "a": "Heghlu'meH QaQ jajvam"},
            {"q": "Какой порядок слов используется в клингонском?", "options": ["OVS (Объект-Глагол-Субъект)", "SVO", "SOV"], "a": "OVS (Объект-Глагол-Субъект)"},
            {"q": "Что означает клингонское слово 'tlhIngan'?", "options": ["Клингон", "Воин", "Человек"], "a": "Клингон"}
        ],
        "Legendary": [
            {"q": "Шекспировский перевод на клингонский с фразой 'To be or not to be':", "options": ["taH pagh taHbe'", "Hegh pagh yIn", "Qapla' pagh Qapla'be'"], "a": "taH pagh taHbe'"},
            {"q": "Какое слово обозначает согласие и завершение речи ('Готово')?", "options": ["pItlh", "Maj", "lu'"], "a": "pItlh"},
            {"q": "Как пишется название клингонского алфавита?", "options": ["pIqaD", "KlingonScript", "tLHinganA"], "a": "pIqaD"}
        ]
    },
    "💀 Dark Souls Математика": {
        "Common": [
            {"q": "Какое базовое число душ дает 'Soul of a Lost Undead'?", "options": ["200", "500", "1000"], "a": "200"},
            {"q": "Максимальный уровень заточки обычного оружия в Dark Souls 1:", "options": ["+15", "+10", "+5"], "a": "+15"},
            {"q": "Сколько фляг Эстуса по умолчанию дает зажженный костер?", "options": ["10", "5", "15"], "a": "10"}
        ],
        "Rare": [
            {"q": "Процент веса снаряжения для быстрых перекатов (Fast Roll) в DS1:", "options": ["< 25%", "< 50%", "< 70%"], "a": "< 25%"},
            {"q": "Сколько душ требуется для первого уровня персонажа?", "options": ["Зависит от начального класса", "673", "1000"], "a": "Зависит от начального класса"},
            {"q": "Каков мягкий кап (Soft Cap) для Живучести (Vitality) в DS3?", "options": ["27 / 40", "30 / 50", "50 / 99"], "a": "27 / 40"}
        ],
        "Epic": [
            {"q": "Формула расчета физического урона при критическом ударе (Рипост) учитывает:", "options": ["Modifier оружия и показатель Рипоста", "Только силу персонажа", "Уровень костра"], "a": "Modifier оружия и показатель Рипоста"},
            {"q": "Сколько титанитовых локаций/кусков нужно для прокачки оружия с +0 до +15?", "options": ["9 осколков, 9 больших, 8 обломков, 1 кусок", "10 осколков, 5 кусков", "12 осколков, 6 обломков"], "a": "9 осколков, 9 больших, 8 обломков, 1 кусок"},
            {"q": "Какой штраф к устойчивости (Poise) дает тяжелый урон в DS1?", "options": ["Уменьшение до 0 при сбитии", "Потеря 50%", "Фиксированный урон -10"], "a": "Уменьшение до 0 при сбитии"}
        ],
        "Legendary": [
            {"q": "Чему равен коэффициент урона скалирования категории 'S' при 40 силе?", "options": ["100% - 140% от базового урона", "200%", "50%"], "a": "100% - 140% от базового урона"},
            {"q": "Шанс выпадения предметов при 410 Human/Item Discovery:", "options": ["Увеличивает базовый шанс в ~4.1 раза", "100% гарантированный лут", "Фиксированные +41%"], "a": "Увеличивает базовый шанс в ~4.1 раза"},
            {"q": "Сколько душ суммарно нужно для достижения 802 уровня в Dark Souls 3?", "options": ["~2.6 миллиарда", "100 миллионов", "500 тысяч"], "a": "~2.6 миллиарда"}
        ]
    }
}

# Внедрение секретного вопроса во все категории (в Legendary)
for cat_name in QUESTIONS:
    if "Legendary" in QUESTIONS[cat_name]:
        QUESTIONS[cat_name]["Legendary"].append(SECRET_QUESTION)

WORK_QUESTIONS = [
    {"q": "Сколько будет 12 + 15?", "options": ["27", "25", "29"], "a": "27"},
    {"q": "Столица Франции?", "options": ["Париж", "Лондон", "Берлин"], "a": "Париж"},
    {"q": "Какая планета 3-я от Солнца?", "options": ["Земля", "Марс", "Венера"], "a": "Земля"},
    {"q": "Сколько дней в невисокосном году?", "options": ["365", "366", "360"], "a": "365"},
    {"q": "Какой элемент имеет символ 'O'?", "options": ["Кислород", "Золото", "Железо"], "a": "Кислород"},
    SECRET_QUESTION
]

current_mult = 1.0 + (st.session_state.multiplier_level - 1) * 0.25
mult_upgrade_cost = int(100 * (1.5 ** (st.session_state.multiplier_level - 1)))

# --- ВЫЧИСЛЕНИЕ И ПРОВЕРКА АЧИВОК ---
if st.session_state.cases_opened >= 5:
    st.session_state.achievements["case_master"] = True
if st.session_state.cases_opened >= 25:
    st.session_state.achievements["case_addict"] = True
if st.session_state.coins >= 500:
    st.session_state.achievements["high_roller"] = True
if st.session_state.coins >= 1500:
    st.session_state.achievements["millionaire"] = True
if len(st.session_state.unlocked_cats) >= 6:
    st.session_state.achievements["scholar"] = True
if len(st.session_state.unlocked_cats) >= 12:
    st.session_state.achievements["polymath"] = True
if st.session_state.roulette_spins >= 10:
    st.session_state.achievements["roulette_fan"] = True
if st.session_state.correct_answers >= 10:
    st.session_state.achievements["smart_mind"] = True
if st.session_state.work_completed >= 5:
    st.session_state.achievements["workaholic"] = True

unlocked_count = sum(1 for v in st.session_state.achievements.values() if v)

# --- БОКОВАЯ ПАНЕЛЬ ---
st.sidebar.title("🏆 Штаб Достижений")
st.sidebar.metric("Баланс монет", f"🪙 {st.session_state.coins}")
st.sidebar.metric("Очки опыта", f"⭐ {st.session_state.score}")
st.sidebar.metric("Ачивок открыто", f"🎖️ {unlocked_count} / {len(ACHIEVEMENTS_LIST)}")

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Визуальная Тема")
st.session_state.theme_name = st.sidebar.selectbox(
    "Выберите тему оформления:",
    list(ACHIEVEMENT_THEMES.keys()),
    index=list(ACHIEVEMENT_THEMES.keys()).index(st.session_state.theme_name)
)

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Улучшения")

if st.sidebar.button(f"📈 Квалификация (+0.25x)\nЦена: {mult_upgrade_cost} 🪙", use_container_width=True):
    if st.session_state.coins >= mult_upgrade_cost:
        st.session_state.coins -= mult_upgrade_cost
        st.session_state.multiplier_level += 1
        st.sidebar.success("Уровень повышен!")
    else:
        st.sidebar.error("Не хватает монет!")

if not st.session_state.insurance_unlocked:
    if st.sidebar.button("🛡️ Страховка (150 🪙)", use_container_width=True):
        if st.session_state.coins >= 150:
            st.session_state.coins -= 150
            st.session_state.insurance_unlocked = True
            st.sidebar.success("Страховка куплена!")
        else:
            st.sidebar.error("Не хватает монет!")
else:
    st.sidebar.caption("✅ Страховка активна")

st.sidebar.markdown("---")
st.sidebar.subheader("💎 Магазин Редких Дисциплин")

shop_cats = {
    "🇩🇪 Немецкий язык": 80, "🇫🇷 Французский язык": 100, "📐 Алгебра и Геометрия": 120,
    "⚡ Классическая Физика": 150, "💻 Программирование Python": 180, "🇯🇵 Японский язык (Иероглифы)": 250,
    "🏺 Древнегреческая Мифология": 300, "🏛️ Латинский язык (Мертвый язык)": 400, "📜 Философия и Логика": 500,
    "⚛️ Квантовая Физика": 700, "🛸 Клингонский язык (Вымышленный)": 900, "💀 Dark Souls Математика": 1200
}

for cat_name, price in shop_cats.items():
    if cat_name not in st.session_state.unlocked_cats:
        if st.sidebar.button(f"🔓 {cat_name} ({price} 🪙)", use_container_width=True):
            if st.session_state.coins >= price:
                st.session_state.coins -= price
                st.session_state.unlocked_cats.append(cat_name)
                st.sidebar.success("Разблокировано!")
            else:
                st.sidebar.error("Не хватает монет!")

# --- ГЛАВНЫЙ ИНТЕРФЕЙС И ВКЛАДКИ ---
st.title("🎰 EduCasino: Ultimate Edition")

main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
    "📦 Кейсы с Вопросами", 
    "🎡 Классическая Рулетка (Red/Black)", 
    "💼 Подработка",
    "🏆 Достижения и Статистика"
])

# ==========================================
# ВКЛАДКА 1: КЕЙСЫ С ВОПРОСАМИ (CS:GO STYLE)
# ==========================================
with main_tab1:
    # Сортировка списка купленных дисциплин по возрастанию стоимости открытия кейса
    sorted_unlocked_cats = sorted(
        st.session_state.unlocked_cats,
        key=lambda c: CATEGORY_SETTINGS.get(c, {"cost": 20})["cost"]
    )
    
    selected_cat = st.selectbox("Выберите дисциплину (отсортировано по цене):", sorted_unlocked_cats)
    
    cat_cfg = CATEGORY_SETTINGS.get(selected_cat, {"cost": 20, "reward_mult": 1.5, "pop": "🌟 Стандартный выбор"})

    st.markdown(f"""
    <div style="background-color: {active_theme['card']}; padding: 12px 16px; border-radius: 10px; border-left: 5px solid {active_theme['accent']}; margin-bottom: 15px;">
        <b>Категория:</b> {cat_cfg['pop']}<br>
        <b>Стоимость открытия кейса:</b> {cat_cfg['cost']} 🪙 | <b>Множитель темы:</b> x{cat_cfg['reward_mult']}
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"🎁 Открыть Кейс ({cat_cfg['cost']} 🪙)", use_container_width=True):
        if st.session_state.coins < cat_cfg['cost']:
            st.error(f"Недостаточно монет! Потребуется {cat_cfg['cost']} 🪙")
        else:
            st.session_state.coins -= cat_cfg['cost']
            st.session_state.cases_opened += 1
            
            sub_q_db = QUESTIONS.get(selected_cat, QUESTIONS["🇬🇧 Английский язык (Популярно)"])
            avail_r = list(sub_q_db.keys())
            w_list = [RARITY[r]["weight"] for r in avail_r]
            win_rarity = random.choices(avail_r, weights=w_list, k=1)[0]
            chosen_q = random.choice(sub_q_db[win_rarity])
            
            case_items = [random.choices(avail_r, weights=w_list, k=1)[0] for _ in range(24)]
            case_items.append(win_rarity)
            case_items.extend([random.choices(avail_r, weights=w_list, k=1)[0] for _ in range(5)])

            case_slot = st.empty()
            total_steps = 23
            
            for step in range(total_steps):
                visible_5 = case_items[step : step + 5]
                
                cards_html = ""
                for i, item_key in enumerate(visible_5):
                    r_item = RARITY[item_key]
                    is_center = (i == 2)
                    border_style = f"3px solid {r_item['color']}" if not is_center else f"4px solid #ffffff"
                    glow = f"box-shadow: 0 0 15px {r_item['color']};" if is_center else ""
                    
                    cards_html += f"""
                    <div class="case-card" style="background: {r_item['color']}; border: {border_style}; {glow}">
                        <div style="font-size: 22px;">📦</div>
                        <div style="font-size: 11px; text-align: center;">{r_item['name']}</div>
                    </div>
                    """
                
                case_slot.markdown(
                    f"""
                    <div class="case-container">
                        <div class="pointer"></div>
                        {cards_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                delay = 0.04 + (step / total_steps) ** 2 * 0.25
                time.sleep(delay)

            st.session_state.current_rarity = win_rarity
            st.session_state.current_q = chosen_q
            st.session_state.current_options = random.sample(chosen_q["options"], len(chosen_q["options"]))

    # Отображение вопроса
    if st.session_state.current_q:
        r_key = st.session_state.current_rarity
        q_data = st.session_state.current_q
        r_info = RARITY[r_key]
        calc_reward = int(r_info["base_coins"] * current_mult * cat_cfg["reward_mult"])

        st.markdown(
            f"""
            <div style="background-color: {active_theme['card']}; padding: 18px; border-radius: 12px; border: 2px solid {r_info['color']}; margin-top: 15px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: {r_info['color']}; margin: 0;">Вам выпало: {r_info['name']}</h3>
                    <span style="background: {r_info['color']}; color: #ffffff; padding: 4px 12px; border-radius: 15px; font-weight: bold;">
                        Награда: +{calc_reward} 🪙
                    </span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

        st.subheader(q_data["q"])

        with st.form("quiz_form"):
            choice = st.radio("Выберите ответ:", st.session_state.current_options)
            submitted = st.form_submit_button("Ответить", use_container_width=True)
            
            if submitted:
                if choice == q_data["a"]:
                    st.balloons()
                    st.success(f"🎉 Верно! Вы выиграли +{calc_reward} монет!")
                    st.session_state.coins += calc_reward
                    st.session_state.score += calc_reward
                    st.session_state.correct_answers += 1
                    st.session_state.achievements["first_win"] = True
                else:
                    if st.session_state.insurance_unlocked:
                        refund = int(cat_cfg['cost'] * 0.5)
                        st.session_state.coins += refund
                        st.error(f"❌ Неверно! Страховка вернула вам +{refund} 🪙")
                    else:
                        st.error(f"❌ Неверно! Правильный ответ был: **{q_data['a']}**")
                
                st.session_state.current_q = None
                st.session_state.current_rarity = None
                st.session_state.current_options = None

# ==========================================
# ВКЛАДКА 2: КЛАССИЧЕСКАЯ РУЛЕТКА (RED/BLACK)
# ==========================================
with main_tab2:
    st.subheader("🎡 Казино Рулетка (Красное / Черное / Зеленое)")
    st.caption("Красное: x2 | Черное: x2 | Зеленое (Зеро): x14")

    ROULETTE_NUMBERS = [
        {"num": 0, "color": "green", "bg": "#16a34a"},
        {"num": 1, "color": "red", "bg": "#dc2626"},
        {"num": 2, "color": "black", "bg": "#1e293b"},
        {"num": 3, "color": "red", "bg": "#dc2626"},
        {"num": 4, "color": "black", "bg": "#1e293b"},
        {"num": 5, "color": "red", "bg": "#dc2626"},
        {"num": 6, "color": "black", "bg": "#1e293b"},
        {"num": 7, "color": "red", "bg": "#dc2626"},
        {"num": 8, "color": "black", "bg": "#1e293b"},
        {"num": 9, "color": "red", "bg": "#dc2626"},
        {"num": 10, "color": "black", "bg": "#1e293b"},
        {"num": 11, "color": "black", "bg": "#1e293b"},
        {"num": 12, "color": "red", "bg": "#dc2626"},
        {"num": 13, "color": "black", "bg": "#1e293b"},
        {"num": 14, "color": "red", "bg": "#dc2626"}
    ]

    col_bet_amt, col_bet_type = st.columns([1, 1])
    with col_bet_amt:
        bet_amount = st.number_input("Размер ставки (🪙):", min_value=5, max_value=max(5, st.session_state.coins), value=min(20, max(5, st.session_state.coins)), step=5)
    with col_bet_type:
        bet_choice = st.radio("Ставка на:", ["🔴 Красное (x2)", "⚫ Черное (x2)", "🟢 Зеленое 0 (x14)"], horizontal=True)

    if st.button("🚀 Крутить Рулетку!", use_container_width=True):
        if st.session_state.coins < bet_amount:
            st.error("Недостаточно монет для такой ставки!")
        else:
            st.session_state.coins -= bet_amount
            st.session_state.roulette_spins += 1
            
            winning_sector = random.choice(ROULETTE_NUMBERS)
            
            roulette_strip = [random.choice(ROULETTE_NUMBERS) for _ in range(24)]
            roulette_strip.append(winning_sector)
            roulette_strip.extend([random.choice(ROULETTE_NUMBERS) for _ in range(5)])

            roulette_slot = st.empty()
            total_r_steps = 23

            for step in range(total_r_steps):
                visible_5 = roulette_strip[step : step + 5]
                
                cards_html = ""
                for i, sec in enumerate(visible_5):
                    is_center = (i == 2)
                    border = "4px solid #ffffff" if is_center else "2px solid rgba(255,255,255,0.2)"
                    glow = "box-shadow: 0 0 20px #ffffff;" if is_center else ""
                    
                    cards_html += f"""
                    <div class="case-card" style="background: {sec['bg']}; border: {border}; {glow} font-size: 28px;">
                        {sec['num']}
                    </div>
                    """

                roulette_slot.markdown(
                    f"""
                    <div class="case-container">
                        <div class="pointer"></div>
                        {cards_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                delay = 0.03 + (step / total_r_steps) ** 2 * 0.3
                time.sleep(delay)

            win_color = winning_sector["color"]
            multiplier = 0
            
            if "Красное" in bet_choice and win_color == "red":
                multiplier = 2
            elif "Черное" in bet_choice and win_color == "black":
                multiplier = 2
            elif "Зеленое" in bet_choice and win_color == "green":
                multiplier = 14

            if multiplier > 0:
                payout = bet_amount * multiplier
                st.session_state.coins += payout
                st.session_state.score += payout
                st.balloons()
                st.success(f"🎉 ВЫИГРЫШ! Выпало {winning_sector['num']} ({win_color.upper()}). Вы получили +{payout} 🪙!")
            else:
                st.error(f"❌ Проигрыш! Выпало {winning_sector['num']} ({win_color.upper()}). Попробуйте еще раз!")

# ==========================================
# ВКЛАДКА 3: ПОДРАБОТКА (С КУЛДАУНОМ)
# ==========================================
with main_tab3:
    st.subheader("💼 Быстрый заработок монет")
    WORK_COOLDOWN_SECONDS = 60  # Время кулдауна на подработку в секундах

    time_since_last_work = time.time() - st.session_state.last_work_time
    time_remaining = int(WORK_COOLDOWN_SECONDS - time_since_last_work)

    if time_remaining > 0:
        st.warning(f"⏳ Вы переутомились! Следующая подработка будет доступна через **{time_remaining}** сек.")
    else:
        st.caption("Подработка готова к выполнению!")

    tab_quiz, tab_ad = st.tabs(["🧩 Быстрый опрос (+15 🪙)", "📺 Просмотр спонсора (+10 🪙)"])
    
    with tab_quiz:
        if not st.session_state.work_q:
            q_selected = random.choice(WORK_QUESTIONS)
            st.session_state.work_q = q_selected
            st.session_state.work_options = random.sample(q_selected["options"], len(q_selected["options"]))
            
        wq = st.session_state.work_q
        st.write(f"**Вопрос:** {wq['q']}")
        
        with st.form("work_form"):
            w_choice = st.radio("Вариант ответа:", st.session_state.work_options)
            w_sub = st.form_submit_button("Ответить и заработать 15 монет", disabled=(time_remaining > 0))
            
            if w_sub:
                if time_remaining <= 0:
                    st.session_state.last_work_time = time.time()
                    if w_choice == wq["a"]:
                        st.session_state.coins += 15
                        st.session_state.work_completed += 1
                        st.success("🎉 Верно! Вы заработали +15 монет!")
                    else:
                        st.error("❌ Неверно, попробуйте еще раз!")
                    st.session_state.work_q = None
                    st.session_state.work_options = None
                    st.rerun()

    with tab_ad:
        st.write("Посмотрите короткий спонсорский ролик, чтобы получить +10 монет.")
        if st.button("▶ Посмотреть ролик (3 сек)", disabled=(time_remaining > 0)):
            if time_remaining <= 0:
                with st.spinner("Смотрим ролик..."):
                    time.sleep(3)
                st.session_state.last_work_time = time.time()
                st.session_state.coins += 10
                st.session_state.work_completed += 1
                st.success("💰 Вам начислено +10 монет!")
                st.rerun()

# ==========================================
# ВКЛАДКА 4: ДОСТИЖЕНИЯ И СТАТИСТИКА
# ==========================================
with main_tab4:
    st.subheader("🏆 Достижения и Игровая Статистика")

    # Секция ежедневной награды
    st.markdown("### 🎁 Ежедневная Награда")
    today_str = datetime.now().strftime("%Y-%m-%d")
    if st.session_state.last_daily_claim != today_str:
        if st.button("🎉 Забрать Ежедневный Бонус (+50 🪙)", use_container_width=True):
            st.session_state.coins += 50
            st.session_state.last_daily_claim = today_str
            st.balloons()
            st.success("Вы успешно забрали +50 монет!")
    else:
        st.info("✅ Вы уже забрали свой бонус сегодня. Возвращайтесь завтра!")

    st.markdown("---")
    st.markdown("### 📊 Статистика Игрока")
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.write(f"• **Всего открыто кейсов:** {st.session_state.cases_opened}")
        st.write(f"• **Правильных ответов:** {st.session_state.correct_answers}")
        st.write(f"• **Спинов в рулетке:** {st.session_state.roulette_spins}")
    with col_stat2:
        st.write(f"• **Выполнено подработок:** {st.session_state.work_completed}")
        st.write(f"• **Разблокировано дисциплин:** {len(st.session_state.unlocked_cats)} / {len(CATEGORY_SETTINGS)}")
        st.write(f"• **Ачивок получено:** {unlocked_count} / {len(ACHIEVEMENTS_LIST)}")

    st.markdown("---")
    st.markdown("### 🎖️ Доска Ачивок (Забирайте награды за выполнение)")

    # Отображение всех 10 ачивок с кнопками забора монет
    ach_keys = list(ACHIEVEMENTS_LIST.keys())
    for i in range(0, len(ach_keys), 2):
        col_a, col_b = st.columns(2)
        
        # Левая колонка
        key1 = ach_keys[i]
        info1 = ACHIEVEMENTS_LIST[key1]
        is_unlocked1 = st.session_state.achievements[key1]
        is_claimed1 = st.session_state.claimed_achievements[key1]
        
        with col_a:
            st.markdown(f"**{info1['title']}**")
            st.caption(f"{info1['desc']} | Награда: +{info1['reward']} 🪙")
            if is_claimed1:
                st.success("✅ Получено")
            elif is_unlocked1:
                if st.button(f"🎁 Забрать +{info1['reward']} 🪙", key=f"btn_{key1}"):
                    st.session_state.coins += info1['reward']
                    st.session_state.claimed_achievements[key1] = True
                    st.balloons()
                    st.rerun()
            else:
                st.info("🔒 Заблокировано")
        
        # Правая колонка
        if i + 1 < len(ach_keys):
            key2 = ach_keys[i + 1]
            info2 = ACHIEVEMENTS_LIST[key2]
            is_unlocked2 = st.session_state.achievements[key2]
            is_claimed2 = st.session_state.claimed_achievements[key2]
            
            with col_b:
                st.markdown(f"**{info2['title']}**")
                st.caption(f"{info2['desc']} | Награда: +{info2['reward']} 🪙")
                if is_claimed2:
                    st.success("✅ Получено")
                elif is_unlocked2:
                    if st.button(f"🎁 Забрать +{info2['reward']} 🪙", key=f"btn_{key2}"):
                        st.session_state.coins += info2['reward']
                        st.session_state.claimed_achievements[key2] = True
                        st.balloons()
                        st.rerun()
                else:
                    st.info("🔒 Заблокировано")
