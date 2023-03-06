import MetaTrader5 as mt5

ACCOUNT = {
        "login": 5010193829,
        "password": "ce1ymkmh",
        "server": "MetaQuotes-Demo"
    }

def login(loginid, loginpass, nameserver):
    try:
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()

        authorized = mt5.login(loginid, password=loginpass, server= nameserver)
        if authorized:
            return True
        else:
            print("failed to try again connect at account #{}, error code: {}".format(loginid, mt5.last_error()))
            return False
    except Exception as error:
        print(error)
        return False