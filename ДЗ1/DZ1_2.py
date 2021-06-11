from itertools import chain, combinations
from pprint import pp
 
 
def powerset(n):
    """
    Возвращает все подмножества множетсва = {1, 2, ..., n}
    :param n: Число n
    :return: Подмножества
    """
    s = range(n)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))
 
 
def read_func_from_file(file_name):
    """
    Функция читает из файла в виде списка наборы на которых БФ = истина
    :param file_name: Имя файла
    :return: Список наборов
    """
    with open(file_name) as f:
        return sorted([line.strip() for line in f.readlines()])
 
 
def create_coef_for_equation(num, n):
    """
    Функция создает верхнии и нижние коэффициенты для переменных в уравнении системы
    (shorturl.at/suHMO) (Укороченая ссылка на бауманскую википедию с МНК)
    :param num: Десятичное представление набора для данного уравнения
    :param n:Количество переменных
    :return: Индексы для уравнения в системе
    """
    num_base2_as_str = bin(num)[2:].rjust(n, '0')
    equation = set()
    for tup in powerset(n):
        down_index = ''.join(str(x) for x in tup)
        up_index = ''.join(num_base2_as_str[i] for i in tup)
        equation.add((down_index, up_index))
    return equation
 
 
def create_system(f):
    """
    Функция создает систему уравнений
    :param f: Булева Функция
    :return: Словарь(хэш-таблица) <-> система
    """
    set_of_true_nums = {int(num, base=2) for num in f}
    n = len(f[0])
    dict_sys = {num: (True if num in set_of_true_nums else False, create_coef_for_equation(num, n)) for num in
                range(2 ** n)}
    return dict_sys
 
 
def creat_set_of_zero_coef(sys):
    """
    Вспомогательная функция
    Находит все коэфициенты которые точно равны нулю (по уравнениям =0)
    :param sys: Система
    :return: Множество нулевых коэфф.
    """
    res_set = set()
    for tup in sys.values():
        if not tup[0]:
            res_set.update(tup[1])
    return res_set
 
 
def delete_false_from_system(sys):
    """
    Удаление уравнений  равных 0
    :param sys: Система уравнений
    :return: Обновленная система
    """
    set_key_for_del = set()
    for key, (val, _) in sys.items():
        if not val:
            set_key_for_del.add(key)
    for key in set_key_for_del:
        sys.pop(key)
 
 
def delete_zero_coef_from_system(sys, zeros):
    """
    Вычеркиваем из уравнений с 1 значением функции все коэффициенты равные 0, из уравнений с 0 значениями f
    :param sys:
    :param zeros:
    :return:
    """
    for key, (bool_val, cur_set) in sys.items():
        new_set = cur_set - zeros
        #print(new_set)
        sys[key] = (bool_val, new_set)
 
 
def get_final_coef_from_system(sys: dict):
    """
    Сортируем по минимальному коэфициенту и их кол-ву
    Выбираем из коэффициентов минимальной длинный самый частовстречаемый
    Удаляем уравнения с этим коэффициентом
    :param sys: Система
    :return: Список коэффициентов
    """
    exp = dict()
    res = []
    sort_key = sorted([k for k in sys.keys()], key=lambda k: len(min(sys[k][1], key=lambda tup: len(tup[0]))[0]))
    sort_key.sort(key=lambda k: len(sys[k][1]))
    for i, key in enumerate(sort_key):
        if sys.get(key, None) is None:
            continue
        min_len = len(min(sys[key][1], key=lambda tup: len(tup[0]))[0])
        all_min_el = sorted([el for el in sys[key][1] if len(el[0]) == min_len])
        min_el = all_min_el[0]
        if len(all_min_el) != 1:
            max_in_other = 0
            for el in all_min_el:
                cur_el_in_other = 0
                for other_key in sort_key:
                    if sys.get(other_key, None) is None:
                        continue
                    if el in sys[other_key][1]:
                        cur_el_in_other += 1
                if cur_el_in_other > max_in_other:
                    min_el = el
                    max_in_other = cur_el_in_other
        res.append(min_el)
        if i < 13:
            exp = sys.items()
        keys_for_delete = {key for key, (_, coef) in sys.items() if min_el in coef}
        for k in keys_for_delete:
            sys.pop(k)
        print(sys.items())
        
    print(exp)
    return res
 
 
if __name__ == '__main__':
    """
    Аналог main() в C++
    Вызывает необходимые функции в нужно порядке
    """
    file_with_func = 'nabory.txt'
    func = read_func_from_file(file_with_func)
    system = create_system(func)
    set_of_zero_coef = creat_set_of_zero_coef(system)
    delete_false_from_system(system)
    delete_zero_coef_from_system(system, set_of_zero_coef)
    final_coef = get_final_coef_from_system(system)
    pp(sorted(final_coef))