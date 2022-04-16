import geom_lib as geom
#
# Game loop
#
# Criar objeto:
player=geom.GABARITO_OBJETO.copy()

# Mover objeto:
retorno = geom.mover(player,'cima')
if not retorno:
    print('erro')