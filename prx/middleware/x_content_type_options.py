class XContentTypeOptions():
    def process_response(self, zadanie, odpowiedz):
        odpowiedz['X-Content-Type-Options'] = 'nosniff'
        return odpowiedz
