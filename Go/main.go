package main

import (
	"bufio"
	"flag"
	"fmt"
	"math/rand"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

const (
	lowercase = "abcdefghijklmnopqrstuvwxyz"
	uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	digits    = "0123456789"
	special   = "!@#$%^&*()_+-=[]{}|;:,.<>?"
)

// dicewareWordlist словарь для diceware генерации (2048 слов)
var dicewareWordlist = []string{
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
	"zoos", "zulu", "zuni",
}

// PasswordGenerator структура для генерации паролей
type PasswordGenerator struct {
	rng *rand.Rand
}

// NewPasswordGenerator создает новый генератор с инициализированным RNG
func NewPasswordGenerator() *PasswordGenerator {
	return &PasswordGenerator{
		rng: rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// GenerateOptions опции для генерации пароля
type GenerateOptions struct {
	Length            int
	UseUppercase      bool
	UseDigits         bool
	UseSpecial        bool
	ExcludeAmbiguous  bool
	CustomChars       string
}

// Generate генерирует пароль с заданными параметрами
func (pg *PasswordGenerator) Generate(opts GenerateOptions) (string, error) {
	if opts.Length < 4 {
		return "", fmt.Errorf("длина пароля должна быть не менее 4 символов")
	}

	var charset string
	var requiredChars []rune

	// Если указан кастомный набор символов
	if opts.CustomChars != "" {
		if len(opts.CustomChars) < 2 {
			return "", fmt.Errorf("кастомный набор должен содержать минимум 2 символа")
		}
		charset = opts.CustomChars
		requiredChars = append(requiredChars, rune(charset[pg.rng.Intn(len(charset))]))
	} else {
		// Формируем набор символов
		charset = lowercase
		// Добавляем обязательный символ нижнего регистра
		requiredChars = append(requiredChars, rune(lowercase[pg.rng.Intn(len(lowercase))]))

		if opts.UseUppercase {
			charset += uppercase
			requiredChars = append(requiredChars, rune(uppercase[pg.rng.Intn(len(uppercase))]))
		}

		if opts.UseDigits {
			charset += digits
			requiredChars = append(requiredChars, rune(digits[pg.rng.Intn(len(digits))]))
		}

		if opts.UseSpecial {
			charset += special
			requiredChars = append(requiredChars, rune(special[pg.rng.Intn(len(special))]))
		}

		// Исключаем похожие символы если нужно
		if opts.ExcludeAmbiguous {
			ambiguous := "0Ol1I"
			charset = removeChars(charset, ambiguous)
		}
	}

	if len(charset) == 0 {
		return "", fmt.Errorf("должен быть выбран хотя бы один тип символов")
	}

	// Генерируем оставшиеся символы
	passwordChars := make([]rune, len(requiredChars))
	copy(passwordChars, requiredChars)

	remainingLength := opts.Length - len(requiredChars)
	for i := 0; i < remainingLength; i++ {
		passwordChars = append(passwordChars, rune(charset[pg.rng.Intn(len(charset))]))
	}

	// Перемешиваем символы
	pg.shuffle(passwordChars)

	return string(passwordChars), nil
}

// GenerateMultiple генерирует несколько паролей
func (pg *PasswordGenerator) GenerateMultiple(count int, opts GenerateOptions) ([]string, error) {
	passwords := make([]string, 0, count)
	for i := 0; i < count; i++ {
		password, err := pg.Generate(opts)
		if err != nil {
			return nil, err
		}
		passwords = append(passwords, password)
	}
	return passwords, nil
}

// GenerateDiceware генерирует запоминающийся пароль по методу Diceware
func (pg *PasswordGenerator) GenerateDiceware(words int, separator string, capitalize bool, addNumber bool) (string, error) {
	if words < 3 {
		return "", fmt.Errorf("количество слов должно быть не менее 3")
	}
	if words > 10 {
		return "", fmt.Errorf("количество слов не должно превышать 10")
	}

	// Выбираем случайные слова из словаря
	selectedWords := make([]string, words)
	for i := 0; i < words; i++ {
		word := dicewareWordlist[pg.rng.Intn(len(dicewareWordlist))]
		if capitalize {
			word = strings.Title(word)
		}
		selectedWords[i] = word
	}

	// Собираем пароль
	password := strings.Join(selectedWords, separator)

	// Добавляем число если нужно
	if addNumber {
		password = password + separator + strconv.Itoa(pg.rng.Intn(10000))
	}

	return password, nil
}

// GenerateDicewareMultiple генерирует несколько diceware паролей
func (pg *PasswordGenerator) GenerateDicewareMultiple(count int, words int, separator string, capitalize bool, addNumber bool) ([]string, error) {
	passwords := make([]string, 0, count)
	for i := 0; i < count; i++ {
		password, err := pg.GenerateDiceware(words, separator, capitalize, addNumber)
		if err != nil {
			return nil, err
		}
		passwords = append(passwords, password)
	}
	return passwords, nil
}

// shuffle перемешивает слайс рун
func (pg *PasswordGenerator) shuffle(slice []rune) {
	for i := len(slice) - 1; i > 0; i-- {
		j := pg.rng.Intn(i + 1)
		slice[i], slice[j] = slice[j], slice[i]
	}
}

// removeChars удаляет определенные символы из строки
func removeChars(str, charsToRemove string) string {
	var result strings.Builder
	for _, c := range str {
		if !strings.ContainsRune(charsToRemove, c) {
			result.WriteRune(c)
		}
	}
	return result.String()
}

// pluralizePassword возвращает правильную форму слова "пароль" в зависимости от числа
func pluralizePassword(count int) string {
	// Исключения: 11, 12, 13, 14
	if count%100 >= 11 && count%100 <= 14 {
		return "паролей"
	}

	lastDigit := count % 10
	switch lastDigit {
	case 1:
		return "пароль"
	case 2, 3, 4:
		return "пароля"
	default:
		return "паролей"
	}
}

// PasswordStrength структура для информации о силе пароля
type PasswordStrength struct {
	Score   int
	Level   string
	Details string
}

// checkPasswordStrength проверяет силу пароля
func checkPasswordStrength(password string) PasswordStrength {
	score := 0

	// Длина пароля
	length := len(password)
	if length >= 16 {
		score += 3
	} else if length >= 12 {
		score += 2
	} else if length >= 8 {
		score += 1
	}

	// Наличие разных типов символов
	hasLower := false
	hasUpper := false
	hasDigit := false
	hasSpecial := false

	for _, c := range password {
		if c >= 'a' && c <= 'z' {
			hasLower = true
		} else if c >= 'A' && c <= 'Z' {
			hasUpper = true
		} else if c >= '0' && c <= '9' {
			hasDigit = true
		} else if strings.ContainsRune("!@#$%^&*()_+-=[]{}|;:,.<>?", c) {
			hasSpecial = true
		}
	}

	charTypes := 0
	if hasLower {
		charTypes++
	}
	if hasUpper {
		charTypes++
	}
	if hasDigit {
		charTypes++
	}
	if hasSpecial {
		charTypes++
	}
	score += charTypes

	// Разнообразие символов (уникальность)
	uniqueChars := make(map[rune]bool)
	for _, c := range password {
		uniqueChars[c] = true
	}
	uniquenessRatio := float64(len(uniqueChars)) / float64(length)
	if uniquenessRatio > 0.8 {
		score += 2
	} else if uniquenessRatio > 0.6 {
		score += 1
	}

	// Определение уровня
	var level string
	if score >= 9 {
		level = "Очень сильный"
	} else if score >= 7 {
		level = "Сильный"
	} else if score >= 5 {
		level = "Средний"
	} else {
		level = "Слабый"
	}

	// Формируем описание
	var types []string
	if hasLower {
		types = append(types, "строчные")
	}
	if hasUpper {
		types = append(types, "заглавные")
	}
	if hasDigit {
		types = append(types, "цифры")
	}
	if hasSpecial {
		types = append(types, "спецсимволы")
	}

	details := fmt.Sprintf("Длина: %d | Разнообразие: %d/%d | Типы: %s",
		length, len(uniqueChars), length, strings.Join(types, ", "))

	return PasswordStrength{
		Score:   score,
		Level:   level,
		Details: details,
	}
}

// askYesNo спрашивает у пользователя да/нет
func askYesNo(reader *bufio.Reader, prompt string, defaultVal bool) bool {
	defaultHint := "[Д/н]"
	if !defaultVal {
		defaultHint = "[д/Н]"
	}

	for {
		fmt.Printf("%s %s: ", prompt, defaultHint)
		answer, _ := reader.ReadString('\n')
		answer = strings.TrimSpace(strings.ToLower(answer))

		if answer == "" {
			return defaultVal
		}
		if answer == "д" || answer == "да" || answer == "y" || answer == "yes" {
			return true
		}
		if answer == "н" || answer == "нет" || answer == "n" || answer == "no" {
			return false
		}
		fmt.Println("Пожалуйста, введите 'д' (да) или 'н' (нет)")
	}
}

// askInt спрашивает у пользователя число
func askInt(reader *bufio.Reader, prompt string, defaultVal, minVal, maxVal int) int {
	for {
		fmt.Printf("%s [%d]: ", prompt, defaultVal)
		answer, _ := reader.ReadString('\n')
		answer = strings.TrimSpace(answer)

		if answer == "" {
			return defaultVal
		}

		value, err := strconv.Atoi(answer)
		if err != nil {
			fmt.Println("Пожалуйста, введите число")
			continue
		}
		if value < minVal || value > maxVal {
			fmt.Printf("Введите число от %d до %d\n", minVal, maxVal)
			continue
		}
		return value
	}
}

// interactiveMode запускает интерактивный режим
func interactiveMode() {
	fmt.Println()
	fmt.Println("==================================================")
	fmt.Println("  Генератор паролей - Интерактивный режим")
	fmt.Println("==================================================")
	fmt.Println()

	reader := bufio.NewReader(os.Stdin)
	generator := NewPasswordGenerator()

	// Спрашиваем параметры
	length := askInt(reader, "Длина пароля", 12, 4, 128)
	count := askInt(reader, "Количество паролей", 1, 1, 100)

	fmt.Println()
	useUppercase := askYesNo(reader, "Использовать заглавные буквы?", true)
	useDigits := askYesNo(reader, "Использовать цифры?", true)
	useSpecial := askYesNo(reader, "Использовать спецсимволы (!@#$...)?", true)
	excludeAmbiguous := askYesNo(reader, "Исключить похожие символы (0, O, l, 1, I)?", false)

	fmt.Println()
	showStrength := askYesNo(reader, "Показать оценку силы пароля?", false)
	saveFile := askYesNo(reader, "Сохранить в файл?", false)

	var filename string
	if saveFile {
		fmt.Print("Имя файла [passwords.txt]: ")
		filename, _ = reader.ReadString('\n')
		filename = strings.TrimSpace(filename)
		if filename == "" {
			filename = "passwords.txt"
		}
	}

	// Генерируем пароли
	fmt.Println()
	fmt.Println("--------------------------------------------------")
	fmt.Println("Генерация...")
	fmt.Println("--------------------------------------------------")
	fmt.Println()

	opts := GenerateOptions{
		Length:           length,
		UseUppercase:     useUppercase,
		UseDigits:        useDigits,
		UseSpecial:       useSpecial,
		ExcludeAmbiguous: excludeAmbiguous,
	}

	passwords, err := generator.GenerateMultiple(count, opts)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Ошибка: %v\n", err)
		os.Exit(1)
	}

	// Выводим результат
	if count == 1 {
		fmt.Printf("Пароль: %s\n", passwords[0])
		if showStrength {
			strength := checkPasswordStrength(passwords[0])
			fmt.Printf("\nСила пароля: %s\n", strength.Level)
			fmt.Printf("Детали: %s\n", strength.Details)
		}
	} else {
		fmt.Printf("Сгенерировано %d %s:\n\n", count, pluralizePassword(count))
		for i, pwd := range passwords {
			if showStrength {
				strength := checkPasswordStrength(pwd)
				fmt.Printf("%2d. %s  [%s]\n", i+1, pwd, strength.Level)
			} else {
				fmt.Printf("%2d. %s\n", i+1, pwd)
			}
		}
	}

	// Сохраняем в файл
	if filename != "" {
		fmt.Println()
		if err := saveToFile(passwords, filename, length, count); err != nil {
			fmt.Fprintf(os.Stderr, "Ошибка при сохранении в файл: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("Пароли сохранены в файл: %s\n", filename)
	}

	fmt.Println()
}

// saveToFile сохраняет пароли в файл
func saveToFile(passwords []string, filename string, length, count int) error {
	file, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("ошибка при создании файла: %v", err)
	}
	defer file.Close()

	// Записываем заголовок
	fmt.Fprintln(file, "Генератор паролей")
	fmt.Fprintf(file, "Дата: %s\n", time.Now().Format("2006-01-02 15:04:05"))
	fmt.Fprintln(file, "==================================================")
	fmt.Fprintln(file)

	// Записываем пароли
	if count == 1 {
		fmt.Fprintln(file, passwords[0])
	} else {
		fmt.Fprintf(file, "Сгенерировано %d %s (длина: %d)\n\n", count, pluralizePassword(count), length)
		for i, pwd := range passwords {
			fmt.Fprintf(file, "%2d. %s\n", i+1, pwd)
		}
	}

	return nil
}

func main() {
	// Определяем флаги командной строки (порядок как в Python версии)
	help := flag.Bool("h", false, "")
	interactive := flag.Bool("i", false, "")
	length := flag.Int("l", 12, "")
	count := flag.Int("c", 1, "")
	noUppercase := flag.Bool("no-uppercase", false, "")
	noDigits := flag.Bool("no-digits", false, "")
	noSpecial := flag.Bool("no-special", false, "")
	excludeAmbiguous := flag.Bool("exclude-ambiguous", false, "")
	simple := flag.Bool("s", false, "")
	complex := flag.Bool("complex", false, "")
	output := flag.String("o", "", "")
	showStrength := flag.Bool("show-strength", false, "")
	customChars := flag.String("custom-chars", "", "")
	diceware := flag.Bool("d", false, "")
	words := flag.Int("words", 5, "")
	separator := flag.String("separator", "-", "")
	capitalize := flag.Bool("capitalize", false, "")
	addNumber := flag.Bool("add-number", false, "")

	// Сохраняем оригинальный output для восстановления
	originalOutput := flag.CommandLine.Output()

	// Кастомная функция для вывода справки
	printFullHelp := func() {
		progName := filepath.Base(os.Args[0])
		fmt.Fprintf(originalOutput, "Генератор случайных паролей с настройкой сложности\n\n")
		fmt.Fprintf(originalOutput, "Использование:\n")
		fmt.Fprintf(originalOutput, "  %s [опции]\n\n", progName)
		fmt.Fprintf(originalOutput, "Опции:\n")

		// Кастомный вывод опций в нужном порядке и формате
		fmt.Fprintf(originalOutput, "  -h                      Показать справку\n")
		fmt.Fprintf(originalOutput, "  -i                      Интерактивный режим\n")
		fmt.Fprintf(originalOutput, "  -l                      Длина пароля (по умолчанию: 12)\n")
		fmt.Fprintf(originalOutput, "  -c                      Количество генерируемых паролей (по умолчанию: 1)\n")
		fmt.Fprintf(originalOutput, "  -no-uppercase           Не использовать заглавные буквы\n")
		fmt.Fprintf(originalOutput, "  -no-digits              Не использовать цифры\n")
		fmt.Fprintf(originalOutput, "  -no-special             Не использовать специальные символы\n")
		fmt.Fprintf(originalOutput, "  -exclude-ambiguous      Исключить похожие символы (0, O, l, 1, I)\n")
		fmt.Fprintf(originalOutput, "  -s                      Простой режим (только буквы и цифры)\n")
		fmt.Fprintf(originalOutput, "  -complex                Сложный режим (все типы символов, длина 20)\n")
		fmt.Fprintf(originalOutput, "  -o                      Сохранить пароли в файл\n")
		fmt.Fprintf(originalOutput, "  -show-strength          Показать оценку силы пароля\n")
		fmt.Fprintf(originalOutput, "  -custom-chars           Кастомный набор символов для пароля\n")
		fmt.Fprintf(originalOutput, "  -d                      Режим diceware (запоминающиеся пароли)\n")
		fmt.Fprintf(originalOutput, "  -words                  Количество слов для diceware (по умолчанию: 5)\n")
		fmt.Fprintf(originalOutput, "  -separator              Разделитель между словами (по умолчанию: \"-\")\n")
		fmt.Fprintf(originalOutput, "  -capitalize             Капитализировать первую букву каждого слова\n")
		fmt.Fprintf(originalOutput, "  -add-number             Добавить случайное число в конец\n")

		fmt.Fprintf(originalOutput, "\nПримеры:\n")
		fmt.Fprintf(originalOutput, "  %s -l 16                    # Генерация пароля длиной 16 символов\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 20 -no-special        # Пароль без спецсимволов\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 12 -c 5               # Генерация 5 паролей\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 16 -exclude-ambiguous # Пароль без похожих символов\n", progName)
		fmt.Fprintf(originalOutput, "  %s -s -l 10                 # Простой пароль\n", progName)
		fmt.Fprintf(originalOutput, "  %s -complex                 # Максимально сложный пароль\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 16 -c 3 -o passwords.txt # Сохранить 3 пароля в файл\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 10 -custom-chars \"abc123!@#\" # Пароль из заданных символов\n", progName)
		fmt.Fprintf(originalOutput, "  %s -i                       # Интерактивный режим\n", progName)
		fmt.Fprintf(originalOutput, "  %s -d                       # Diceware пароль (5 слов)\n", progName)
		fmt.Fprintf(originalOutput, "  %s -d -words 6 -capitalize  # Diceware с 6 словами и заглавными буквами\n", progName)
		fmt.Fprintf(originalOutput, "  %s -d -add-number -c 3      # 3 diceware пароля с числом в конце\n", progName)
	}

	flag.Usage = func() {
		// При ошибке парсинга выводим только подсказку
		fmt.Fprintf(os.Stderr, "Используйте флаг '-h' для просмотра справки\n")
	}

	flag.Parse()

	if *help {
		printFullHelp()
		os.Exit(0)
	}

	if *interactive {
		interactiveMode()
		return
	}

	// Diceware режим
	if *diceware {
		generator := NewPasswordGenerator()
		passwords, err := generator.GenerateDicewareMultiple(*count, *words, *separator, *capitalize, *addNumber)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Ошибка: %v\n", err)
			os.Exit(1)
		}

		// Выводим результат
		if *count == 1 {
			fmt.Println(passwords[0])
		} else {
			fmt.Println()
			fmt.Println("==================================================")
			fmt.Printf("  Сгенерировано %d %s (diceware)\n", *count, pluralizePassword(*count))
			fmt.Println("==================================================")
			fmt.Println()
			for i, pwd := range passwords {
				fmt.Printf("%2d. %s\n", i+1, pwd)
			}
			fmt.Println()
		}

		// Сохраняем в файл если указан флаг -o
		if *output != "" {
			if err := saveToFile(passwords, *output, *words, *count); err != nil {
				fmt.Fprintf(os.Stderr, "Ошибка при сохранении в файл: %v\n", err)
				os.Exit(1)
			}
			fmt.Printf("Пароли сохранены в файл: %s\n", *output)
		}

		return
	}

	// Применяем предустановленные режимы
	opts := GenerateOptions{
		Length:           *length,
		UseUppercase:     !*noUppercase,
		UseDigits:        !*noDigits,
		UseSpecial:       !*noSpecial,
		ExcludeAmbiguous: *excludeAmbiguous,
		CustomChars:      *customChars,
	}

	if *simple {
		opts.UseUppercase = true
		opts.UseDigits = true
		opts.UseSpecial = false
		opts.ExcludeAmbiguous = true
	} else if *complex {
		if opts.Length < 20 {
			opts.Length = 20
		}
		opts.UseUppercase = true
		opts.UseDigits = true
		opts.UseSpecial = true
		opts.ExcludeAmbiguous = false
	}

	// Создаем генератор и генерируем пароли
	generator := NewPasswordGenerator()
	passwords, err := generator.GenerateMultiple(*count, opts)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Ошибка: %v\n", err)
		os.Exit(1)
	}

	// Выводим результат
	if *count == 1 {
		fmt.Println(passwords[0])
		if *showStrength {
			strength := checkPasswordStrength(passwords[0])
			fmt.Printf("\nСила пароля: %s\n", strength.Level)
			fmt.Printf("Детали: %s\n", strength.Details)
		}
	} else {
		fmt.Println()
		fmt.Println("==================================================")
		fmt.Printf("  Сгенерировано %d %s (длина: %d)\n", *count, pluralizePassword(*count), opts.Length)
		fmt.Println("==================================================")
		fmt.Println()
		for i, pwd := range passwords {
			if *showStrength {
				strength := checkPasswordStrength(pwd)
				fmt.Printf("%2d. %s  %s\n", i+1, pwd, strength.Level)
			} else {
				fmt.Printf("%2d. %s\n", i+1, pwd)
			}
		}
		fmt.Println()
	}

	// Сохраняем в файл если указан флаг -o
	if *output != "" {
		if err := saveToFile(passwords, *output, opts.Length, *count); err != nil {
			fmt.Fprintf(os.Stderr, "Ошибка при сохранении в файл: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("Пароли сохранены в файл: %s\n", *output)
	}
}
