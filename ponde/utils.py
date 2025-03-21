def var_assigns(var, score : int):
    if var == None:
        var = score
    else:
        var = (var + score)/ 2

    return var

def numerical_calculator(var, respuestas):
    respuesta_ideal = respuestas['Respuesta ideal']
    respuesta_candidato = respuestas['Respuesta candidato']
    if respuesta_ideal == respuesta_candidato:
        var = var_assigns(var, 100)
    elif respuesta_candidato == 0 and respuesta_ideal > 0:
        var = var_assigns(var, 0)
    else:
        respuesta_diff = abs(respuesta_ideal - respuesta_candidato)
        var = var_assigns(var, max(100 - (respuesta_diff * 15), 0))

    return var