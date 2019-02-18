import codecs
import os
import urllib
import threading

class DownloadImgs(object):
    def __init__(self, img_urls_file, thread_num=8):
        self.img_urls_file = img_urls_file
        self.fold_name = self.img_urls_file.split("/")[-1].split(".")[0]
        self.__get_img_urls_list()
        if not os.path.exists("./"+self.fold_name):
            os.mkdir("./"+self.fold_name)
        self.thread_num = thread_num

    def __get_img_urls_list(self):
        with codecs.open(self.img_urls_file, 'r') as fread:
            self.img_urls = [i.strip() for i in fread.readlines()]
            self.imgs_num = len(self.img_urls)

    def __download_img(self, thread_id):
        thread_url_list = []
        for index, img_url in enumerate(self.img_urls):
            if index % thread_id == 0:
                thread_url_list.append(img_url)
        for img_url in thread_url_list:
            try:
                save_path = os.path.join("./"+self.fold_name, img_url.split("/")[-1])
                print "img_url: {0}, save_path: {1}".format(img_url, save_path)
                urllib.urlretrieve(img_url, save_path)
            except Exception as e:
                print "e: {0}".format(e.message)
                continue

    def fit(self):
        for i in range(self.thread_num):
            t = threading.Thread(target=self.__download_img, args=(i,))
            t.start()

if __name__ == "__main__":
    download_imgs = DownloadImgs("../raw_data/age_college/urls_age_college.txt",20)
    download_imgs.fit()
