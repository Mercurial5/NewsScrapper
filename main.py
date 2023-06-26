from openpyxl.workbook import Workbook

from scrapper import Scrapper

QUERIES = ['АЭС', 'Строительство АЭС', 'Буденовскоgе', 'Добыча урана']
COUNTRIES = [
    {'hl': 'ru', 'gl': 'RU', 'ceid': 'RU:ru'},
]


def main():
    workbook = Workbook()
    sheet = workbook.active

    scrapper = Scrapper(QUERIES, COUNTRIES)
    for article in scrapper.articles():
        row = [article.url, article.title, ' '.join(article.keywords)]
        sheet.append(row)

    workbook.save('result.xlsx')


if __name__ == '__main__':
    main()
