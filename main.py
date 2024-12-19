import json
import re
import sys


class ConfigCompiler:
    """
    Класс для компиляции конфигурационного файла в определённый формат.
    Загружает JSON, компилирует его в формат, представленный строками, и сохраняет результат в выходной файл.
    """

    def __init__(self, input_file, output_file):
        """
        Инициализация класса с путями к входному и выходному файлам.
        
        Аргументы:
        input_file (str): Путь к файлу входных данных (в формате JSON).
        output_file (str): Путь к файлу для записи скомпилированного результата.
        """
        self.input_file = input_file
        self.output_file = output_file

    def parse_json(self):
        """
        Загружает данные из JSON-файла и возвращает их в виде Python-структуры (словарь или список).
        
        Возвращает:
        dict или list: Содержимое JSON-файла в виде соответствующей структуры данных Python.
        """
        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def write_output(self, output):
        """
        Записывает скомпилированный текст в выходной файл.
        
        Аргументы:
        output (str): Скомпилированный результат, который будет записан в файл.
        """
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(output)

    def compile(self, data, indent_level=0):
        """
        Рекурсивно компилирует данные в строковое представление с нужным отступом.
        Если данные представляют собой список или словарь, они рекурсивно обрабатываются.

        Аргументы:
        data (dict, list, str, int, float): Данные для компиляции.
        indent_level (int): Уровень отступов для текущего уровня данных (по умолчанию 0).

        Возвращает:
        str: Строковое представление скомпилированных данных.
        """
        # Определяем отступы в зависимости от уровня вложенности
        indent = '    ' * indent_level
        
        if isinstance(data, dict):
            # Если данные — это словарь, обрабатываем каждый ключ-значение
            result = []
            for key, value in data.items():
                result.append(f"{indent}(define {key} {self.compile(value, indent_level + 1)});")
            return f"{{\n" + "\n".join(result) + f"\n{indent}}}"
        
        elif isinstance(data, list):
            # Если данные — это список, рекурсивно обрабатываем каждый элемент
            result = [self.compile(value, indent_level) for value in data]
            return f"[{', '.join(result)}]"
        
        elif isinstance(data, str):
            # Если данные — это строка, обрабатываем её в функцию q()
            return f"q({data})"
        
        elif isinstance(data, (int, float)):
            # Если данные — это число, просто возвращаем его как строку
            return str(data)
        
        else:
            raise ValueError(f"Неизвестный тип данных: {type(data)}")

    def process_comments(self, content):
        """
        Удаляет комментарии из строки. Комментарии начинаются с '||' и продолжаются до конца строки.
        
        Аргументы:
        content (str): Строка с исходным текстом, из которой нужно удалить комментарии.

        Возвращает:
        str: Строка без комментариев.
        """
        # Удаляем всё, что идет после '||' (включая саму '||')
        return re.sub(r'\|\|.*', '', content)

    def handle_syntax(self, content):
        """
        Обрабатывает синтаксис в строке: корректирует все вхождения вида !{название},
        гарантируя правильный формат.
        
        Аргументы:
        content (str): Строка, в которой нужно обработать синтаксис.

        Возвращает:
        str: Строка с исправленным синтаксисом.
        """
        # Заменяем все вхождения вида !{...} на корректный формат
        content = re.sub(r'!\{([a-zA-Z][_a-zA-Z0-9]*)\}', r'!\{\1\}', content)
        return content

    def run(self):
        """
        Основной метод для выполнения всего процесса: 
        - загружает данные из JSON,
        - компилирует их в строку,
        - обрабатывает комментарии и синтаксис,
        - записывает результат в файл.
        """
        # Загружаем данные из входного JSON-файла
        data = self.parse_json()

        # Компилируем данные в строку с нужным форматированием
        output = self.compile(data)

        # Обрабатываем комментарии
        output = self.process_comments(output)

        # Обрабатываем синтаксис
        output = self.handle_syntax(output)

        # Записываем результат в выходной файл
        self.write_output(output)


if __name__ == '__main__':
    """
    Основная точка входа программы. Принимает аргументы командной строки:
    - Входной файл (в формате JSON),
    - Выходной файл (для записи скомпилированного результата).

    Программа выполняет все этапы обработки: загрузка данных, компиляция и сохранение.
    """
    # Проверка наличия нужных аргументов в командной строке
    if len(sys.argv) != 3:
        print("Использование: python config_compiler.py <входной_файл> <выходной_файл>")
        sys.exit(1)

    # Получаем аргументы командной строки
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Создаём экземпляр компилятора и запускаем его
    compiler = ConfigCompiler(input_file, output_file)
    compiler.run()

    # Сообщение о завершении работы программы
    print(f"Конфигурация успешно преобразована в файл: {output_file}")
