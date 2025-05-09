import time  # time 모듈을 임포트하여 sleep 기능을 사용.
import re
from selenium import webdriver  # Selenium 패키지에서 webdriver 모듈을 임포트.
from selenium.webdriver.chrome.options import Options  # Chrome 옵션을 설정하기 위해 Options 모듈을 임포트.
from selenium.webdriver.common.by import By

# 전체 화면 캡처 기능을 정의하는 함수
def full_screenshot(category,title,post_date,post_url,count):
    
    for i in range(count):
    
        output_path = "/Users/cyoonlee.KOREANAIR/output/" +post_date[i]+"_"+category[i]+"_"+title[i]+".png"
        
        driver.get(post_url[i])  # 지정된 URL을 웹드라이버에서 열기.
        time.sleep(3)  # 페이지가 로드되기를 기다리기 위해 2초 동안 대기.

        # 창 사이즈 구하기
        driver.get_window_size() 
        
        # Body Tag의 Full Size 가로/세로 구하기 
        w = driver.execute_script('return document.body.parentNode.scrollWidth')
        h = driver.execute_script('return document.body.parentNode.scrollHeight')
            
        # 위에서 구한 가로/세로 사이즈 적용
        driver.set_window_size(w, h)

        time.sleep(2)  # 2초 동안 대기.
        driver.save_screenshot(output_path)  # 스크린샷을 지정된 출력 경로에 저장.
        
        print(post_date[i] +" "+category[i] + " 완료")
    

# 로그인 기능 함수
def login(id,url,pw):
    driver.get(url)  # 지정된 URL을 웹드라이버에서 열기.
    time.sleep(2)  # 페이지가 로드되기를 기다리기 위해 2초 동안 대기.
    
    driver.find_element(By.CLASS_NAME, "user_sign_in").click() # 로그인 버튼 클릭
    time.sleep(2)  # 페이지가 로드되기를 기다리기 위해 2초 동안 대기.

    #id 입력(Naver 로그인시 보안 캡챠 내용 피하기 위해 pyperclip 사용)
    driver.find_element(By.ID, "id").click() 
    driver.execute_script(f"document.getElementById('id').value = '{id}';")
    time.sleep(1)
    
    #pw 입력(Naver 로그인시 보안 캡챠 내용 피하기 위해 pyperclip 사용)
    driver.find_element(By.ID, "pw").click() 
    driver.execute_script(f"document.getElementById('pw').value = '{pw}';")
    time.sleep(1)
    
    driver.find_element(By.ID, "log.login").click() # 로그인 버튼 클릭
    time.sleep(2)  # 페이지가 로드되기를 기다리기 위해 2초 동안 대기.
    
    driver.find_element(By.CLASS_NAME, "btn").click() # 등록 버튼 클릭 (if문 처리해야할듯)

# 컨텐츠 내용 불러오기
def page_cursor(driver):
    
    driver.find_element(By.CLASS_NAME, "channel_content_more").click() # 전체 콘텐츠 보기 클릭
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    category, title, post_date, post_url, last_number = [], [], [], [], []
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    link_list = driver.find_elements(By.CLASS_NAME, 'content_item_inner')

    for element in link_list:
        # element.id를 문자열로 변환합니다.
        element_id = str(element.id)  
        # 정규 표현식을 사용하여 마지막 숫자를 추출합니다.
        match = re.search(r'\.e\.(\d+)$', element_id)
        if match:
            last_number.append(match.group(1))
        
    for i in range(len(last_number)):
        category.append(driver.find_element(By.CSS_SELECTOR, "#likeItCountViewDiv > li:nth-child("+str(i+1)+") > div > div > a.content_category").text)
        title.append(driver.find_element(By.CSS_SELECTOR, "#likeItCountViewDiv > li:nth-child("+str(i+1)+") > div > div > a.content_text_link > strong").text)
        post_date.append(driver.find_element(By.CSS_SELECTOR, "#likeItCountViewDiv > li:nth-child("+str(i+1)+") > div > div > div.content_info > div.content_info_inner > span:nth-child(3)").text)
        post_url.append(driver.find_element(By.CSS_SELECTOR, "#likeItCountViewDiv > li:nth-child("+str(i+1)+") > div > a ").get_attribute('href'))
                
        print("순번 : " + str(i+1))
        print("카테고리 : " + category[i])
        print("타이틀틀 : " + title[i])
        print("게시일 : " + post_date[i])
        print("게시URL : " + post_url[i])
    
    return full_screenshot(category,title,post_date,post_url,len(last_number))    
                        
# 헤드리스 모드를 위한 Chrome 옵션 설정.
chrome_options = Options()
chrome_options.add_argument('--headless')

# 지정된 옵션으로 Chrome 웹드라이버 인스턴스를 생성.
driver = webdriver.Chrome(options=chrome_options)

# 스크린샷을 찍을 웹페이지의 URL 및 출력 경로를 설정.
url = "https://contents.premium.naver.com/macroinvesting/macroinvest"
id = "lcy608"
pw = "!Kal02kal"


# Naver Login 함수
login(id,url,pw)

#컨텐츠 URL 수집 & 캡처처
page_cursor(driver)

# 웹드라이버를 닫기.
driver.quit()