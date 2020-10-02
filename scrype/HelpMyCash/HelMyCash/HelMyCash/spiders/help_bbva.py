
import scrapy
from collections import Counter
# title = //h1[@class="mt-xs-5 mt-md-0"]/text()
# qualification = //span[@class="font-weight-bold"]/text() | //p[@class="lead mt-2"]/text()
# description = //div[@class="card card-sheet-point card-border-top-secondary"]//p[not (@class)]/text() | //div[@class="card-body"]//li/text()

# title_opinion = //div[@class="card card-review-list mb-4 "]//a/text()
# user_description = //div[@class="card-text my-3 mt-sm-0 px-0 px-sm-4"]/text()
# review = response.xpath('//div//i[contains(@class, "fa fa-star active")]/@class').extract_first().replace('fa fa-star ','')

class SpiderBBVA(scrapy.Spider):
    name = 'HelpMyCash'
    start_urls =[
        'https://www.helpmycash.com/opiniones/banco/bbva/'
    ]

    custom_settings = {
        'FEED_URI':'HelpMyCash.json',
        'FEED_FORMAT':'json',
        'CONCURRENT_REQUESTS':24,
        'USER_AGENT':'DataTeam',
        'FEED_EXPORT_ENCODING':'utf-8'
    }

    def parse(self, response):
        try:
            if response.status == 200:
                title = response.xpath('//h1[@class="mt-xs-5 mt-md-0"]/text()').get()
                qualification = response.xpath('//span[@class="font-weight-bold"]/text() | //p[@class="lead mt-2"]/text()').getall()
                description = response.xpath('//div[@class="card card-sheet-point card-border-top-secondary"]//p[not (@class)]/text() | //div[@class="card-body"]//li/text()').getall()

                title_opinion = response.xpath('//div[@class="card card-review-list mb-4 "]//a/text()').getall()
                user_description = response.xpath('//div[@class="card card-review-list mb-4 "]//div[@class="card-text my-3 mt-sm-0 px-0 px-sm-4"]/text()').getall()
                review = response.xpath('//div[@class="card card-review-list mb-4 "]//i[contains(@class, "fa fa-star ")]/@class').getall()

                # Convertimos los elementos en 1 si tiene una estrella, 0 si no tiene estrella
                for x in range(0,len(review)):
                    if review[x] == 'fa fa-star active':
                        review[x] = 1
                    elif review[x] =='fa fa-star ':
                        review[x] = 0
                print(review[:-1])

                # Creamos una sublista para separar los elementos en una longitud de 5
                # 5 es la longitud por que se califica de 1 a 5 estrellas
                sublista = []
                for i in range(0,len(review[:-1]),5):
                    sublista.append(review[:-1][i:i+5])
                print(sublista)

                #convertimos la sublista en una lista, extrayendo solo el elemento numero en la posición 0
                contador = 0
                lista_review = []
                for j in sublista:
                    contador +=1
                    if 1 in j:
                        stars = Counter(j).values()
                        review = list(stars).pop(0)
                        lista_review.append(review)
                
                yield {
                    'title' : title,
                    'qualification': qualification,
                    'description': description,
                    'title_opinion': title_opinion,
                    'user_description': user_description,
                    'review': lista_review
                }

            else:
                raise ValueError(f'Error {response.status_code}')

        except ValueError as e:
            print(e)        


if __name__ == '__main__':
    SpiderBBVA.parse()