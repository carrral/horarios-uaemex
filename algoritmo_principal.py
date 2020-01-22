import copy
from horarios import horarios_compatibles, HorarioClase, HorarioMaestro

def recursivo(L: list, C: list, Z: list, w: int):
    if not C:

        # C vacío
        # Fin de la ejecución
        return True

    else:
        Hk = C.pop()

        for hi in Hk:
            Lc = copy.deepcopy(L)
            if horarios_compatibles(Lc,hi):
                Lc.merge(hi)

                if Lc.len == w:
                    Z.append(Lc)

                else:
                    recursivo(Lc, C, Z, w)

def principal_semilla(C:list, S: HorarioClase, w: int):

    L = HorarioMaestro("Horario")
    L.merge(S)

    Z = list()

    if w != 1:
        recursivo(L, C, Z, w)

    else:
        Z.append(L)

    return Z

def principal(C: list, w: int):
    Hk = C.pop()
    Z = list()

    for Si in Hk:
        Ci = copy.deepcopy(C)
        z = principal_semilla(Ci,Si,w)
        Z = Z+z

    return Z

