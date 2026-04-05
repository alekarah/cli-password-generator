package main

import (
	"strings"
	"testing"
)

// ── helpers ──────────────────────────────────────────────────────────────────

func newGen() *PasswordGenerator {
	return NewPasswordGenerator()
}

func defaultOpts() GenerateOptions {
	return GenerateOptions{
		Length:       12,
		UseUppercase: true,
		UseDigits:    true,
		UseSpecial:   true,
	}
}

// ── Generate() ───────────────────────────────────────────────────────────────

func TestGenerateLength(t *testing.T) {
	gen := newGen()
	for _, length := range []int{4, 8, 16, 32, 64} {
		opts := defaultOpts()
		opts.Length = length
		pwd, err := gen.Generate(opts)
		if err != nil {
			t.Fatalf("length=%d: unexpected error: %v", length, err)
		}
		if len([]rune(pwd)) != length {
			t.Errorf("length=%d: got %d", length, len(pwd))
		}
	}
}

func TestGenerateTooShortReturnsError(t *testing.T) {
	gen := newGen()
	opts := defaultOpts()
	opts.Length = 3
	_, err := gen.Generate(opts)
	if err == nil {
		t.Error("expected error for length < 4, got nil")
	}
}

func TestGenerateNoUppercase(t *testing.T) {
	gen := newGen()
	opts := GenerateOptions{Length: 20, UseUppercase: false, UseDigits: false, UseSpecial: false}
	for i := 0; i < 10; i++ {
		pwd, _ := gen.Generate(opts)
		for _, c := range pwd {
			if c >= 'A' && c <= 'Z' {
				t.Fatalf("found uppercase in password %q", pwd)
			}
		}
	}
}

func TestGenerateNoDigits(t *testing.T) {
	gen := newGen()
	opts := GenerateOptions{Length: 20, UseUppercase: false, UseDigits: false, UseSpecial: false}
	for i := 0; i < 10; i++ {
		pwd, _ := gen.Generate(opts)
		for _, c := range pwd {
			if c >= '0' && c <= '9' {
				t.Fatalf("found digit in password %q", pwd)
			}
		}
	}
}

func TestGenerateNoSpecial(t *testing.T) {
	gen := newGen()
	specialChars := special
	opts := GenerateOptions{Length: 20, UseUppercase: false, UseDigits: false, UseSpecial: false}
	for i := 0; i < 10; i++ {
		pwd, _ := gen.Generate(opts)
		for _, c := range pwd {
			if strings.ContainsRune(specialChars, c) {
				t.Fatalf("found special char in password %q", pwd)
			}
		}
	}
}

func TestGenerateUppercaseGuaranteed(t *testing.T) {
	gen := newGen()
	opts := GenerateOptions{Length: 8, UseUppercase: true, UseDigits: false, UseSpecial: false}
	found := false
	for i := 0; i < 20; i++ {
		pwd, _ := gen.Generate(opts)
		for _, c := range pwd {
			if c >= 'A' && c <= 'Z' {
				found = true
				break
			}
		}
		if found {
			break
		}
	}
	if !found {
		t.Error("uppercase never appeared despite UseUppercase=true")
	}
}

func TestGenerateDigitsGuaranteed(t *testing.T) {
	gen := newGen()
	opts := GenerateOptions{Length: 8, UseUppercase: false, UseDigits: true, UseSpecial: false}
	found := false
	for i := 0; i < 20; i++ {
		pwd, _ := gen.Generate(opts)
		for _, c := range pwd {
			if c >= '0' && c <= '9' {
				found = true
				break
			}
		}
		if found {
			break
		}
	}
	if !found {
		t.Error("digit never appeared despite UseDigits=true")
	}
}

func TestGenerateExcludeAmbiguous(t *testing.T) {
	gen := newGen()
	opts := defaultOpts()
	opts.Length = 30
	opts.ExcludeAmbiguous = true
	ambiguous := "0Ol1I"
	for i := 0; i < 20; i++ {
		pwd, _ := gen.Generate(opts)
		for _, c := range pwd {
			if strings.ContainsRune(ambiguous, c) {
				t.Fatalf("ambiguous char %q found in password %q", c, pwd)
			}
		}
	}
}

func TestGenerateCustomChars(t *testing.T) {
	gen := newGen()
	charset := "abc"
	opts := GenerateOptions{Length: 10, CustomChars: charset}
	for i := 0; i < 10; i++ {
		pwd, _ := gen.Generate(opts)
		for _, c := range pwd {
			if !strings.ContainsRune(charset, c) {
				t.Fatalf("char %q not in custom charset, password: %q", c, pwd)
			}
		}
	}
}

func TestGenerateCustomCharsTooShort(t *testing.T) {
	gen := newGen()
	opts := GenerateOptions{Length: 8, CustomChars: "a"}
	_, err := gen.Generate(opts)
	if err == nil {
		t.Error("expected error for custom charset with 1 char")
	}
}

func TestGeneratePasswordsAreDifferent(t *testing.T) {
	gen := newGen()
	seen := make(map[string]bool)
	opts := defaultOpts()
	opts.Length = 16
	for i := 0; i < 10; i++ {
		pwd, _ := gen.Generate(opts)
		seen[pwd] = true
	}
	if len(seen) < 2 {
		t.Error("all generated passwords are identical")
	}
}

// ── GenerateMultiple() ───────────────────────────────────────────────────────

func TestGenerateMultipleCount(t *testing.T) {
	gen := newGen()
	passwords, err := gen.GenerateMultiple(5, defaultOpts())
	if err != nil {
		t.Fatal(err)
	}
	if len(passwords) != 5 {
		t.Errorf("expected 5 passwords, got %d", len(passwords))
	}
}

func TestGenerateMultipleEachLength(t *testing.T) {
	gen := newGen()
	opts := defaultOpts()
	opts.Length = 14
	passwords, _ := gen.GenerateMultiple(5, opts)
	for _, pwd := range passwords {
		if len([]rune(pwd)) != 14 {
			t.Errorf("expected length 14, got %d for %q", len(pwd), pwd)
		}
	}
}

// ── GenerateDiceware() ───────────────────────────────────────────────────────

func TestDicewareWordCount(t *testing.T) {
	gen := newGen()
	pwd, err := gen.GenerateDiceware(5, "-", false, false)
	if err != nil {
		t.Fatal(err)
	}
	parts := strings.Split(pwd, "-")
	if len(parts) != 5 {
		t.Errorf("expected 5 words, got %d: %q", len(parts), pwd)
	}
}

func TestDicewareCustomSeparator(t *testing.T) {
	gen := newGen()
	pwd, _ := gen.GenerateDiceware(4, "_", false, false)
	if !strings.Contains(pwd, "_") {
		t.Errorf("separator '_' not found in %q", pwd)
	}
	if len(strings.Split(pwd, "_")) != 4 {
		t.Errorf("expected 4 parts, got %d", len(strings.Split(pwd, "_")))
	}
}

func TestDicewareCapitalize(t *testing.T) {
	gen := newGen()
	pwd, _ := gen.GenerateDiceware(4, "-", true, false)
	for _, word := range strings.Split(pwd, "-") {
		if len(word) == 0 {
			continue
		}
		if word[0] < 'A' || word[0] > 'Z' {
			t.Errorf("word %q not capitalized in %q", word, pwd)
		}
	}
}

func TestDicewareAddNumber(t *testing.T) {
	gen := newGen()
	pwd, _ := gen.GenerateDiceware(4, "-", false, true)
	parts := strings.Split(pwd, "-")
	last := parts[len(parts)-1]
	for _, c := range last {
		if c < '0' || c > '9' {
			t.Errorf("last part %q is not a number in %q", last, pwd)
		}
	}
}

func TestDicewareTooFewWordsReturnsError(t *testing.T) {
	gen := newGen()
	_, err := gen.GenerateDiceware(2, "-", false, false)
	if err == nil {
		t.Error("expected error for words < 3")
	}
}

func TestDicewareTooManyWordsReturnsError(t *testing.T) {
	gen := newGen()
	_, err := gen.GenerateDiceware(11, "-", false, false)
	if err == nil {
		t.Error("expected error for words > 10")
	}
}

// ── checkPasswordStrength() ──────────────────────────────────────────────────

func TestStrengthWeak(t *testing.T) {
	result := checkPasswordStrength("abc")
	if result.Level != "Слабый" {
		t.Errorf("expected Слабый, got %q", result.Level)
	}
}

func TestStrengthStrong(t *testing.T) {
	result := checkPasswordStrength("Abcdefgh1!XyZ@345")
	if result.Level != "Сильный" && result.Level != "Очень сильный" {
		t.Errorf("expected Сильный or Очень сильный, got %q", result.Level)
	}
}

func TestStrengthScoreIncreasesWithLength(t *testing.T) {
	short := checkPasswordStrength("Ab1!")
	long := checkPasswordStrength("Ab1!Ab1!Ab1!Ab1!")
	if long.Score <= short.Score {
		t.Errorf("longer password should have higher score: short=%d, long=%d", short.Score, long.Score)
	}
}

// ── pluralizePassword() ──────────────────────────────────────────────────────

func TestPluralize(t *testing.T) {
	cases := []struct {
		n    int
		want string
	}{
		{1, "пароль"},
		{2, "пароля"},
		{5, "паролей"},
		{11, "паролей"},
		{21, "пароль"},
		{100, "паролей"},
	}
	for _, c := range cases {
		got := pluralizePassword(c.n)
		if got != c.want {
			t.Errorf("pluralizePassword(%d) = %q, want %q", c.n, got, c.want)
		}
	}
}

// ── removeChars() ────────────────────────────────────────────────────────────

func TestRemoveChars(t *testing.T) {
	result := removeChars("abcdefg", "ace")
	for _, c := range "ace" {
		if strings.ContainsRune(result, c) {
			t.Errorf("char %q should have been removed, result: %q", c, result)
		}
	}
	for _, c := range "bdfg" {
		if !strings.ContainsRune(result, c) {
			t.Errorf("char %q should remain, result: %q", c, result)
		}
	}
}
