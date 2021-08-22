import websocket, json, pprint, talib, numpy

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIODO = 14
RSI_SOBRECOMPRA = 70
RSI_SOBREVENTA = 30
SIMBOLO_TRADE = 'ETHUSD'
CANTIDAD_TRADE = 0.008

cierres = []
en_posicion = False

def on_open(ws):
    print('Conexion abierta')

def on_close(ws):
    print('Conexion cerrada')

def on_message(ws, message):
    global cierres
    print('Mensaje recibido')
    json_mensaje = json.loads(message)
    pprint.pprint(json_mensaje)

    vela = json_mensaje['k']
    esta_cerrada = vela['x']
    cierre = vela['c']

    if esta_cerrada:
        print('La vela se ha cerrado a {}'.format(cierre))
        cierres.append(float(cierre))
        print('Velas cerradas')
        print(cierres)

        if len(cierres) > RSI_PERIODO:
            np_cierres = numpy.array(cierres)
            rsi = talib.RSI(np_cierres)
            print("Todos los cierres calculados hasta el momento:")
            print(rsi)

            '''El indice -1 en python es para empezar a guardar desde
            la ultima posicion del array'''

            ultimo_rsi = rsi[-1]
            print("El rsi actual es {}".format(ultimo_rsi))

        if ultimo_rsi > RSI_SOBRECOMPRA:
            if en_posicion:
                print("Vende vende vende!!!")
                #Vender en binance aqui
            else:
                print("Esta en sobrecompra, pero no tenemos nada. Nada que hacer")
        
        if ultimo_rsi < RSI_SOBREVENTA:
            if en_posicion:
                print("Esta en sobreventa, pero ya has comprado. Nada que hacer")
            else:
                print("Compra compra compra")
                #Comprar en binance aqui


        

    

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()