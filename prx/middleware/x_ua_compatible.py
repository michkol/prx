class XUACompatible():
    def process_response(self, zadanie, odpowiedz):
        odpowiedz['X-UA-Compatible'] = 'IE=9'
        return odpowiedz
