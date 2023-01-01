import requests
from bs4 import BeautifulSoup
import smtplib
from account import *  # headers, FROM_ADDRESS, TO_ADDRESS, EMAIL_PASSWORD 변수를 저장한 파일입니다.
from email.message import EmailMessage

def setup(url):
    res = requests.get(url, headers=headers)    # User-Agent
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def today_weather():
    aaa = []
    aaa.append("[오늘의 날씨]\n")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=0&acr=1&acq=%EB%82%A0%E3%85%86&qdt=0&ie=utf8&query=%EB%82%A0%EC%94%A8"
    soup = setup(url)
    cast = soup.find("div", attrs={"class":"temperature_text"}).get_text().strip().replace("온도", "온도 : ")
    cast_detail = soup.find("p", attrs={"class":"summary"}).get_text().strip().replace("요  ", "요, ")
    temperature_inner = soup.find("span", attrs={"class":"temperature_inner"}).get_text().strip().replace("온", "온 ")
    weather_left = soup.find_all("span", attrs={"class":"weather_left"})
    morning_rain = weather_left[0].get_text().strip()
    afternoon_rain = weather_left[1].get_text().strip()
    today_chart_list = soup.find("ul", attrs={"class":"today_chart_list"}).find_all("li")
    list1 = today_chart_list[0].get_text().strip()
    list2 = today_chart_list[1].get_text().strip()
    list3 = today_chart_list[2].get_text().strip()
    aaa.append("{} ({})\n".format(cast, cast_detail))
    aaa.append(temperature_inner)
    aaa.append("\n강수량 : {} / {}\n".format(morning_rain, afternoon_rain))
    aaa.append("{} / {} / {}\n".format(list1, list2, list3))
    return "".join(aaa)

def today_news():
    aaa1 = today_politics()
    aaa2 = today_business()
    aaa3 = today_it_science()
    reaaa = []
    reaaa.append("\n[오늘의 정치 뉴스]\n")
    for a in aaa1:
        reaaa.append(a)
    reaaa.append("\n[오늘의 경제 뉴스]\n")
    for a in aaa2:
        reaaa.append(a)
    reaaa.append("\n[오늘의 IT/과학 뉴스]\n")
    for a in aaa3:
        reaaa.append(a)
    return "".join(reaaa)

def news_scrape(url):
    aaa = []
    soup = setup(url)
    cluster = soup.find("div", attrs={"class":"_persist"}).find_all("div", attrs={"class":"cluster_group _cluster_content"}, limit=5)
    for index, news in enumerate(cluster):
        title = news.find("div", attrs={"class":"cluster_text"}).find("a").get_text().strip()
        link = news.find("div", attrs={"class":"cluster_text"}).find("a")["href"]
        aaa.append("{}) {}\n(링크 : {})\n".format(index+1, title, link))
    return aaa

def today_politics():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
    aaa = news_scrape(url)
    return aaa

def today_business():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"
    aaa = news_scrape(url)
    return aaa

def today_it_science():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"
    aaa = news_scrape(url)
    return aaa

def set_content():
    relist=[]
    relist.append(today_weather())
    relist.append(today_news())
    return "".join(relist)

def sendmail():
    msg = EmailMessage()
    content = set_content()
    msg["Subject"] = "SecretaryService"
    msg["From"] = FROM_ADDRESS # 보내는 사람
    msg["To"] = TO_ADDRESS # 받는 사람

    msg.set_content(content)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(FROM_ADDRESS, EMAIL_PASSWORD)  # 앱 비밀번호
        smtp.send_message(msg)

if __name__ == "__main__":
    sendmail()