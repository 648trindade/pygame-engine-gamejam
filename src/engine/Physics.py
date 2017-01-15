import math
from engine.Point import Point
from pygame import Rect


def mruv(pos_ini, vel_ini, accel, delta_time):
    """
    Calcula o movimento retilíneo uniforme variado
    :param pos_ini: Point -> posição inicial do objeto
    :param vel_ini: Point -> velocidade inicial do objeto em px/s
    :param accel: Point -> aceleração do objeto em px/s²
    :param delta_time: int -> variação de tempo em milisegundos
    :return: (Point, Point) -> posição e velocidade finais do objeto
    """
    time = delta_time / 1000
    pos_fin = Point(pos_ini) + Point(vel_ini) * time + Point(accel) * (time ** 2) / 2
    vel_fin = Point(vel_ini) + Point(accel) * time
    return (pos_fin, vel_fin)


def reflect(dir_ini, normal):
    """
    Calcula a reflexão de um objeto ao bater em um obstaculo com a normal fornecida
    :param dir_ini: Point -> direção do objeto
    :param normal: Point -> normal do obstaculo
    :return: Point -> nova direção
    """
    dir_ini = Point(dir_ini)
    return -2 * dir_ini.dot(normal) * normal + dir_ini

def distance_pt_rect(point, rect):
    """
    Retorna a distancia entre um ponto e um retangulo
    :param point: ponto
    :param rect: retangulo
    :return: float, distancia
    """
    dx = max(min(point[0], rect.right), rect.left)
    dy = max(min(point[1], rect.bottom), rect.top)
    return math.hypot(point[0] - dx, point[1] - dy)