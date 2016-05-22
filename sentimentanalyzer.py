import web

import get_twitter_data

import naive_bayes_classifier
import json, logging, html_helper

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        query = web.ctx.get('query')
        html = html_helper.HTMLHelper()
        twitterData = get_twitter_data.TwitterData()
        if query:
            if(query[0] == '?'):
                query = query[1:]
            arr = query.split('&')
            logging.warning(arr)
            
            #default values
            time = 'daily'

            for item in arr:
                if 'keyword' in item:
                    keyword = item.split('=')[1]
                elif 'time' in item:
                    time = item.split('=')[1]
            #end loop
                            
            
            tweets = twitterData.getTwitterData(keyword, time)
            if(tweets):
                trainingDataFile = 'fulltrainingdataset-csv.csv'               
                #classifierDumpFile = 'data/naivebayes_trained_model.pickle'
                classifierDumpFile = 'my_final_classifier2.pickle'
                trainingRequired = 0
                nb = naive_bayes_classifier.NaiveBayesClassifier(tweets, keyword, time, \
                                              trainingDataFile, classifierDumpFile, trainingRequired)
                nb.classify()
                #nb.main()#added for testing
                #nb.accuracy()
                return nb.getHTML()
            else:
                return html.getDefaultHTML(error=1)
        else:
            return html.getDefaultHTML()

if __name__ == "__main__":
    web.ctx.default_bind_address = '127.0.0.1:9000'
    app = web.application(urls, globals())
    #web.config.default_port = 8090
    #app.run()
    web.httpserver.runsimple(app.wsgifunc(), ("127.0.0.1", 8001))
