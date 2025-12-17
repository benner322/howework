# Конвертер конфигурационного языка (Вариант 4)

## Что делает программа
Конвертирует файлы из специального формата в XML. Поддерживает:
- Числа в научной нотации (например, `1.5e2`)
- Массивы без запятых `[10 20 30]`
- Константы: `var имя значение`
- Вычисления: `${a b +}` (постфиксная запись)
- Функции: `pow()`, `max()`, `+`

## Как использовать

### Основная команда
```bash
python converter.py входной_файл.conf -o выходной_файл.xml
```

### Примеры команд

**Тест с вычислениями:**
```bash
python converter.py test_expr.conf -o test.xml
Get-Content test.xml
```

**Пример 1 - физика:**
```bash
python converter.py example1.conf -o physics.xml
Get-Content physics.xml
```

**Пример 2 - финансы:**
```bash
python converter.py example2.conf -o finance.xml
Get-Content finance.xml
```

**Пример 3 - игры:**
```bash
python converter.py example3.conf -o game.xml
Get-Content game.xml
```

### Проверка тестов
```bash
python test_converter.py
```
