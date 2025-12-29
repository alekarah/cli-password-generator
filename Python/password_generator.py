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
                 use_special=True, exclude_ambiguous=False):
        """
        Генерирует случайный пароль с заданными параметрами

        Args:
            length (int): Длина пароля
            use_uppercase (bool): Использовать заглавные буквы
            use_digits (bool): Использовать цифры
            use_special (bool): Использовать специальные символы
            exclude_ambiguous (bool): Исключить похожие символы (0, O, l, 1, I)

        Returns:
            str: Сгенерированный пароль
        """
        if length < 4:
            raise ValueError("Длина пароля должна быть не менее 4 символов")

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
        """
    )

    parser.add_argument('-h', '--help', action='help',
                        help='Показать справку')

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

    args = parser.parse_args()

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
            exclude_ambiguous=exclude_ambiguous
        )

        # Выводим результат
        if args.count == 1:
            print(passwords[0])
        else:
            print(f"\n{'='*50}")
            print(f"  Сгенерировано {args.count} {pluralize_password(args.count)} (длина: {args.length})")
            print(f"{'='*50}\n")
            for i, pwd in enumerate(passwords, 1):
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
