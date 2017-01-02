import math


class Point:
    """
    Classe que representa um ponto.
    Possui diversos operator overloads, permitindo realizar operações
     aritméticas com outro objeto Point (soma, subtração) ou algum valor
     númerico (multiplicação, divisão).
    Sobrescreve o operador de colchetes [] permitindo que o pygame imagine que a
     classe seja uma list ou tuple

    Logo, você pode usar essa classe como se fosse uma lista ou um dicionário
    """

    def __init__(self, point=None, y=None):
        """
        Construtor do point.
        :param point: outro Point, lista, tupla, dicionário (com 'x' e 'y') ou
                      valor numérico (int, float) representando x
        :param y: valor numérico (int, float) representando y
        """
        self.x = 0
        self.y = 0

        if type(point) is Point:
            self.x = point.x
            self.y = point.y
        elif type(point) in (list, tuple):
            self.x = point[0]
            self.y = point[1]
        elif type(point) is dict:
            if None not in (point.get('x'), point.get('y')):
                self.x = point['x']
                self.y = point['y']
        elif (type(point) in (int, float)) and (type(y) in (int, float)):
            x = point
            self.x = x
            self.y = y

    def int(self):
        """
        Converte as coordenadas pra inteiro e retorna. Chamado quando se usa a
         função int() pra converter o ponto
        :return: Point com coordenadas inteiras
        """
        return Point(
            int(self.x),
            int(self.y)
        )

    def __add__(self, other):
        """
        Realiza uma soma
        :param other: outro Point, lista, tupla ou dicionário (com 'x' e 'y')
        :return: um novo Point com o valor resultante
        """
        point = Point(other)
        res = Point(self)
        res.x += point.x
        res.y += point.y
        return res

    def __sub__(self, other):
        """
        Realiza uma subtração
        :param other: outro Point, lista, tupla ou dicionário (com 'x' e 'y')
        :return: um novo Point com o valor resultante
        """
        point = Point(other)
        res = Point(self)
        res.x -= point.x
        res.y -= point.y
        return res

    def __mul__(self, other):
        """
        Realiza uma multiplicação por uma constante
        :param other: qualquer valor numérico (int ou float)
        :return: um novo Point com o valor resultante
        """
        res = Point(self)
        if type(other) in (int, float):
            res.x *= other
            res.y *= other
        return res

    def __rmul__(self, other):
        """
        Realiza uma multiplicação à direita por uma constante
        :param other: qualquer valor numérico (int ou float)
        :return: um novo Point com o valor resultante
        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Realiza uma divisão por uma constante
        :param other: qualquer valor numérico (int ou float)
        :return: um novo Point com o valor resultante
        """
        res = Point(self)
        if type(other) in (int, float):
            res.x /= other
            res.y /= other
        return res

    def __rtruediv__(self, other):
        """
        Realiza uma divisão à direita por uma constante
        :param other: qualquer valor numérico (int ou float)
        :return: um novo Point com o valor resultante
        """
        res = Point(self)
        if type(other) in (int, float):
            res.x = other / res.x
            res.y = other / res.y
        return res

    def __floordiv__(self, other):
        """
        Realiza uma divisão inteira por uma constante
        :param other: qualquer valor numérico (int ou float)
        :return: um novo Point com o valor resultante
        """
        res = Point(self)
        if type(other) in (int, float):
            res.x //= other
            res.y //= other
        return res

    def __rfloordiv__(self, other):
        """
        Realiza uma divisão inteira à direita por uma constante
        :param other: qualquer valor numérico (int ou float)
        :return: um novo Point com o valor resultante
        """
        res = Point(self)
        if type(other) in (int, float):
            res.x = other // res.x
            res.y = other // res.y
        return res

    def __len__(self):
        """
        Método chamado quando usada a função len() (usada pelas funções internas
         do pygame)
        :return: 2
        """
        return 2

    def __getitem__(self, item):
        """
        Método chamado quando usado o operador [] no objeto para retornar um
         valor
        :param item: índice (list ou tuple) ou key (dict)
        :return: x ou y, dependendo de item
        """
        if type(item) is int:
            if item is 0:
                return self.x
            elif item is 1:
                return self.y
        elif type(item) is str:
            if item == 'x':
                return self.x
            elif item == 'y':
                return self.y
        return None

    def __setitem__(self, key, value):
        """
        Método chamado quando usado o operador [] no objeto para atribuir um
         valor
        :param key: indice (list) ou key (dict)
        :param value: valor a ser atribuido
        :return: None
        """
        if type(key) is int:
            if key is 0:
                self.x = value
            elif key is 1:
                self.y = value
        elif type(key) is str:
            if key == 'x':
                self.x = value
            elif key == 'y':
                self.y = value

    def __eq__(self, other):
        """
        Testa se os pontos são iguais
        :param other: outro Point, lista, tupla ou dicionário (com 'x' e 'y')
        :return: True se são iguais, False caso contrário
        """
        point = Point(other)
        return self.x == point.x and self.y == point.y

    def length(self):
        """
        Trata o objeto como se fosse um vetor geométrico 2D e retorna seu
         comprimento
        :return: comprimento do vetor
        """
        return math.hypot(self.x, self.y)

    def dot(self, other):
        """
        Trata o objeto como se fosse um vetor geométrico 2D e retorna o produto
         vetorial com outro vetor
        :param other: outro point
        :return: produto vetorial
        """
        point = Point(other)
        return self.x * point.x + self.y * point.y