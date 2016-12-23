import logging
import traceback
import urllib2
from cookielib import CookieJar
import validators
from flask_restplus import Resource
from flask_restplus import abort
from flask_restplus import fields

import utils
from flask_restplus import Api

rest_api = Api(version='1.0', title='reducto-api', description='Basic Services')

log = logging.getLogger(__name__)
@rest_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    return {'message': message}, 500


summarize = rest_api.namespace('summarize', description='Summarize Operations')
parser = summarize.parser()
parser.add_argument('url', type=str, help='url for summery and images')

summary = rest_api.model('ScrapingResults', {
    'images': fields.List(fields.String(description='Urls to images for site')),
    'summary': fields.String(required=True, description='summary for article'),
    'website': fields.String(required=True, description='summary for article'),
    'title': fields.String(required=True, description='summary for article')
})

@summarize.route('/summarize')
class Summarize(Resource):
    @summarize.marshal_with(summary)
    @summarize.expect(parser)
    def get(self):
        args = parser.parse_args()
        if not(args.url.startswith('http') | args.url.startswith('https')):
            args.url = 'http://'+args.url

        if validators.url(args.url) is not True:
            abort(400, "Provided URL Is Invalid")

        # Step 2 load content:
        try:
            # TODO: allow for https redirects
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')]

            data = opener.open(args.url).read()

            splits = args.url.split('//')[1].split('.')
            website_title = 'unknown'
            if splits[0] == 'www':
                website_title = splits[1]
            else:
                website_title = splits[0]
            website_title = website_title.upper()
            raw_text = utils.obtain_text(data)
            # raw_summery = utils.summarize_text(raw_text[:10],4)
            return {'title': utils.obtain_title(data).encode('ascii', 'ignore'),
             'images': utils.obtain_images(data),
             'summary': " ".join(raw_text[:3]).encode('ascii', 'ignore'),
             'website': website_title}
        except Exception as err:
            print err.message
            abort(500, err.message)




