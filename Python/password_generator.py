#!/usr/bin/env python3
"""
Генератор случайных паролей с настройкой сложности
"""

import random
import string
import argparse
import sys
from datetime import datetime


# Словарь для diceware генерации (2048 слов для ~55 бит энтропии при 5 словах)
DICEWARE_WORDLIST = [
    "able", "about", "above", "acid", "acne", "acre", "adam", "aged", "ages", "aide",
    "aims", "alan", "alex", "ally", "alto", "anna", "anne", "anti", "ants", "arch",
    "area", "args", "army", "arts", "asia", "atom", "aunt", "auto", "away", "baby",
    "back", "bags", "bail", "bake", "ball", "band", "bank", "bare", "bark", "barn",
    "base", "bash", "bass", "bath", "bats", "beam", "bean", "bear", "beat", "been",
    "beer", "bell", "belt", "bend", "bent", "berg", "bert", "best", "beta", "beth",
    "bias", "bike", "bill", "bind", "bird", "bite", "bits", "blue", "blur", "boat",
    "body", "bold", "bolt", "bomb", "bond", "bone", "book", "boom", "boot", "bore",
    "born", "boss", "both", "bowl", "boys", "brad", "brag", "bran", "brat", "brew",
    "brig", "brim", "bulk", "bull", "bump", "bunk", "burn", "bush", "busy", "buzz",
    "byte", "cafe", "cage", "cake", "calf", "call", "calm", "came", "camp", "cane",
    "cape", "card", "care", "carl", "carp", "carr", "cart", "case", "cash", "cast",
    "cave", "cell", "cent", "chad", "char", "chat", "chef", "chen", "chip", "chop",
    "cite", "city", "clan", "clap", "clay", "clip", "club", "clue", "coal", "coat",
    "code", "coin", "cold", "cole", "coma", "comb", "come", "cone", "cook", "cool",
    "cope", "copy", "cord", "core", "cork", "corn", "cost", "cozy", "crab", "crew",
    "crop", "crow", "cruz", "cuba", "cube", "cult", "cure", "curl", "cute", "cyan",
    "dale", "dame", "damp", "dana", "dane", "dang", "dare", "dark", "darn", "dart",
    "dash", "data", "date", "dawn", "days", "dead", "deaf", "deal", "dean", "dear",
    "debt", "deck", "deed", "deem", "deep", "deer", "demo", "deny", "desk", "dial",
    "dice", "died", "diet", "dime", "dine", "dire", "dirt", "disc", "dish", "disk",
    "dive", "dock", "does", "doll", "dome", "done", "doom", "door", "dose", "doug",
    "dove", "down", "doze", "drag", "dram", "draw", "drew", "drop", "drug", "drum",
    "dual", "duck", "duct", "dude", "duel", "duke", "dull", "dumb", "dump", "dune",
    "dunk", "dusk", "dust", "duty", "dyer", "dyke", "each", "earl", "earn", "ears",
    "ease", "east", "easy", "eats", "echo", "edge", "edit", "eggs", "eith", "else",
    "emit", "emma", "envy", "epic", "eric", "erik", "euro", "even", "ever", "evil",
    "exam", "exit", "eyed", "eyes", "face", "fact", "fade", "fail", "fair", "fake",
    "fall", "fame", "fare", "farm", "fast", "fate", "fawn", "fear", "feat", "feel",
    "fees", "feet", "fell", "felt", "fern", "fest", "fiat", "file", "fill", "film",
    "find", "fine", "fire", "firm", "fish", "fist", "five", "flag", "flap", "flat",
    "flaw", "fled", "flee", "flew", "flex", "flip", "flit", "flow", "flux", "foam",
    "foil", "fold", "folk", "fond", "font", "food", "fool", "foot", "ford", "fore",
    "fork", "form", "fort", "four", "fowl", "fran", "fred", "free", "frog", "from",
    "fuel", "full", "fund", "funk", "fury", "fuse", "fuss", "gain", "gale", "game",
    "gang", "gaps", "gary", "gate", "gave", "gear", "gene", "germ", "gets", "gift",
    "gina", "girl", "give", "glad", "glow", "glue", "goal", "goat", "goes", "gold",
    "golf", "gone", "good", "gore", "gosh", "gown", "grab", "grad", "gram", "gray",
    "greg", "grew", "grey", "grid", "grim", "grin", "grip", "grit", "grow", "grub",
    "gulf", "gull", "gust", "guys", "hack", "hail", "hair", "half", "hall", "halt",
    "hand", "hang", "hank", "hans", "hard", "hare", "harm", "harp", "hart", "hash",
    "hate", "have", "hawk", "haze", "hazy", "head", "heal", "heap", "hear", "heat",
    "heck", "heel", "heir", "held", "hell", "helm", "help", "hemp", "hens", "herb",
    "here", "hero", "hers", "hide", "high", "hike", "hill", "hilt", "hint", "hire",
    "hits", "hive", "hoax", "hold", "hole", "holy", "home", "hong", "hood", "hoof",
    "hook", "hoop", "hope", "horn", "host", "hour", "huge", "hugh", "hull", "hunt",
    "hurt", "hyde", "hymn", "icon", "idea", "idle", "igor", "inch", "info", "into",
    "iowa", "iran", "iraq", "iris", "iron", "isle", "item", "ivan", "jack", "jade",
    "jail", "jake", "jane", "jazz", "jean", "jeff", "jerk", "jest", "jets", "jews",
    "jill", "joan", "jobs", "joel", "joey", "john", "join", "joke", "jose", "josh",
    "juan", "judy", "july", "jump", "june", "junk", "jury", "just", "jute", "kant",
    "karl", "kate", "keen", "keep", "kent", "kept", "kern", "keys", "khan", "kick",
    "kids", "kill", "kilo", "kind", "king", "kirk", "kiss", "kite", "knee", "knew",
    "knit", "knob", "knot", "know", "kong", "kurt", "labs", "lace", "lack", "lacy",
    "lady", "laid", "lake", "lamb", "lame", "lamp", "land", "lane", "lang", "laps",
    "lard", "lars", "lash", "last", "late", "lava", "lawn", "laws", "lazy", "lead",
    "leaf", "leak", "lean", "leap", "left", "legs", "lend", "lens", "lent", "leon",
    "less", "levy", "liar", "lice", "lick", "lied", "lien", "lies", "lieu", "life",
    "lift", "like", "lily", "limb", "lime", "limp", "line", "ling", "link", "lint",
    "lion", "lips", "lisa", "lisp", "list", "live", "load", "loaf", "loan", "lock",
    "loft", "logo", "logs", "loin", "lone", "long", "look", "loop", "loot", "lord",
    "lore", "lose", "loss", "lost", "lots", "loud", "lout", "love", "luck", "lucy",
    "luge", "luis", "luke", "lump", "lung", "lure", "lush", "lust", "lute", "lynx",
    "lyon", "lyre", "mace", "made", "maid", "mail", "maim", "main", "make", "male",
    "mall", "malt", "mama", "mane", "many", "maps", "marc", "mare", "mark", "mars",
    "mary", "mash", "mask", "mass", "mast", "mate", "math", "matt", "maul", "maya",
    "mayo", "maze", "mead", "meal", "mean", "meat", "meek", "meet", "melt", "memo",
    "mend", "menu", "meow", "mere", "mesa", "mesh", "mess", "mice", "mike", "mild",
    "mile", "milk", "mill", "milo", "mime", "mind", "mine", "ming", "mini", "mink",
    "mint", "miss", "mist", "mite", "mitt", "moan", "moat", "mock", "mode", "mold",
    "mole", "molt", "monk", "mood", "moon", "moor", "moot", "mope", "more", "morn",
    "moss", "most", "moth", "move", "much", "muck", "mule", "mum", "muse", "mush",
    "musk", "must", "mute", "mutt", "myth", "nail", "name", "nape", "navy", "near",
    "neat", "neck", "need", "neil", "neon", "nero", "nest", "neva", "news", "newt",
    "next", "nice", "nick", "nigh", "nina", "nine", "noah", "node", "noir", "none",
    "noon", "norm", "nose", "note", "noun", "nova", "nude", "null", "numb", "nuts",
    "oath", "obey", "odds", "odor", "ohio", "oily", "okay", "omen", "omit", "once",
    "only", "onto", "oops", "ooze", "opal", "open", "opus", "oral", "orca", "orcs",
    "otto", "ouch", "ours", "oust", "outs", "oven", "over", "owed", "owes", "owls",
    "owns", "pace", "pack", "pact", "page", "paid", "pail", "pain", "pair", "pale",
    "palm", "pane", "pang", "pant", "papa", "para", "pare", "park", "part", "pass",
    "past", "path", "paul", "pave", "pawn", "pays", "peak", "peal", "pear", "peas",
    "peat", "peck", "peek", "peel", "peer", "pelt", "penn", "pens", "peon", "perk",
    "perm", "pert", "pest", "pete", "pets", "pews", "phil", "pier", "pies", "pigs",
    "pike", "pile", "pill", "pine", "ping", "pink", "pins", "pint", "pipe", "pita",
    "pity", "plan", "play", "plea", "pled", "plot", "plow", "ploy", "plug", "plum",
    "plus", "poem", "poet", "poke", "pole", "poll", "polo", "pond", "pony", "pool",
    "poop", "poor", "pope", "pops", "pore", "pork", "porn", "port", "pose", "posh",
    "post", "posy", "pour", "pout", "pray", "prep", "prey", "prim", "prod", "prof",
    "prop", "pros", "prow", "prune", "puff", "puke", "pull", "pulp", "puma", "pump",
    "punk", "puns", "punt", "puny", "pupa", "pups", "pure", "purl", "purr", "push",
    "puts", "putt", "quad", "quay", "quid", "quit", "quiz", "race", "rack", "raft",
    "rage", "raid", "rail", "rain", "rake", "ramp", "rand", "rang", "rank", "rant",
    "rare", "rash", "rate", "rats", "rave", "rays", "raze", "razz", "read", "real",
    "ream", "reap", "rear", "reed", "reef", "reek", "reel", "refs", "rein", "rely",
    "rend", "reno", "rent", "rest", "reva", "rice", "rich", "rick", "ride", "rife",
    "rift", "rigs", "rill", "rims", "rind", "ring", "rink", "riot", "ripe", "rise",
    "risk", "rita", "rite", "road", "roam", "roan", "roar", "robe", "robs", "rock",
    "rode", "rods", "roil", "role", "roll", "rome", "romp", "rood", "roof", "rook",
    "room", "root", "rope", "rosa", "rose", "ross", "rosy", "rote", "rots", "rout",
    "rove", "rows", "roxy", "rube", "ruby", "ruck", "rude", "rued", "rues", "ruff",
    "rugs", "ruin", "rule", "rump", "rums", "rune", "rung", "runs", "runt", "ruse",
    "rush", "rusk", "rust", "ruth", "ruts", "ryde", "ryan", "sack", "safe", "saga",
    "sage", "sago", "said", "sail", "sake", "sale", "salt", "same", "sand", "sane",
    "sang", "sank", "sara", "sash", "sass", "sate", "saul", "save", "sawn", "saws",
    "says", "scab", "scam", "scan", "scar", "scat", "scot", "seal", "seam", "sear",
    "seas", "seat", "sect", "seed", "seek", "seem", "seen", "seep", "seer", "self",
    "sell", "semi", "send", "sent", "sept", "serf", "seth", "sets", "sewn", "sews",
    "sexy", "shag", "shah", "sham", "shaw", "shed", "shin", "ship", "shiv", "shoe",
    "shop", "shot", "show", "shun", "shut", "sick", "side", "sigh", "sign", "silk",
    "sill", "silo", "silt", "sine", "sing", "sink", "sins", "sips", "sire", "site",
    "sits", "size", "skew", "skid", "skim", "skin", "skip", "skis", "skit", "slab",
    "slag", "slam", "slap", "slat", "slaw", "slay", "sled", "slew", "slid", "slim",
    "sling", "slip", "slit", "slob", "sloe", "slog", "slop", "slot", "slow", "slue",
    "slug", "slum", "slur", "slut", "smog", "smug", "smut", "snag", "snap", "snip",
    "snob", "snot", "snow", "snub", "snug", "soak", "soap", "soar", "sobs", "sock",
    "soda", "sofa", "soft", "soil", "sold", "sole", "solo", "soma", "some", "song",
    "sons", "soon", "soot", "sops", "sore", "sort", "soul", "soup", "sour", "sous",
    "sown", "sows", "soya", "soys", "spam", "span", "spar", "spas", "spat", "spec",
    "sped", "spew", "spin", "spit", "spot", "spry", "spud", "spun", "spur", "stab",
    "stag", "stan", "star", "stat", "stay", "stem", "step", "stew", "stir", "stop",
    "stow", "stub", "stud", "stun", "subs", "such", "suds", "sued", "suer", "sues",
    "suit", "sulk", "sumo", "sums", "sung", "sunk", "suns", "supe", "sure", "surf",
    "surg", "swab", "swag", "swam", "swan", "swap", "swat", "sway", "swim", "swop",
    "swum", "sync", "tabs", "tack", "taco", "tact", "tags", "tail", "take", "tale",
    "talk", "tall", "tame", "tamp", "tang", "tank", "tans", "tape", "taps", "tara",
    "tare", "tarn", "taro", "tarp", "tars", "tart", "task", "tate", "taut", "taxi",
    "teak", "teal", "team", "tear", "teas", "teat", "tech", "teed", "teem", "teen",
    "tees", "tell", "temp", "tend", "tens", "tent", "term", "tern", "test", "text",
    "than", "that", "thaw", "thee", "them", "then", "thew", "they", "thin", "this",
    "thou", "thud", "thug", "thus", "tick", "tide", "tidy", "tied", "tier", "ties",
    "tiff", "tift", "tile", "till", "tilt", "time", "tina", "tine", "ting", "tins",
    "tint", "tiny", "tips", "tire", "toad", "tock", "toes", "toff", "tofu", "toga",
    "togs", "toil", "told", "toll", "tomb", "tome", "toms", "tone", "tong", "tons",
    "tony", "took", "tool", "toot", "tops", "tore", "torn", "tort", "tory", "toss",
    "tote", "tots", "tour", "tout", "town", "toys", "trad", "tram", "trap", "tray",
    "tree", "trek", "trey", "trim", "trio", "trip", "trod", "trot", "troy", "true",
    "tsar", "tuba", "tube", "tubs", "tuck", "tuft", "tugs", "tuna", "tune", "tung",
    "tunk", "turf", "turk", "turn", "tusk", "tutu", "twig", "twin", "twit", "type",
    "typo", "tyre", "ugly", "ulna", "undo", "unit", "unto", "upon", "urea", "urge",
    "uric", "urns", "used", "user", "uses", "utah", "vail", "vain", "vale", "vamp",
    "vane", "vans", "vary", "vase", "vast", "vats", "veal", "veer", "veil", "vein",
    "vela", "vend", "vent", "verb", "vera", "vers", "very", "vest", "veto", "vets",
    "vial", "vice", "vida", "vied", "vies", "view", "vile", "vill", "vine", "vino",
    "vins", "vint", "viny", "viol", "visa", "vise", "void", "volt", "vote", "vows",
    "wade", "wads", "waft", "wage", "wags", "waif", "wail", "wait", "wake", "walk",
    "wall", "walt", "wand", "wane", "want", "ward", "ware", "warm", "warn", "warp",
    "wars", "wart", "wary", "wash", "wasp", "wave", "wavy", "waxy", "ways", "weak",
    "weal", "wean", "wear", "webb", "weds", "weed", "week", "weep", "weft", "weir",
    "well", "welt", "went", "wept", "were", "west", "wets", "what", "when", "whet",
    "whey", "whim", "whip", "whir", "whit", "whom", "whop", "wick", "wide", "wife",
    "wigs", "wild", "wile", "will", "wilt", "wily", "wimp", "wind", "wine", "wing",
    "wink", "wins", "wipe", "wire", "wiry", "wise", "wish", "wisp", "with", "wits",
    "woes", "woke", "wolf", "womb", "wont", "wood", "woof", "wool", "woos", "word",
    "wore", "work", "worm", "worn", "wort", "wove", "wows", "wrap", "wren", "writ",
    "wynn", "xray", "yale", "yank", "yard", "yarn", "yawn", "yeah", "year", "yell",
    "yelp", "yens", "yeti", "yews", "yoke", "yolk", "york", "your", "yowl", "yuan",
    "yuck", "yule", "yuma", "yurt", "zeal", "zebu", "zeds", "zeke", "zero", "zest",
    "zeta", "zeus", "zinc", "zing", "zion", "zips", "zits", "zone", "zonk", "zoom",
    "zoos", "zulu", "zuni"
]


class PasswordGenerator:
    """Класс для генерации паролей с различными параметрами сложности"""

    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(self, length=12, use_uppercase=True, use_digits=True,
                 use_special=True, exclude_ambiguous=False, custom_chars=None):
        """
        Генерирует случайный пароль с заданными параметрами

        Args:
            length (int): Длина пароля
            use_uppercase (bool): Использовать заглавные буквы
            use_digits (bool): Использовать цифры
            use_special (bool): Использовать специальные символы
            exclude_ambiguous (bool): Исключить похожие символы (0, O, l, 1, I)
            custom_chars (str): Кастомный набор символов (игнорирует другие опции)

        Returns:
            str: Сгенерированный пароль
        """
        if length < 4:
            raise ValueError("Длина пароля должна быть не менее 4 символов")

        # Если указан кастомный набор символов
        if custom_chars:
            if len(custom_chars) < 2:
                raise ValueError("Кастомный набор должен содержать минимум 2 символа")
            charset = custom_chars
            required_chars = [random.choice(charset)]
        else:
            # Формируем набор символов
            charset = self.lowercase
            required_chars = [random.choice(self.lowercase)]

            if use_uppercase:
                charset += self.uppercase
                required_chars.append(random.choice(self.uppercase))

            if use_digits:
                charset += self.digits
                required_chars.append(random.choice(self.digits))

            if use_special:
                charset += self.special
                required_chars.append(random.choice(self.special))

            # Исключаем похожие символы если нужно
            if exclude_ambiguous:
                ambiguous = "0Ol1I"
                charset = ''.join(c for c in charset if c not in ambiguous)

        if not charset:
            raise ValueError("Должен быть выбран хотя бы один тип символов")

        # Генерируем оставшиеся символы
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [random.choice(charset) for _ in range(remaining_length)]

        # Перемешиваем символы
        random.shuffle(password_chars)

        return ''.join(password_chars)

    def generate_multiple(self, count=1, **kwargs):
        """
        Генерирует несколько паролей

        Args:
            count (int): Количество паролей
            **kwargs: Параметры для метода generate()

        Returns:
            list: Список сгенерированных паролей
        """
        return [self.generate(**kwargs) for _ in range(count)]

    def generate_diceware(self, words=5, separator="-", capitalize=False, add_number=False):
        """
        Генерирует запоминающийся пароль по методу Diceware

        Args:
            words (int): Количество слов (по умолчанию: 5)
            separator (str): Разделитель между словами (по умолчанию: "-")
            capitalize (bool): Капитализировать первую букву каждого слова
            add_number (bool): Добавить случайное число в конец

        Returns:
            str: Сгенерированный пароль из слов
        """
        if words < 3:
            raise ValueError("Количество слов должно быть не менее 3")
        if words > 10:
            raise ValueError("Количество слов не должно превышать 10")

        # Выбираем случайные слова из словаря
        selected_words = random.choices(DICEWARE_WORDLIST, k=words)

        # Капитализация если нужно
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]

        # Собираем пароль
        password = separator.join(selected_words)

        # Добавляем число если нужно
        if add_number:
            password += separator + str(random.randint(0, 9999))

        return password

    def generate_diceware_multiple(self, count=1, **kwargs):
        """
        Генерирует несколько diceware паролей

        Args:
            count (int): Количество паролей
            **kwargs: Параметры для метода generate_diceware()

        Returns:
            list: Список сгенерированных паролей
        """
        return [self.generate_diceware(**kwargs) for _ in range(count)]


class CustomFormatter(argparse.RawDescriptionHelpFormatter):
    """Кастомный форматтер для скрытия metavar у определённых опций"""
    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            parts = []
            # Если есть короткая опция
            if action.option_strings:
                parts.extend(action.option_strings)
            return ', '.join(parts)

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Использование: '
        return super().add_usage(usage, actions, groups, prefix)

    def format_help(self):
        help_text = super().format_help()
        # Заменяем "options:" на "Опции:"
        help_text = help_text.replace('options:', 'Опции:')
        help_text = help_text.replace('optional arguments:', 'Опции:')
        return help_text


class CustomArgumentParser(argparse.ArgumentParser):
    """Кастомный парсер с улучшенным выводом ошибок"""
    def error(self, message):
        """Переопределяем вывод ошибок"""
        self.print_usage(sys.stderr)
        sys.stderr.write(f"{self.prog}: error: {message}\n")
        sys.stderr.write("Используйте флаг '-h' для просмотра справки\n")
        sys.exit(2)


def pluralize_password(count):
    """
    Возвращает правильную форму слова "пароль" в зависимости от числа

    Args:
        count (int): Количество паролей

    Returns:
        str: "пароль", "пароля" или "паролей"
    """
    if count % 100 in (11, 12, 13, 14):
        return "паролей"

    last_digit = count % 10
    if last_digit == 1:
        return "пароль"
    elif last_digit in (2, 3, 4):
        return "пароля"
    else:
        return "паролей"


def check_password_strength(password):
    """
    Проверяет силу пароля

    Args:
        password (str): Пароль для проверки

    Returns:
        tuple: (баллы, уровень, описание)
    """
    score = 0
    feedback = []

    # Длина пароля
    length = len(password)
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    # Наличие разных типов символов
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    char_types = sum([has_lower, has_upper, has_digit, has_special])
    score += char_types

    # Разнообразие символов (уникальность)
    unique_chars = len(set(password))
    uniqueness_ratio = unique_chars / length if length > 0 else 0
    if uniqueness_ratio > 0.8:
        score += 2
    elif uniqueness_ratio > 0.6:
        score += 1

    # Определение уровня
    if score >= 9:
        level = "Очень сильный"
    elif score >= 7:
        level = "Сильный"
    elif score >= 5:
        level = "Средний"
    else:
        level = "Слабый"

    # Формируем описание
    details = []
    details.append(f"Длина: {length}")
    details.append(f"Разнообразие: {unique_chars}/{length}")

    types = []
    if has_lower:
        types.append("строчные")
    if has_upper:
        types.append("заглавные")
    if has_digit:
        types.append("цифры")
    if has_special:
        types.append("спецсимволы")

    details.append(f"Типы: {', '.join(types)}")

    return score, level, " | ".join(details)


def save_to_file(passwords, filename, length, count):
    """
    Сохраняет пароли в файл

    Args:
        passwords (list): Список паролей для сохранения
        filename (str): Имя файла для сохранения
        length (int): Длина паролей
        count (int): Количество паролей
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Генератор паролей\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n\n")

            if count == 1:
                f.write(f"{passwords[0]}\n")
            else:
                f.write(f"Сгенерировано {count} {pluralize_password(count)} (длина: {length})\n\n")
                for i, pwd in enumerate(passwords, 1):
                    f.write(f"{i:2d}. {pwd}\n")

        print(f"Пароли сохранены в файл: {filename}")
    except IOError as e:
        print(f"Ошибка при сохранении в файл: {e}", file=sys.stderr)


def ask_yes_no(prompt, default=True):
    """
    Спрашивает у пользователя да/нет

    Args:
        prompt (str): Вопрос для пользователя
        default (bool): Значение по умолчанию

    Returns:
        bool: True или False
    """
    default_hint = "[Д/н]" if default else "[д/Н]"
    while True:
        answer = input(f"{prompt} {default_hint}: ").strip().lower()
        if answer == "":
            return default
        if answer in ("д", "да", "y", "yes"):
            return True
        if answer in ("н", "нет", "n", "no"):
            return False
        print("Пожалуйста, введите 'д' (да) или 'н' (нет)")


def ask_int(prompt, default, min_val=1, max_val=1000):
    """
    Спрашивает у пользователя число

    Args:
        prompt (str): Вопрос для пользователя
        default (int): Значение по умолчанию
        min_val (int): Минимальное значение
        max_val (int): Максимальное значение

    Returns:
        int: Введённое число
    """
    while True:
        answer = input(f"{prompt} [{default}]: ").strip()
        if answer == "":
            return default
        try:
            value = int(answer)
            if min_val <= value <= max_val:
                return value
            print(f"Введите число от {min_val} до {max_val}")
        except ValueError:
            print("Пожалуйста, введите число")


def interactive_mode():
    """Интерактивный режим генерации паролей"""
    print("\n" + "="*50)
    print("  Генератор паролей - Интерактивный режим")
    print("="*50 + "\n")

    generator = PasswordGenerator()

    # Спрашиваем параметры
    length = ask_int("Длина пароля", default=12, min_val=4, max_val=128)
    count = ask_int("Количество паролей", default=1, min_val=1, max_val=100)

    print()
    use_uppercase = ask_yes_no("Использовать заглавные буквы?", default=True)
    use_digits = ask_yes_no("Использовать цифры?", default=True)
    use_special = ask_yes_no("Использовать спецсимволы (!@#$...)?", default=True)
    exclude_ambiguous = ask_yes_no("Исключить похожие символы (0, O, l, 1, I)?", default=False)

    print()
    show_strength = ask_yes_no("Показать оценку силы пароля?", default=False)
    save_file = ask_yes_no("Сохранить в файл?", default=False)

    filename = None
    if save_file:
        filename = input("Имя файла [passwords.txt]: ").strip()
        if not filename:
            filename = "passwords.txt"

    # Генерируем пароли
    print("\n" + "-"*50)
    print("Генерация...")
    print("-"*50 + "\n")

    try:
        passwords = generator.generate_multiple(
            count=count,
            length=length,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_special=use_special,
            exclude_ambiguous=exclude_ambiguous
        )

        # Выводим результат
        if count == 1:
            print(f"Пароль: {passwords[0]}")
            if show_strength:
                score, level, details = check_password_strength(passwords[0])
                print(f"\nСила пароля: {level}")
                print(f"Детали: {details}")
        else:
            print(f"Сгенерировано {count} {pluralize_password(count)}:\n")
            for i, pwd in enumerate(passwords, 1):
                if show_strength:
                    score, level, details = check_password_strength(pwd)
                    print(f"{i:2d}. {pwd}  [{level}]")
                else:
                    print(f"{i:2d}. {pwd}")

        # Сохраняем в файл
        if filename:
            print()
            save_to_file(passwords, filename, length, count)

        print()

    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Главная функция CLI"""
    parser = CustomArgumentParser(
        description='Генератор случайных паролей с настройкой сложности',
        formatter_class=CustomFormatter,
        usage='%(prog)s [опции]',
        add_help=False,
        epilog="""
Примеры:
  %(prog)s -l 16                     # Генерация пароля длиной 16 символов
  %(prog)s -l 20 --no-special        # Пароль без спецсимволов
  %(prog)s -l 12 -c 5                # Генерация 5 паролей
  %(prog)s -l 16 --exclude-ambiguous # Пароль без похожих символов
  %(prog)s -s -l 10                  # Простой пароль
  %(prog)s --complex                 # Максимально сложный пароль
  %(prog)s -l 16 -c 3 -o passwords.txt # Сохранить 3 пароля в файл
  %(prog)s -l 10 --custom-chars "abc123!@#" # Пароль из заданных символов
  %(prog)s -i                        # Интерактивный режим
  %(prog)s -d                        # Diceware пароль (5 слов)
  %(prog)s -d --words 6 --capitalize # Diceware с 6 словами и заглавными буквами
  %(prog)s -d --add-number -c 3      # 3 diceware пароля с числом в конце
        """
    )

    parser.add_argument('-h', '--help', action='help',
                        help='Показать справку')

    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Интерактивный режим')

    parser.add_argument('-l', '--length', type=int, default=12,
                        help='Длина пароля (по умолчанию: 12)')

    parser.add_argument('-c', '--count', type=int, default=1,
                        help='Количество генерируемых паролей (по умолчанию: 1)')

    parser.add_argument('--no-uppercase', action='store_true',
                        help='Не использовать заглавные буквы')

    parser.add_argument('--no-digits', action='store_true',
                        help='Не использовать цифры')

    parser.add_argument('--no-special', action='store_true',
                        help='Не использовать специальные символы')

    parser.add_argument('--exclude-ambiguous', action='store_true',
                        help='Исключить похожие символы (0, O, l, 1, I)')

    parser.add_argument('-s', '--simple', action='store_true',
                        help='Простой режим (только буквы и цифры)')

    parser.add_argument('--complex', action='store_true',
                        help='Сложный режим (все типы символов, длина 20)')

    parser.add_argument('-o', '--output', type=str, metavar='FILE',
                        help='Сохранить пароли в файл')

    parser.add_argument('--show-strength', action='store_true',
                        help='Показать оценку силы пароля')

    parser.add_argument('--custom-chars', type=str, metavar='CHARS',
                        help='Кастомный набор символов для пароля (например: "abc123!@#")')

    parser.add_argument('-d', '--diceware', action='store_true',
                        help='Режим diceware (запоминающиеся пароли из слов)')

    parser.add_argument('--words', type=int, default=5,
                        help='Количество слов для diceware (по умолчанию: 5)')

    parser.add_argument('--separator', type=str, default='-',
                        help='Разделитель между словами (по умолчанию: "-")')

    parser.add_argument('--capitalize', action='store_true',
                        help='Капитализировать первую букву каждого слова')

    parser.add_argument('--add-number', action='store_true',
                        help='Добавить случайное число в конец')

    args = parser.parse_args()

    # Интерактивный режим
    if args.interactive:
        interactive_mode()
        return

    try:
        generator = PasswordGenerator()

        # Diceware режим
        if args.diceware:
            passwords = generator.generate_diceware_multiple(
                count=args.count,
                words=args.words,
                separator=args.separator,
                capitalize=args.capitalize,
                add_number=args.add_number
            )

            # Выводим результат
            if args.count == 1:
                print(passwords[0])
            else:
                print(f"\n{'='*50}")
                print(f"  Сгенерировано {args.count} {pluralize_password(args.count)} (diceware)")
                print(f"{'='*50}\n")
                for i, pwd in enumerate(passwords, 1):
                    print(f"{i:2d}. {pwd}")
                print()

            # Сохраняем в файл если указан флаг -o
            if args.output:
                save_to_file(passwords, args.output, args.words, args.count)

            return

        # Применяем предустановленные режимы
        if args.simple:
            use_uppercase = True
            use_digits = True
            use_special = False
            exclude_ambiguous = True
        elif args.complex:
            args.length = max(args.length, 20)
            use_uppercase = True
            use_digits = True
            use_special = True
            exclude_ambiguous = False
        else:
            use_uppercase = not args.no_uppercase
            use_digits = not args.no_digits
            use_special = not args.no_special
            exclude_ambiguous = args.exclude_ambiguous

        # Генерируем пароли
        passwords = generator.generate_multiple(
            count=args.count,
            length=args.length,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_special=use_special,
            exclude_ambiguous=exclude_ambiguous,
            custom_chars=args.custom_chars
        )

        # Выводим результат
        if args.count == 1:
            print(passwords[0])
            if args.show_strength:
                score, level, details = check_password_strength(passwords[0])
                print(f"\nСила пароля: {level}")
                print(f"Детали: {details}")
        else:
            print(f"\n{'='*50}")
            print(f"  Сгенерировано {args.count} {pluralize_password(args.count)} (длина: {args.length})")
            print(f"{'='*50}\n")
            for i, pwd in enumerate(passwords, 1):
                if args.show_strength:
                    score, level, details = check_password_strength(pwd)
                    print(f"{i:2d}. {pwd}  {level}")
                else:
                    print(f"{i:2d}. {pwd}")
            print()

        # Сохраняем в файл если указан флаг -o
        if args.output:
            save_to_file(passwords, args.output, args.length, args.count)

    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
