import sys
import argparse
import json
import math


class Parser:
    def __init__(self):
        self.vars = {}

    def parse(self, text):
        lines = text.strip().split('\n')
        result = {}
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            if line.startswith('var '):
                self.parse_var(line)
            elif ':' in line:
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip()
                result[key] = self.parse_value(val)
            else:
                # Массив в отдельной строке
                if line.startswith('[') and line.endswith(']'):
                    result['array'] = self.parse_array(line[1:-1])

            i += 1

        return result

    def parse_var(self, line):
        parts = line[4:].split()
        if len(parts) >= 2:
            name = parts[0]
            value = ' '.join(parts[1:])
            self.vars[name] = self.parse_simple_value(value)

    def parse_value(self, val):
        if val.startswith('[') and val.endswith(']'):
            return self.parse_array(val[1:-1])
        else:
            return self.parse_simple_value(val)

    def parse_simple_value(self, val):
        # Проверка на научную нотацию
        if 'e' in val.lower():
            try:
                return float(val)
            except:
                return val
        # Проверка на число
        try:
            if '.' in val:
                return float(val)
            else:
                return int(val)
        except:
            # Обработка константных выражений
            if val.startswith('${') and val.endswith('}'):
                return self.eval_expr(val[2:-1])
            return val

    def parse_array(self, content):
        items = content.strip().split()
        return [self.parse_simple_value(item) for item in items if item]

    def eval_expr(self, expr):
        # Постфиксная форма: ${имя 1 +}
        tokens = expr.strip().split()
        stack = []

        for token in tokens:
            if token in self.vars:
                stack.append(self.vars[token])
            elif token == '+':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif token == 'pow':
                b = stack.pop()
                a = stack.pop()
                stack.append(math.pow(a, b))
            elif token == 'max':
                b = stack.pop()
                a = stack.pop()
                stack.append(max(a, b))
            else:
                try:
                    num = float(token) if '.' in token else int(token)
                    stack.append(num)
                except:
                    pass

        return stack[0] if stack else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Входной файл')
    parser.add_argument('-o', '--output', required=True, help='Выходной XML файл')
    args = parser.parse_args()

    # Читаем входной файл
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    # Парсим
    parser_obj = Parser()
    data = parser_obj.parse(content)

    # Генерируем XML
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<config>']

    for key, value in data.items():
        if isinstance(value, list):
            xml_lines.append(f'  <{key}>')
            for item in value:
                xml_lines.append(f'    <item>{item}</item>')
            xml_lines.append(f'  </{key}>')
        else:
            xml_lines.append(f'  <{key}>{value}</{key}>')

    xml_lines.append('</config>')

    # Записываем в файл
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))

    print(f"Конфигурация сохранена в {args.output}")


if __name__ == '__main__':
    main()
