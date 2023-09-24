class Cars:
    def __init__(self, model, url, byn, usd, data):
        self.model = model
        self.url = url
        self.byn = byn
        self.usd = usd
        self.data = data

    def get_dict(self):
        return {'model': self.model,
                'url': self.url,
                'byn': self.byn,
                'usd': self.usd,
                'data': self.data}

    def __str__(self):
        return f'{self.model}\n -> {self.url}\n' \
               f'Стоимость: {self.byn} BYN или ~ {self.usd} $\n' \
               f'{self.data}\n'
