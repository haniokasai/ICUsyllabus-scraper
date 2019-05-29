# coding: utf-8
#https://campus.icu.ac.jp/icumap/ehb/SearchCO.aspx
import time
import configparser
import sqlite3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


##settings.ini にuser名とパスワードを入力してください。gluegentにしかパスワードを送信しないことは明らか。
##[conf]
##username = ユーザー名
##passwd = パスワード
CONFIG_FILE = "settings.ini"

##conf
year = "2019"
tablename = "Spring2019"
dbfilename = "syllabus2019_t2.db"

#ini
conf = configparser.SafeConfigParser()
conf.read(CONFIG_FILE)
username = conf.get("conf","username")
passwd = conf.get("conf","passwd")


#sqlite
########mk sqlite
conn = sqlite3.connect(dbfilename)
c = conn.cursor()
c.execute("CREATE TABLE "+tablename+"('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'rgno' TEXT,'season' TEXT,'csno' TEXT,'lang' TEXT,'etitle' TEXT,'jtitle' TEXT,'schedule' TEXT,'room' TEXT,'instructor' TEXT,'unit' TEXT,'schedule_string' TEXT,'s11' INTEGER,'s12' INTEGER,'s13' INTEGER,'s14' INTEGER,'s15' INTEGER,'s16' INTEGER,'s21' INTEGER,'s22' INTEGER,'s23' INTEGER,'s24' INTEGER,'s25' INTEGER,'s26' INTEGER,'s31' INTEGER,'s32' INTEGER,'s33' INTEGER,'s34' INTEGER,'s35' INTEGER,'s36' INTEGER,'s41' INTEGER,'s42' INTEGER,'s43' INTEGER,'s44' INTEGER,'s45' INTEGER,'s46' INTEGER,'s51' INTEGER,'s52' INTEGER,'s53' INTEGER,'s54' INTEGER,'s55' INTEGER,'s56' INTEGER,'s61' INTEGER,'s62' INTEGER,'s63' INTEGER,'s64' INTEGER,'s65' INTEGER,'s66' INTEGER,'s71' INTEGER,'s72' INTEGER,'s73' INTEGER,'s74' INTEGER,'s75' INTEGER,'s76' INTEGER,'s81' INTEGER,'s82' INTEGER,'s83' INTEGER,'s84' INTEGER,'s85' INTEGER,'s86' INTEGER,'s91' INTEGER,'s92' INTEGER,'s93' INTEGER,'s94' INTEGER,'s95' INTEGER,'s96' INTEGER)")
conn.commit()

######
#////#Initialize#/////##
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)
driver.get("https://campus.icu.ac.jp/icumap/ehb/SearchCO.aspx")
time.sleep(1)
print(driver.current_url)
driver.find_element_by_id("username_input").send_keys(username)
driver.find_element_by_id("password_input").send_keys(passwd)
driver.find_element_by_id("login_button").click()
time.sleep(1)
print(driver.current_url)

Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddl_year")).select_by_value(year)
Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlPageSize")).select_by_value("50")
driver.find_element_by_id("ctl00_ContentPlaceHolder1_btn_search").click()

i=0
# 選択したメジャー内の捜索
while (True):
    i = i + 1

    pagenum = "Page$" + str(i)
    if i!=1:
     try:
         #<a href="javascript:__doPostBack('ctl00$ContentPlaceHolder1$grv_course','Page$2')">2</a>
         selectnum = driver.find_element_by_xpath(
             "//a[contains(@href,'ctl00$ContentPlaceHolder1$grv_course') and contains(@href,'" + pagenum + "')]")
         print("===" + selectnum.text)
         selectnum.click()
     except NoSuchElementException:
         if i != 1:
             i = 0
             break
    else:
        print("===1")


    time.sleep(1)

    classtable = driver.find_element_by_id("ctl00_ContentPlaceHolder1_grv_course").find_element_by_tag_name(
        "tbody").find_elements_by_tag_name("tr")

    # sql文
    execstring = "insert into " + tablename + " (rgno, season, csno, lang, etitle, jtitle, schedule, room, instructor, unit) values (?,?,?,?,?,?,?,?,?,?)"
    print(execstring)

    ii = 0
    for classone in classtable:
        ii = ii + 1
        if (ii <= 2):
            continue
        if (len(classtable) == (ii + 1)):
            break

                ##!!['10117\nSpring\n2019\n[change]\n2019/02/25', 'ELA074', 'E', 'A', 'Advanced English Studies: IELTS\n上級総合英語：IELTS\n1/W,1/F\nH-252', '', 'SMITH, Nicholas W.', '2']
        #('id' ,'rgno' ,'season' ,'csno' ,'lang','etitle' ,'jtitle' ,'schedule' ,'room' ,'instructor' ,'unit' ,'schedule_string'
        t_rgno = classone.find_element_by_xpath("td/div/span[contains(@id,'_rgno')]").text
        t_season = classone.find_element_by_xpath("td/div/span[contains(@id,'_season')]").text
        t_csno = classone.find_element_by_xpath("td/div/span[contains(@id,'_course_no')]").text
        t_lang = classone.find_element_by_xpath("td/div/span[contains(@id,'_lang')]").text
        t_etitle = classone.find_element_by_xpath("td/div/span[contains(@id,'_title_e')]").text
        t_jtitle = classone.find_element_by_xpath("td/div/span[contains(@id,'_title_j')]").text
        t_room = classone.find_element_by_xpath("td/div/span[contains(@id,'_room')]").text
        t_schedule = classone.find_element_by_xpath("td/div/span[contains(@id,'_schedule')]").text
        t_instructor = classone.find_element_by_xpath("td/div/span[contains(@id,'_instructor')]").text
        t_unit = classone.find_element_by_xpath("td/div/span[contains(@id,'_unit')]").text
        li = (t_rgno, t_season, t_csno, t_lang, t_etitle, t_jtitle,t_schedule, t_room, t_instructor, t_unit)
        print(str(li))

        c.execute(execstring, li)
    conn.commit()
#ログアウト
#https://auth.gluegent.net/sso/logout.cgi?logout=true
driver.get("https://auth.gluegent.net/sso/logout.cgi?logout=true")

#SQL終了
conn.commit()
conn.close()