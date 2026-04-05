import string
import pytest
from password_generator import PasswordGenerator, check_password_strength, pluralize_password


@pytest.fixture
def gen():
    return PasswordGenerator()


# ── generate() ──────────────────────────────────────────────────────────────

class TestGenerate:
    def test_default_length(self, gen):
        assert len(gen.generate(length=12)) == 12

    def test_custom_length(self, gen):
        for length in (4, 8, 20, 64):
            assert len(gen.generate(length=length)) == length

    def test_length_too_short_raises(self, gen):
        with pytest.raises(ValueError):
            gen.generate(length=3)

    def test_contains_lowercase(self, gen):
        pwd = gen.generate(length=20, use_uppercase=False, use_digits=False, use_special=False)
        assert any(c.islower() for c in pwd)

    def test_no_uppercase_when_disabled(self, gen):
        for _ in range(10):
            pwd = gen.generate(length=16, use_uppercase=False, use_digits=False, use_special=False)
            assert not any(c.isupper() for c in pwd)

    def test_no_digits_when_disabled(self, gen):
        for _ in range(10):
            pwd = gen.generate(length=16, use_uppercase=False, use_digits=False, use_special=False)
            assert not any(c.isdigit() for c in pwd)

    def test_no_special_when_disabled(self, gen):
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        for _ in range(10):
            pwd = gen.generate(length=16, use_uppercase=False, use_digits=False, use_special=False)
            assert not any(c in special for c in pwd)

    def test_uppercase_guaranteed(self, gen):
        # Генератор гарантирует минимум один символ каждого включённого типа
        found = False
        for _ in range(20):
            pwd = gen.generate(length=8, use_uppercase=True, use_digits=False, use_special=False)
            if any(c.isupper() for c in pwd):
                found = True
                break
        assert found

    def test_digits_guaranteed(self, gen):
        found = False
        for _ in range(20):
            pwd = gen.generate(length=8, use_uppercase=False, use_digits=True, use_special=False)
            if any(c.isdigit() for c in pwd):
                found = True
                break
        assert found

    def test_special_guaranteed(self, gen):
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        found = False
        for _ in range(20):
            pwd = gen.generate(length=8, use_uppercase=False, use_digits=False, use_special=True)
            if any(c in special for c in pwd):
                found = True
                break
        assert found

    def test_exclude_ambiguous(self, gen):
        ambiguous = set("0Ol1I")
        for _ in range(30):
            pwd = gen.generate(length=20, exclude_ambiguous=True)
            assert not any(c in ambiguous for c in pwd)

    def test_custom_chars_only(self, gen):
        charset = "abc"
        for _ in range(10):
            pwd = gen.generate(length=10, custom_chars=charset)
            assert all(c in charset for c in pwd)

    def test_custom_chars_too_short_raises(self, gen):
        with pytest.raises(ValueError):
            gen.generate(length=8, custom_chars="a")

    def test_passwords_are_different(self, gen):
        passwords = {gen.generate(length=16) for _ in range(10)}
        assert len(passwords) > 1


# ── generate_multiple() ──────────────────────────────────────────────────────

class TestGenerateMultiple:
    def test_returns_correct_count(self, gen):
        passwords = gen.generate_multiple(count=5, length=12)
        assert len(passwords) == 5

    def test_each_password_correct_length(self, gen):
        for pwd in gen.generate_multiple(count=5, length=14):
            assert len(pwd) == 14


# ── generate_diceware() ──────────────────────────────────────────────────────

class TestGenerateDiceware:
    def test_default_word_count(self, gen):
        pwd = gen.generate_diceware(words=5)
        assert len(pwd.split("-")) == 5

    def test_custom_separator(self, gen):
        pwd = gen.generate_diceware(words=4, separator="_")
        assert "_" in pwd
        assert len(pwd.split("_")) == 4

    def test_capitalize(self, gen):
        pwd = gen.generate_diceware(words=4, capitalize=True)
        for word in pwd.split("-"):
            assert word[0].isupper()

    def test_add_number(self, gen):
        pwd = gen.generate_diceware(words=4, add_number=True)
        parts = pwd.split("-")
        # Последняя часть должна быть числом
        assert parts[-1].isdigit()

    def test_too_few_words_raises(self, gen):
        with pytest.raises(ValueError):
            gen.generate_diceware(words=2)

    def test_too_many_words_raises(self, gen):
        with pytest.raises(ValueError):
            gen.generate_diceware(words=11)


# ── check_password_strength() ────────────────────────────────────────────────

class TestCheckPasswordStrength:
    def test_weak_password(self):
        score, level, _ = check_password_strength("abc")
        assert level == "Слабый"

    def test_strong_password(self):
        score, level, _ = check_password_strength("Abcdefgh1!XyZ@345")
        assert level in ("Сильный", "Очень сильный")

    def test_returns_tuple_of_three(self):
        result = check_password_strength("Test1!")
        assert len(result) == 3

    def test_score_increases_with_length(self):
        score_short, _, _ = check_password_strength("Ab1!")
        score_long, _, _ = check_password_strength("Ab1!" * 5)
        assert score_long > score_short


# ── pluralize_password() ─────────────────────────────────────────────────────

class TestPluralize:
    def test_one(self):
        assert pluralize_password(1) == "пароль"

    def test_two(self):
        assert pluralize_password(2) == "пароля"

    def test_five(self):
        assert pluralize_password(5) == "паролей"

    def test_eleven(self):
        assert pluralize_password(11) == "паролей"

    def test_twenty_one(self):
        assert pluralize_password(21) == "пароль"
