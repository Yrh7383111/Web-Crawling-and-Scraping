from scrapy import Spider
from scrapy.http import Request


class ClassCenterSpider(Spider):
    name = 'Class_Center'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']

    # Constructor
    def __init__(self, subject=None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject

    # Parsing function
    def parse(self, response, **kwargs):
        ul = response.xpath('//body/div[1]/section[2]/ul[1]')
        lis = ul.xpath('./li')

        if self.subject:
            relative_subject_link = lis.xpath('./h3/a[contains(@title, "' + self.subject + '")]/@href').extract_first()
            subject_link = response.urljoin(relative_subject_link)
            yield Request(url=subject_link, callback=parse_subject)
        else:
            for li in lis:
                relative_subject_link = li.xpath('./h3/a[1]/@href').extract_first()
                subject_link = response.urljoin(relative_subject_link)
                yield Request(url=subject_link, callback=parse_subject)


# Parse each subject
def parse_subject(response):
    table = response.xpath('//table[@id="subjectstablelist"]')
    body = table.xpath('./tbody')
    rows = body.xpath('./tr[@itemtype="http://schema.org/Event"]')

    for row in rows:
        # Subject
        subject = response.xpath('//header/div[1]/div[1]/div[2]/h1[1]/text()').extract_first()
        subject = subject.replace(' Courses', '')

        # Course name
        course_name = row.xpath('./td[2]')
        base_link = 'https://www.classcentral.com'

        institution_name = course_name.xpath('./div[1]/a[1]/text()').extract_first()
        if institution_name:
            institution_name = institution_name.strip()
        else:
            institution_name = 'None'

        institution_link = course_name.xpath('./div[1]/a[1]/@href').extract_first()
        if institution_link:
            institution_link = base_link + institution_link
        else:
            institution_link = 'None'

        course_title = course_name.xpath('.//span[@itemprop="name"]/text()').extract_first()
        if course_title:
            course_title = course_title.strip()
        else:
            course_title = 'None'

        course_link = course_name.xpath('.//a[@itemprop="url"]/@href').extract_first()
        if course_link:
            course_link = base_link + course_link
        else:
            course_link = 'None'

        provider_name = course_name.xpath('.//a[contains(@class, "italic")]/text()').extract_first()
        if provider_name:
            provider_name = provider_name.rstrip()
        else:
            provider_name = 'None'

        provider_link = course_name.xpath('.//a[contains(@class, "italic")]/@href').extract_first()
        if provider_link:
            provider_link = base_link + provider_link
        else:
            provider_link = 'None'

        course_duration = course_name.xpath('./div[2]/span[1]/span[2]/text()').extract_first()
        if course_duration:
            course_duration = course_duration.strip().replace(',', '').split()
            course_duration = ' '.join(course_duration)
        else:
            course_duration = 'None'

        # Start date
        start_date = row.xpath('./td[3]')
        date = start_date.xpath('./text()').extract_first()
        if date:
            date = date.strip()
        else:
            date = 'None'

        # Rating
        rating = row.xpath('./td[4]')
        star = rating.xpath('./@data-timestamp').extract_first()
        if star:
            pass
        else:
            star = '0'

        reviews = rating.xpath('./div[1]/div[1]/span[3]/text()').extract_first()
        if reviews:
            reviews = reviews.strip()
        else:
            reviews = '0 Reviews'

        yield {'Subject': subject,
               'Institution Name': institution_name, 'Institution Link': institution_link,
               'Course Title': course_title, 'Course Link': course_link,
               'Provider Name': provider_name,
               'Provider Link': provider_link,
               'Course Duration': course_duration,
               'Start Date': date,
               'Rating': star,
               'Reviews': reviews}

    # Next page
    relative_next_page_link = response.xpath('.//link[@rel="next"]/@href').extract_first()
    if relative_next_page_link:
        next_page_link = response.urljoin(relative_next_page_link)
        yield Request(url=next_page_link, callback=parse_subject)
