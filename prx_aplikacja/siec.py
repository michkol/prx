import timeit
import socket

def ping(ip, port):
    pingi = []

    for i in range(2):
        try:
            czas_poczatkowy = timeit.default_timer()
            gniazdo = socket.create_connection((ip, port), 5)
            czas_koncowy = timeit.default_timer()

            gniazdo.close
            pingi.append((czas_koncowy - czas_poczatkowy) * 1000);
        except OSError:
            pass

    if len(pingi) > 0:
        return min(pingi)
    else:
        return None
