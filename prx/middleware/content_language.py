class ContentLanguage():
    def process_response(self, zadanie, odpowiedz):
        odpowiedz['Content-Language'] = 'pl-pl'
        return odpowiedz
