# coding: utf-8
import time
import csv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

#////#Initialize#/////##
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)
driver.get("https://campus.icu.ac.jp/public/ehandbook/SearchCourseAndSyllabus.aspx")

#////#Select year#/////##
Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_pnl_japanese").find_elements_by_tag_name("div")[1].find_element_by_id("ctl00_ContentPlaceHolder1_ddl_year_j")).select_by_value("2019")

#getmajorlist func
def getMajorlist():
    return Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddl_major_j"))

#makemajorlist
majordic = []
for major in getMajorlist().options:
    if major.text == "" or "==" in major.text:
        continue
    majordic.append(major.text)

##################circulation###################################
i=0
for majortx in majordic:
    #作業中のメジャー
    print("=major="+majortx+"=major=")

    #ページをリセットして表示
    driver.get("https://campus.icu.ac.jp/public/ehandbook/SearchCourseAndSyllabus.aspx")
    getMajorlist().select_by_visible_text(majortx)

    #検索ボタンを押す
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_btn_search_j").click()

    #テーブルを取得
    table =driver.find_element_by_id("ctl00_ContentPlaceHolder1_grv_course_j")

    pgnum = 0

    f = open(majortx+".csv", 'w', encoding='utf-16')
    writer = csv.writer(f, lineterminator='\n')
    #科目番号	科目タイトル	時間割	担当教員	単位	開講言語	科目概要	シラバス
    writer.writerow(["科目番号","科目タイトル","時間割","担当教員","単位","開講言語","科目概要","シラバス"])

    #選択したメジャー内の捜索
    while(True):
        i = i + 1

        pagenum="Page$"+str(i)

        #ページ番号ボタンを捜索して押す
        try:
            selectnum = driver.find_element_by_xpath("//a[contains(@href,'ctl00$ContentPlaceHolder1$grv_course_j') and contains(@href,'"+pagenum+"')]")
            print("===" + selectnum.text)
            selectnum.click()
        except NoSuchElementException:
            if i!=1:
                i=0
                break
            else:
                print("===1")

        time.sleep(3)

        #授業一覧を取得
        classtable = driver.find_element_by_id("ctl00_ContentPlaceHolder1_grv_course_j").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        ii=0
        for classone in classtable:
            ii = ii + 1
            if (ii <= 2):
                continue
            if ("科目番号" in classone.text):
                continue
            if (len(classtable) == (ii + 2)):
                break
            #csvに記録すべき項目
            tdslist = []
            for intdcontent in classone.find_elements_by_tag_name("td"):
                tdslist.append(intdcontent.text)
            writer.writerow(tdslist)
    f.close()
##################################
