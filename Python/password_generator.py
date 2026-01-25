#!/usr/bin/env python3
"""
Генератор случайных паролей с настройкой сложности
"""

import random
import string
import argparse
import sys
from datetime import datetime


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

    args = parser.parse_args()

    # Интерактивный режим
    if args.interactive:
        interactive_mode()
        return

    try:
        generator = PasswordGenerator()

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
