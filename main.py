from src.graphtec_scraper import Graphtec_Scraper
import time

# example use-case
if __name__ == '__main__':
    # URL
    GRAPHTEC_URL = 'http://169.254.0.1'

    # initiate graphtec scraper instance
    graphtec = Graphtec_Scraper(GRAPHTEC_URL)

    try:
        # Open
        graphtec.openBrowser()
        # navigate
        graphtec.navigateToData()
        
        # get 10 data sets
        for i in range(10):
            print(graphtec.getTemp())
            time.sleep(1)
    except:
        print('Something happened')

    # Close
    graphtec.closeBrowser()