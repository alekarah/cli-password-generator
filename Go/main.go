package main

import (
	"flag"
	"fmt"
	"math/rand"
	"os"
	"path/filepath"
	"strings"
	"time"
)

const (
	lowercase = "abcdefghijklmnopqrstuvwxyz"
	uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	digits    = "0123456789"
	special   = "!@#$%^&*()_+-=[]{}|;:,.<>?"
)

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
}

// Generate генерирует пароль с заданными параметрами
func (pg *PasswordGenerator) Generate(opts GenerateOptions) (string, error) {
	if opts.Length < 4 {
		return "", fmt.Errorf("длина пароля должна быть не менее 4 символов")
	}

	// Формируем набор символов
	charset := lowercase
	var requiredChars []rune

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

		fmt.Fprintf(originalOutput, "\nПримеры:\n")
		fmt.Fprintf(originalOutput, "  %s -l 16                    # Генерация пароля длиной 16 символов\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 20 -no-special        # Пароль без спецсимволов\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 12 -c 5               # Генерация 5 паролей\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 16 -exclude-ambiguous # Пароль без похожих символов\n", progName)
		fmt.Fprintf(originalOutput, "  %s -s -l 10                 # Простой пароль\n", progName)
		fmt.Fprintf(originalOutput, "  %s -complex                 # Максимально сложный пароль\n", progName)
		fmt.Fprintf(originalOutput, "  %s -l 16 -c 3 -o passwords.txt # Сохранить 3 пароля в файл\n", progName)
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

	// Применяем предустановленные режимы
	opts := GenerateOptions{
		Length:           *length,
		UseUppercase:     !*noUppercase,
		UseDigits:        !*noDigits,
		UseSpecial:       !*noSpecial,
		ExcludeAmbiguous: *excludeAmbiguous,
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
