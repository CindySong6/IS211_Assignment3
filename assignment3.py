import argparse
# other imports go here
import urllib.request
import csv
import io
import re

'''
Open the file and process it's contents in memory for later processing
2. Search for all hits that are images (using a regular expression) and gather some stats on those
images
image format [jpeg, png, jpg, gif] lower and upper
3. Find out which is the most popular browser people use to go to this website
'''

def downloadData(url):
    '''
    download the file from url
    '''
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')
    return response


def processData(data):
    '''
    store the data to a list of dictionary each with the keys:
    path to file, datetime accessed, browser, status of request, request size in bytes
    '''
    csv_data = csv.reader(io.StringIO(data))
    output_data = []
    for row in csv_data:
        #process each row into a dictionary
        output_data.append({'path_to_file': row[0],
                            'datetime_accessed': row[1],
                            'browser': row[2],
                            'request_status': row[3],
                            'size': row[4]
        })
    return output_data


def searchImageHits(data_list):
    '''
    find out how many percent of the hits are image
    match any png, gif, jpg, jpeg files
    '''
    image_hit = 0
    total_hit = 0

    # iterate through each dictionary and look for the 'path_to_file' value matches the with image format
    # pattern is case-insensitive
    # find total image hits
    for hit in data_list:
        total_hit += 1
        if re.search(r'(png|jpe{0,1}g|gif)$', hit['path_to_file'], re.I):
            image_hit += 1

    # find percentage of image hits over total hits
    hit_percentage = round(image_hit/total_hit*100, 2)
    
    # print results
    print("Image requests account for {}% of all requests!".format(hit_percentage))


def findMostPopularBrowser(data_list):
    '''
    Find out which is the most popular browser people use to go to this website
    '''
    # a dictionary to hold the counts of each browser use
    browsers_count = {'Firefox':0,
                     'Chrome': 0,
                     'Internet Explorer':0,
                     'Safari': 0
                    }

    # patterns for Firefox, Chrome, Internet Explorer, Safari browsers
    # avoid counting chromeframe
    pattern= re.compile(r'(Firefox|Chrome|Internet explorer|Safari)/')

    # iterate through data_list and search for the browser used for each hit
    for hit in data_list:
        browser = pattern.search(hit['browser'])
        if browser:
            browser = browser.group(1)
            browsers_count[browser] += 1

    # find the maximum used browser and it's count from the browsers_count dictionary
    most_popular_browser = max(browsers_count, key=browsers_count.get)
    num_of_times_used = browsers_count[most_popular_browser]

    # print the result
    print("The most popular browser is {} with {} use!".format(most_popular_browser, num_of_times_used))


def main(url):
    print(f"Running main with URL = {url}...")
    # download the file from url
    url_data = downloadData(url)
    # process the data
    output_data = processData(url_data)
    # find percentage of images hits
    searchImageHits(output_data)
    #find most used broser
    findMostPopularBrowser(output_data)
    


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
