# Unit-Tests: Äquivalenzklassen und Grenzwerte

Eine Teamaufgabe zum Testen mit pytest. Sie bestimmen für kleine Python-Funktionen die Äquivalenzklassen und ihre
Grenzen und schreiben dafür Tests. Dabei arbeiten Sie mit Feature-Branches und Pull Requests. Im Code stecken Fehler,
die Tests mit einem Repräsentanten pro Klasse übersehen. Gute Grenztests finden sie. Am Ende stellen Sie Ihr
Ergebnis vor.

**Ablauf in Kürze**

1. Eine Person legt das Team-Repo an und lädt die anderen ein.
2. Jede Person übernimmt mindestens eine Datei unter `src/testing_examples/` und schreibt die Tests dafür, für jede
   Datei auf einem eigenen Branch.
3. Findet ein Test einen Fehler, beheben Sie ihn im Code. Alles kommt per Pull Request mit Review auf `main`.
4. Sie präsentieren, was Sie gemacht haben. Es gibt keine Abgabe: Bewertet wird nur die Präsentation.

## Worum es geht

Alle Eingaben durchzuprobieren ist unmöglich: Allein ein `float` hat rund 1,8 · 10¹⁹ mögliche Werte. Darum teilen Sie
die Eingaben in **Äquivalenzklassen** ein, also in Gruppen, die sich gleich verhalten, und testen einen Repräsentanten
pro Klasse. Fehler sitzen aber oft an den **Grenzen** zwischen den Klassen, nicht in ihrer Mitte. Dort testen Sie
zusätzlich.

**Ihre Aufgabe:** Schreiben Sie für jede Funktion Tests für alle Äquivalenzklassen und alle Grenzen. Der Docstring
jeder Funktion ist die Spezifikation. Weicht der Code davon ab, ist das ein Fehler im Code.

**Im Code stecken vier Fehler**, in `simple.py`, `discrete.py`, `intermediate.py` und `advanced.py` je einer, und
jeder sitzt an einer Grenze. `reciprocal` ist fehlerfrei. Finden Sie die Fehler mit Ihren Tests und beheben Sie sie.
Ein Verdacht beim Lesen des Codes zählt erst, wenn ein Test ihn bestätigt.

## Was drin ist

```text
src/testing_examples/
├── simple.py          reciprocal (schon getestet), absolute_value, sign
├── discrete.py        calculate_grade, classify_temperature, day_type
├── intermediate.py    reciprocal_sum, calculate_ray_slope, triangle_type
└── advanced.py        find_max, moving_average
tests/
└── test_reciprocal.py das Muster: alle Tests für reciprocal
```

## So gehen Sie vor

Gehen Sie für jede Funktion in vier Schritten vor. Wie das fertig aussieht, zeigt `tests/test_reciprocal.py`: oben im
Docstring die Klassen und Grenzen, darunter die Tests.

1. **Klassen bestimmen:** Welche verschiedenen Ergebnisse gibt es, auch Fehler und Sonderwerte wie `None`? Welche
   Eingaben führen zu welchem Ergebnis? Lesen Sie dafür den Docstring und den Code. Eine Klasse bekommt einen
   Repräsentanten, keine fünf.
2. **Grenzen finden:** Wo wechselt das Ergebnis? Typisch sind null und Werte nahe null, Schwellenwerte, leere Listen,
   Listen mit einem oder zwei Elementen und die Ränder des erlaubten Bereichs. Bei Texten sind es z. B. der leere
   Text, eine andere Groß- und Kleinschreibung und ein Zeichen zu viel oder zu wenig.
3. **An jeder Grenze dreimal testen:** knapp darunter, genau darauf, knapp darüber, also z. B. `59.99`, `60.0` und
   `60.01` für eine Schwelle bei 60. Wirft eine Seite der Grenze einen Fehler, testen Sie diese Seite in einem eigenen
   Test mit `pytest.raises`.
4. **Sonderwerte testen, wo der Docstring ihr Verhalten festlegt:** `-0.0`, `5e-324` (der kleinste positive Float),
   `sys.float_info.min`, `sys.float_info.max`, `math.inf` und `math.nan`. Sagt der Docstring zu einem Wert nichts,
   notieren Sie ihn als offene Frage im Docstring Ihrer Testdatei, statt ihn zu testen. Eingaben, die nicht zum
   Typ-Hinweis passen (etwa `None` statt eines Strings), testen Sie nicht.

Schreiben Sie die Klassen und Grenzen wie im Muster in den Docstring am Anfang Ihrer Testdatei. Für jeden Test gilt:

- **Ein Verhalten pro Test,** mit einem Namen, der es nennt: `test_calculate_grade_boundary_exactly_90` statt `test_3`.
- **Erwartete Werte fest eintragen,** nachgerechnet von Hand, nie im Test berechnen. Ein Taschenrechner oder Python als
  Taschenrechner ist erlaubt, nur nicht die Funktion, die Sie testen.
- **Kein `for` und kein `if` im Test.** Für mehrere Eingaben nehmen Sie `@pytest.mark.parametrize`.
- **Keine Mocks:** Die Funktionen rechnen nur, es gibt nichts zu ersetzen.

## pytest-Hilfsmittel

**Mehrere Fälle in einem Test:** `@pytest.mark.parametrize` macht aus jeder Zeile der Liste einen eigenen Testfall.
pytest meldet jeden Fall einzeln, Sie sehen also sofort, welcher Wert fehlschlägt. Ein Beispiel mit einer erfundenen
Funktion `passed(score)`, die ab 50 Punkten `True` liefert:

```python
@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (49.99, False),
        (50.0, True),
        (50.01, True),
    ],
)
def test_passed_boundary_50(score: float, expected: bool):
    """Grenze bei 50: knapp darunter, genau darauf, knapp darüber"""
    assert passed(score) == expected
```

Mit `pytest.param(50.0, True, id="genau darauf")` statt `(50.0, True)` bekommt ein Fall einen lesbaren Namen in der
Ausgabe. Schreiben Sie IDs ohne Umlaute (`knapp darueber`), sonst zeigt pytest `ü` als `\xfc`.

**Floats vergleichen:** Floats rechnen nicht exakt, `0.1 + 0.2 == 0.3` ist `False`. Vergleichen Sie darum mit Toleranz:
`assert result == pytest.approx(0.3)`. Mit `rel=1e-9` legen Sie eine relative, mit `abs=0.01` eine absolute Toleranz
fest. `pytest.approx` vergleicht auch ganze Listen: `assert result == pytest.approx([1.5, 2.5])`.

Für Werte nahe null hilft die Toleranz nicht: Ohne eigenes `abs` lässt `pytest.approx` immer `1e-12` Abstand zu, darum
gilt `0.0 == pytest.approx(5e-324)`. Ist das Ergebnis exakt, vergleichen Sie mit `==`, sonst mit
`pytest.approx(expected, rel=1e-9, abs=0)`.

Auch Ihre Testwerte runden: Soll eine Summe genau auf einer Grenze liegen, nehmen Sie Zahlen, die ein Float exakt
darstellt, z. B. `0.5` oder `2.0`, nicht `0.1` oder `0.2`. Bei Extremwerten gilt: `1.0 + 5e-324` ist `1.0`,
`5e-324 / 4` ist `0.0`, und `sys.float_info.max * 2` ist `inf`.

**Fehler erwarten:** Der Test besteht nur, wenn der Fehler wirklich geworfen wird:

```python
with pytest.raises(ValueError):
    int("abc")
```

Mit `pytest.raises(ValueError, match="invalid literal")` prüfen Sie zusätzlich den Text der Meldung.

**Sonderwerte prüfen:** `nan == nan` ist immer `False`. Prüfen Sie darum mit `math.isnan(result)`. Ob ein Wert endlich
ist, sagt `math.isfinite(result)`, und `None` prüfen Sie mit `assert result is None`.

**Tests ausführen:**

```bash
uv run pytest
uv run pytest -v
uv run pytest -k "grade"
```

Mit `-v` erscheint jeder Testfall einzeln, mit `-k "grade"` laufen nur Tests mit „grade“ im Namen, mit `-x` stoppt
pytest beim ersten Fehler, und `--tb=short` kürzt die Fehlerausgabe.

## Spielregeln im Team

Teams aus 2 bis 4 Personen.

1. Jede Person übernimmt **mindestens eine Datei** unter `src/testing_examples/` und legt dafür die Testdatei an:
   Tests für `discrete.py` kommen nach `tests/test_discrete.py`, entsprechend `test_simple.py`,
   `test_intermediate.py` und `test_advanced.py`. Zu viert übernimmt jede Person eine Datei, zu dritt eine Person
   `simple.py` und `advanced.py`, zu zweit z. B. eine Person `simple.py` und `discrete.py`, die andere
   `intermediate.py` und `advanced.py`.
2. Jede Datei bekommt einen **eigenen Feature-Branch** und einen eigenen Pull Request, z. B. `tests/discrete`.
3. **Fehler beheben Sie im Code, nicht im Test:** Ändern Sie nur die fehlerhafte Zeile, und zwar in einem eigenen
   Commit. Docstrings bleiben unverändert, denn sie sind die Spezifikation. Der Test, der den Fehler gefunden hat,
   bleibt in der Testdatei.
4. Auf `main` kommt nichts direkt, sondern nur per **Pull Request**, den **jemand anderes** aus dem Team reviewt.
5. Jeder Branch hält die Regeln aus `pyproject.toml` ein: **ruff und pyright ohne Fehler**. Die Einstellungen in
   `pyproject.toml` bleiben unverändert.

## Einrichten

Sie brauchen einen GitHub-Account, git, uv und einen Editor (z. B. VS Code).

1. **Team-Repo anlegen (eine Person):** Öffnen Sie
   <https://github.com/hs-aalen-software-engineering/unit-testing-equivalence-classes-template> und klicken Sie oben
   rechts auf **Use this template → Create a new repository**. Owner ist Ihr Account, der Name ist frei wählbar,
   Public oder Private geht beides. Dann **Create repository**.
2. **Team einladen (dieselbe Person):** Im neuen Repo **Settings → Collaborators → Add people**, die anderen über ihren
   GitHub-Namen einladen. Die Einladung kommt per E-Mail und muss angenommen werden.
3. **Klonen (alle):** Ersetzen Sie `<account>` und `<repo-name>` durch den GitHub-Namen des Owners und den Namen des
   Repos.

   ```bash
   git clone https://github.com/<account>/<repo-name>.git
   cd <repo-name>
   uv sync
   ```

4. **Startzustand prüfen (alle):**

   ```bash
   uv run pytest
   uv run ruff check
   uv run ruff format --check
   uv run pyright
   ```

   Erwartet: pytest meldet `12 passed`, das sind die Tests für `reciprocal`. Dazu `All checks passed!`,
   `7 files already formatted` und `0 errors, 0 warnings, 0 informations`. Eine zusätzliche Zeile
   `WARNING: there is a new pyright version available` können Sie ignorieren.

## Arbeitsablauf für Ihre Datei

1. **Branch anlegen:**

   ```bash
   git switch main
   git pull
   git switch -c tests/discrete
   ```

   `git switch` ist der neuere Befehl zum Wechseln von Branches (seit Git 2.23). Viele Anleitungen nutzen noch
   `git checkout`, das funktioniert genauso: `git checkout main` statt `git switch main` und
   `git checkout -b tests/discrete` statt `git switch -c tests/discrete`.

2. **Testdatei anlegen:** z. B. `tests/test_discrete.py`. Oben stehen wie im Muster die Klassen und Grenzen, darunter
   die Imports, z. B. `from testing_examples.discrete import calculate_grade`.
3. **Tests schreiben und ausführen:** `uv run pytest -v`. Schlägt ein Test fehl, prüfen Sie zuerst, ob Ihr erwarteter
   Wert zum Docstring passt. Passt er, haben Sie einen Fehler im Code gefunden. Beheben Sie ihn mit einer
   Ein-Zeilen-Änderung (Spielregel 3). Committet wird die Korrektur in Schritt 5, nach den Tests.
4. **Prüfen:**

   ```bash
   uv run ruff check --fix
   uv run ruff format
   uv run pyright
   uv run pytest
   ```

5. **Committen und pushen:** Erst die Tests, dann die Korrektur, jeweils als eigener Commit. Der erste Commit ist
   noch rot, das ist hier gewollt. In der zweiten Nachricht ersetzen Sie `FUNKTION` und `GRENZE`: So zeigt Ihr
   Branch-Graph später, welcher Test welchen Fehler gefunden hat.

   ```bash
   git add tests/test_discrete.py
   git commit -m "Tests für discrete.py ergänzen"
   git add src/testing_examples/discrete.py
   git commit -m "Fehler in FUNKTION an der Grenze GRENZE beheben"
   git push -u origin tests/discrete
   ```

6. **Pull Request:** Auf GitHub erscheint **Compare & pull request**. Ziel ist `main`. Tragen Sie rechts unter
   **Reviewers** jemanden aus dem Team ein und klicken Sie **Create pull request**.
7. **Review:** Die andere Person öffnet **Files changed** und prüft: Hat jede Klasse einen Test? Wird jede Grenze knapp
   darunter, genau darauf und knapp darüber getestet? Stimmen die erwarteten Werte mit dem Docstring überein? Ändert
   die Korrektur nur die fehlerhafte Zeile? Dann **Submit review** (in der älteren Ansicht **Review changes**) →
   **Approve** → **Submit review**.
8. **Mergen:** **Merge pull request → Confirm merge**. Danach holen sich alle den neuen Stand:
   `git switch main` (oder `git checkout main`) und `git pull`.

## Typische Fehlermeldungen

| Meldung | Ursache | Lösung |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'discrete'` | Import ohne Paketnamen | `from testing_examples.discrete import …` |
| `assert 0.30000000000000004 == 0.3` | Floats mit `==` verglichen | `pytest.approx(0.3)` |
| `Failed: DID NOT RAISE ValueError` | Der Code wirft die erwartete Exception nicht | Docstring prüfen: Irrt der Test oder der Code? |
| `TypeError: '>' not supported between instances of 'NoneType' and 'int'` | Ergebnis ist `None` | zuerst `assert result is not None`, dann vergleichen |
| Ihre Tests fehlen in der Ausgabe von `uv run pytest -v` | Datei liegt nicht in `tests/` oder heißt nicht `test_….py`, oder der Funktionsname beginnt nicht mit `test` | `tests/test_….py` und `def test_…()` |
| `N802 Function name … should be lowercase` | Großbuchstaben im Testnamen | nur Kleinbuchstaben, z. B. `test_calculate_grade_a` |

## KI-Werkzeuge

Ein LLM darf Ihnen Schreibarbeit abnehmen, das Testgerüst etwa oder die Liste für `parametrize`. Die Fachlogik
bleibt bei Ihnen: **Klassen, Grenzen und erwartete Werte bestimmen Sie selbst.** Ein LLM kennt Ihre Spezifikation
nicht so genau wie Sie, schreibt gern Assertions, die allein zu schwach sind, etwa nur `assert result is not None`,
rechnet erwartete Werte falsch aus und schlägt Mocks oder Schleifen vor, die hier nicht hingehören. Darum prüfen Sie jede Zeile, die Sie
übernehmen, und rechnen jeden erwarteten Wert selbst nach. Den Fehler im Code soll Ihr Test finden, nicht ein LLM:
Lassen Sie sich die Fehler nicht suchen.

| ✅ So ja: Sie geben Klassen und Werte vor | ❌ So nicht: die Denkarbeit abgeben |
| --- | --- |
| „Schreib einen parametrisierten pytest-Test für `calculate_grade` mit diesen Fällen: 89.99 → B, 90.0 → A, 90.01 → A.“ | „Schreib alle Tests für `discrete.py`.“ |
| „Was ist der Unterschied zwischen `rel` und `abs` bei `pytest.approx`?“ | „Welche Äquivalenzklassen hat `triangle_type`?“ |
| „Warum ist `nan == nan` in Python `False`?“ | „Finde den Fehler in dieser Funktion.“ |
| „pytest meldet `DID NOT RAISE`. Was bedeutet das?“ | „Mein Test schlägt fehl. Ändere ihn, damit er grün wird.“ |

**Faustregel:** Nennen Sie dem LLM die Klasse und das erwartete Verhalten. Was es daraus macht, prüfen Sie. In der
Präsentation erklären Sie jeden Test und jede Grenze selbst.

## Präsentation

Bewertet wird nur die Präsentation. Termin und Dauer (etwa 10 Minuten pro Team) gibt die Lehrperson bekannt.
Zeigen Sie:

- **Ihre Klassen und Grenzen:** Jede Person erklärt sie für eine Funktion ihrer Datei.
- **Ihre Grenztests:** einen parametrisierten Test und seine Ausgabe mit `uv run pytest -v`
- **Ihre Fehler:** welcher Test den Fehler gefunden hat, warum nur ein Grenztest ihn findet, und Ihre Korrektur
- **Ihren Branch-Graphen:** `git log --oneline --graph --all`
- **Live:** `uv run pytest` ganz grün, dazu `uv run ruff check` und `uv run pyright` ohne Fehler

Danach gibt es Fragen, zum Beispiel: Warum reicht ein Repräsentant pro Klasse? Welche Grenze war am schwersten zu
finden? Welcher Test hätte den Fehler nicht gefunden? Jede Person sollte auch die Tests der anderen grob erklären
können.
