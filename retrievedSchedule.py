import os
import string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import hashlib

retrieve_url = 'http://tkbkmavnteam.tk'
path = os.path.dirname(os.path.realpath(__file__))

def setupDriverForDownloadMethod(download_path):
    print(download_path)
    options = Options()
    options.add_experimental_option('prefs', {
        'download.default_directory': download_path,
        'download.prompt_for_download': False,
        'safebrowsing.enabled': False,
        'download.directory_upgrade': True,
        'safebrowsing_for_trusted_sources_enabled': False
    })
    return options

def createDriverWithOptions(options):
    driver = webdriver.Chrome(executable_path='{}/chromedriver'.format(path), options=options)
    print('--- Getting the webdriver to scrapping...')
    return driver

def createDriver():
    driver = webdriver.Chrome(executable_path='{}/chromedriver'.format(path))
    print('--- Getting the webdriver to scrapping...')
    return driver

def getUserLoginData():
    username = str(input('Enter your studentID: '))
    password = str(input('Enter your password: '))
    return username, password

def getLoginAsGuest(driver):
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-login/div/div/div[2]/div[4]').click()
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-app-privacy-policy/div/div/div/p/input').click()
    driver.find_element_by_xpath('//*[@id="RoomBoxChat"]/div[1]/div[1]/div[3]').click()
    driver.find_element_by_tag_name('html').send_keys(Keys.END)
    print('--- Logging in as a guest...')

def Await(seconds):
    time.sleep(seconds)

def getLoginUser(driver, username, password):
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-app-privacy-policy/div/div/div/div').click()
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[2]/ul/li[4]/a/img').click()

    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-setting-app/div/div/div/div[2]/form/div[2]/div/input').send_keys(username)
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-setting-app/div/div/div/div[2]/form/div[3]/div/input').send_keys(password)
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-setting-app/div/div/div/div[2]/form/div[4]/button[2]').click()
    print('--- Getting schedule from https://actvn.edu.vn')

def createExcelWriter():
    writer = pd.ExcelWriter('outp.xlsx', engine='xlsxwriter')
    return writer

def setDataFrameDownloaded(df, writer):
    dfs = df[1]
    dfs.to_excel(writer, sheet_name='Sheet1', startcol=3)
    dfs = df[2]
    dfs.to_excel(writer, sheet_name='Sheet1', startcol=8)
    dfs = df[3]
    dfs.to_excel(writer, sheet_name='Sheet1', startrow=8)
    print('--- Got data from original webURL')
    return dfs

def setDataFrame(driver, writer):
    subjects = driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-mainapp/div/div/div[2]/table/tr')
    sublist1 = subjects.find_element_by_xpath('./td[{}]'.format(1)).get_attribute('innerHTML')
    df = pd.read_html(sublist1)
    dfs = df[0]
    dfs.to_excel(writer, sheet_name='Sheet1', startcol=3)

    sublist2 = subjects.find_element_by_xpath('./td[{}]'.format(2)).get_attribute('innerHTML')
    df = pd.read_html(sublist2)
    dfs = df[0]
    dfs.to_excel(writer, sheet_name='Sheet1', startcol=8)

    subjects = driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-mainapp/div/div/div[2]/div').get_attribute('innerHTML')
    df = pd.read_html(subjects)
    dfs = df[0]
    dfs.to_excel(writer, sheet_name='Sheet1', startrow=8)
    print('--- Got data from original webURL')
    return dfs

def settingExcelFile(writer, df):
    book = writer.book
    sheet = writer.sheets['Sheet1']
    wrap_format = book.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})

    d = dict(zip(range(26), list(string.ascii_uppercase)))

    for col in range(3, df.shape[1] + 1):
        excel_header = d[col] + ':' + d[col]
        sheet.set_column(excel_header, 25, wrap_format)
    writer.save()

def DownloadHTMLMethod():
    # Get access key
    username, password = getUserLoginData()
    download_path = path + '/downloads'
    before = os.listdir(download_path)
    # setup download options for Chrome_options
    options = setupDriverForDownloadMethod(download_path)
    # Create WebDriver for Chrome
    driver = createDriverWithOptions(options)
    # Access the webURL
    driver.get(retrieve_url)
    # Get Login as Guest
    getLoginAsGuest(driver)
    print('--- Waiting for Response to accept License...')
    Await(10)
    # Click to get login to URL
    getLoginUser(driver, username, password)
    Await(3)
    writer = createExcelWriter()
    print('--- Downloading HTML file...')
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[2]/ul/li[1]/a/img').click()    # download button clicked
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[4]/div/div[2]/div[1]/div/img').click()         # HTML file download Clicked
    Await(3)
    after = os.listdir(download_path)
    change = set(after) - set(before)
    filename = None
    if len(change) == 1:
        filename = change.pop()

    # ------------- Open HTML file downloaded above -------------
    html_file = download_path + '/' + filename
    f = open(html_file, 'r')
    content = f.read()
    f.close()

    df = pd.read_html(content)
    dfs = setDataFrameDownloaded(df, writer)
    driver.close()
    settingExcelFile(writer, dfs)
    print('--- Saved into outp.xlsx file successfully!')

def DownloadImage():
    username, password = getUserLoginData()
    download_path = path + '/image'
    before = os.listdir(download_path)
    options = setupDriverForDownloadMethod(download_path)
    driver = createDriverWithOptions(options)
    driver.get(retrieve_url)
    getLoginAsGuest(driver)
    print('--- Waiting for Response to accept License...')
    Await(10)
    getLoginUser(driver, username, password)
    Await(3)
    print('--- Downloading Image...')
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[2]/ul/li[1]/a/img').click()
    driver.find_element_by_xpath('/html/body/div[2]/app-root/div[4]/div/div[2]/div[2]/div/img').click()
    Await(3)
    after = os.listdir(download_path)
    change = set(after) - set(before)
    filename = None
    if len(change) == 1:
        filename = change.pop()
    print('--- Saved into image named {}'.format(filename))

def WebScrappingMethod():
    username, password = getUserLoginData()
    driver = createDriver()
    driver.get(retrieve_url)
    getLoginAsGuest(driver)
    print('--- Waiting for Response to accept License...')
    Await(10)
    getLoginUser(driver, username, password)
    Await(3)
    writer = createExcelWriter()
    dfs = setDataFrame(driver, writer)
    driver.close()
    settingExcelFile(writer, dfs)
    print('--- Saved into outp.xlsx file successfully!')

def main():
    print('-- 1. Download HTML file --')
    print('-- 2. Download Image --')
    print('-- 3. Web scrapping --')
    choice = int(input('Choose a method from above: '))
    if choice == 1:
        DownloadHTMLMethod()
    elif choice == 2:
        DownloadImage()
    else:
        WebScrappingMethod()

if __name__ == '__main__':
    main()