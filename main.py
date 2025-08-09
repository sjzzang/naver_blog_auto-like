# 필요한 라이브러리를 가져옵니다.
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def naver_blog_macro():
    """
    네이버 블로그 이웃새글에 공감 및 삭제 매크로를 실행하는 함수입니다.
    """
    print("네이버 블로그 매크로를 시작합니다.")

    # ChromeDriver를 자동으로 설치 및 설정합니다.
    chromedriver_autoinstaller.install()

    # Chrome WebDriver를 설정합니다.
    driver = webdriver.Chrome()

    try:
        # 네이버 블로그 홈으로 이동합니다.
        print("네이버 블로그 홈으로 이동 중...")
        driver.get("https://blog.naver.com")

        # 사용자가 로그인할 시간을 줍니다.
        print("로그인이 필요합니다. 30초 안에 로그인 해주세요.")
        time.sleep(15)  # 사용자가 로그인할 수 있도록 30초 대기

        # 로그인 후 이웃새글 섹션이 나타날 때까지 기다립니다.
        print("로그인 중...")
        try:
            # 이웃새글 섹션의 부모 요소를 찾을 때까지 최대 10초 대기합니다.
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.list_post_article'))
            )
            print("로그인이 완료되었습니다. 이웃새글 섹션이 확인되었습니다. 매크로를 시작합니다.")
        except TimeoutException:
            print("이웃새글 섹션을 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다.")
            return

        while True:
            # 페이지의 첫 번째 게시물을 찾습니다.
            try:
                try:
                    # 팝업 닫기 버튼을 찾습니다.
                    close_button = driver.find_element(By.CSS_SELECTOR, 'button[data-role="expansionClose"]')
                    close_button.click()
                    print("팝업창을 닫았습니다.")
                    time.sleep(1)  # 팝업이 닫힐 시간을 줍니다.
                except NoSuchElementException:
                    print("팝업창이 없습니다.")
                    pass  # 팝업이 없으면 무시하고 계속 진행
                # `posts` 리스트를 매번 새로 찾아서 Stale Element 오류를 방지합니다.
                posts = driver.find_elements(By.CSS_SELECTOR, '.list_post_article .item')

                if not posts:
                    print("더 이상 처리할 게시물이 없습니다. 1분 후 다시 확인합니다.")
                    time.sleep(10)
                    continue

                # 첫 번째 게시물을 처리합니다.
                post_to_process = posts[0]

                try:
                    # 게시물 내의 '공감' 버튼을 찾습니다.
                    like_button = post_to_process.find_element(By.CSS_SELECTOR, '.u_likeit_list_btn._button.off')
                    print("공감 버튼을 클릭합니다.")
                    like_button.click()
                    time.sleep(0.3)  # 공감 처리 대기

                    # 게시물 내의 '숨기기' (X) 버튼을 찾습니다.
                    hide_button = post_to_process.find_element(By.CSS_SELECTOR, '.button_del_post')
                    print("게시물 숨기기(X) 버튼을 클릭합니다.")
                    hide_button.click()
                    time.sleep(0.3)  # 숨기기 처리 대기

                    print("게시물 처리가 완료되었습니다. 다음 게시물을 처리합니다.")

                except NoSuchElementException:
                    # '공감' 또는 '숨기기' 버튼이 없는 게시물일 경우 건너뛰기
                    print("게시물 내에서 공감 또는 숨기기 버튼을 찾을 수 없습니다. 다음 게시물을 시도합니다.")
                    # `NoSuchElementException`이 발생하면 다음 게시물을 처리하도록 스크롤을 내립니다.
                    # 하지만 게시물 삭제가 되지 않았으므로, 다음 게시물을 보기 위해 스크롤을 내리는 작업이 필요합니다.
                    driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(2)
                    continue

                except Exception as e:
                    print(f"게시물 처리 중 오류 발생: {e}")
                    # 오류가 발생하면 루프를 다시 시작
                    continue

            except Exception as e:
                print(f"페이지에서 게시물 목록을 찾을 수 없습니다: {e}")
                print("10초 후 다시 시도합니다.")
                time.sleep(10)
                continue

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
    finally:
        # 작업이 끝나면 WebDriver를 닫습니다.
        print("매크로를 종료하고 브라우저를 닫습니다.")
        driver.quit()


if __name__ == "__main__":
    naver_blog_macro()

