#coding = utf-8
import re
import json
from multiprocessing import Pool
from selenium import webdriver
import time


def get_one_page(url):
	option = webdriver.ChromeOptions()
	option.add_argument("headless")
	browser = webdriver.Chrome(chrome_options=option)
	browser.get(url)
	return browser.page_source

def parse_one_page(html):
	pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?alt="(.*?)".*?class="star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?"integer">(.*?)<.*?"fraction">(.*?)</i>.*?</dd>',re.S)

	items = re.findall(pattern,html)

	for item in items:
		yield{
			  "index":item[0].strip(),
			  "image": item[1].strip(),
			  "title":item[2].strip(),
			  "actor":item[3].strip()[3:],
			  "time":item[4].strip()[5:],
			  "score":item[5]+item[6]
		}

def write_to_file(content,filename):
	with open(filename,'a',encoding='UTF-8') as file:
		file.write(json.dumps(content,ensure_ascii=False)+'\n')
		file.close()
def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    #print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item,"Results\\MaoYanTop100MP.txt")


if __name__ == '__main__':
	start_time = time.time()
	pool = Pool()
	pool.map(main,[i*10 for i in range(10)])
	pool.close()
	pool.join()
	elapsed = (time.time()-start_time)
	print("RuningTime:", elapsed, "s")