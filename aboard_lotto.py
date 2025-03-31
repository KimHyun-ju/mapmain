import re
import requests
import csv
import json

class AboardLotto:
    def __init__(self):
        self.lotto_data = {
            "japan_lotto6": self.japan_get()[0],
            "japan_lotto7": self.japan_get()[1],
            "singapore_lotto": self.singapore_get(),
            "swiss_lotto": self.swiss_get(),
            "south_africa_lotto": self.south_africa_get(),
            "philippine_lotto": self.philippine_get(),
            "nederland_lotto": self.nederland_get(),
            "newzealand_lotto": self.newzealand_get(),
            "newyork_lotto": self.newyork_get(),
            "euro_lotto": self.euro_get()
        }

    def save_to_json(self, filename="aboard_lotto.json"):
        try:
            with open(filename, "w", encoding="utf-8") as json_file:
                json.dump(self.lotto_data, json_file, ensure_ascii=False, indent=4)
            print(f"로또 데이터가 {filename} 파일로 저장되었습니다.")
        except Exception as e:
            print(f"JSON 저장 중 오류 발생: {e}")

    def japan_get(self): # 번호 6개 보너스 1개짜리, 번호 7개 보너스 2개짜리
        try:
            csv_name_url_6 = "https://www.mizuhobank.co.jp/takarakuji/apl/txt/loto6/name.txt"
            csv_name_url_7 = "https://www.mizuhobank.co.jp/takarakuji/apl/txt/loto7/name.txt"
            response_6 = requests.get(csv_name_url_6).content.decode('utf-8')
            response_7 = requests.get(csv_name_url_7).content.decode('utf-8')
            match_6 = re.search(r"NAME\s+(\S+)", response_6)
            match_7 = re.search(r"NAME\s+(\S+)", response_7)
            latest_csv_name_6 = match_6.group(1)
            latest_csv_name_7 = match_7.group(1)
            csv_url_6 = f"https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/csv/{latest_csv_name_6}"
            csv_url_7 = f"https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/csv/{latest_csv_name_7}"
            csv_response_6 = requests.get(csv_url_6).content.decode('shift-jis')
            csv_response_7 = requests.get(csv_url_7).content.decode('shift-jis')
            csv_reader_6 = list(csv.reader(csv_response_6.splitlines()))
            csv_reader_7 = list(csv.reader(csv_response_7.splitlines()))
            date_6 = re.findall(r'\d+', csv_reader_6[1][2])[1:]
            date_6_str = date_6[0] + "월 " + date_6[1] + "일"
            date_7 = re.findall(r'\d+', csv_reader_7[1][2])[1:]
            date_7_str = date_7[0] + "월 " + date_7[1] + "일"
            number_6 = list(map(int, [csv_reader_6[3][i] for i in [1, 2, 3, 4, 5, 6, 8]])) #마지막 1개 보너스
            number_7 = list(map(int, [csv_reader_7[3][i] for i in [1, 2, 3, 4, 5, 6, 7, 9, 10]])) #마지막 2개 보너스
            number_6 = list(map(str, number_6))
            number_7 = list(map(str, number_7))
            number_6.insert(0, date_6_str)
            number_7.insert(0, date_7_str)
        except:
            number_6 = ["-", "-", "-", "-", "-", "-", "-", "-"]
            number_7 = ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
        """날짜, 1,2,3,4,5,6 또는 7, 그리고 보너스"""
        return number_6, number_7

    def singapore_get(self): # 번호 6개 보너스 1개
        try:
            url = "https://www.singaporepools.com.sg/DataFileArchive/Lottery/Output/toto_result_top_draws_en.html"
            response = requests.get(url)
            html = response.text
            date_match = re.search(r"<th[^>]*class='drawDate'[^>]*>([^<]+)</th>", html)
            raw_date = date_match.group(1).strip() if date_match else "날짜 없음"

            # 날짜 변환 (예: "Thu, 27 Mar 2025" → "3월 27일")
            month_map = {
                "Jan": "1월", "Feb": "2월", "Mar": "3월", "Apr": "4월",
                "May": "5월", "Jun": "6월", "Jul": "7월", "Aug": "8월",
                "Sep": "9월", "Oct": "10월", "Nov": "11월", "Dec": "12월"
            }
            date_parts = raw_date.split()  # ['Thu,', '27', 'Mar', '2025']
            formatted_date = f"{month_map.get(date_parts[2], date_parts[2])} {int(date_parts[1])}일"
            main_numbers_all = re.findall(r"<td[^>]*class='win\d+'[^>]*>(\d+)</td>", html)
            main_numbers = main_numbers_all[0:6]
            # 추가 번호 찾기
            additional_number = re.search(r"<td[^>]*class='additional'[^>]*>(\d+)</td>", html)
            additional_number = additional_number.group(1) if additional_number else None
            main_numbers.append(additional_number)
            main_numbers.insert(0, formatted_date)
        except:
            main_numbers = ["-", "-", "-", "-", "-", "-", "-", "-"]
        return main_numbers

    def swiss_get(self): # 번호 6개 보너스 1개
        try:
            url = "https://www.swisslos.ch/en/swisslotto/information/winning-numbers/winning-numbers.html"
            response = requests.get(url)
            html = response.text

            # 날짜 찾기 (예: value="26.03.2025")
            date_match = re.search(r'<input[^>]*id="formattedFilterDate"[^>]*value="(\d{2})\.(\d{2})\.(\d{4})"', html)
            if date_match:
                day, month, year = date_match.groups()

                # 월 변환 (숫자 → "3월" 형식)
                month_map = {
                    "01": "1월", "02": "2월", "03": "3월", "04": "4월",
                    "05": "5월", "06": "6월", "07": "7월", "08": "8월",
                    "09": "9월", "10": "10월", "11": "11월", "12": "12월"
                }
                formatted_date = f"{month_map[month]} {int(day)}일"
            else:
                formatted_date = "날짜 없음"

            # 메인 로또 번호 찾기
            main_numbers_all = re.findall(r'<li[^>]*actual-numbers__number___normal[^>]*>\s*<span[^>]*>(\d+)</span>', html)
            main_numbers = main_numbers_all[:6]
            lucky_number = re.search(r'<li[^>]*actual-numbers__number___lucky[^>]*>\s*<span[^>]*>(\d+)</span>', html)
            lucky_number = lucky_number.group(1) if lucky_number else None
            main_numbers.append(lucky_number)
            main_numbers.insert(0, formatted_date)
        except:
            main_numbers = ["-", "-", "-", "-", "-", "-", "-", "-"]
        return main_numbers

    def south_africa_get(self):  # 번호 6개 보너스 1개
        try:
            url = "https://www.nationallottery.co.za/results/lotto"
            headers = {
                "Accept-Encoding": "identity",  # Gzip 압축 해제 방지
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(url, headers=headers)
            html = response.text
            date_pattern = r'<span class="date">(\d{4}-\d{2}-\d{2})</span>'
            date_match = re.search(date_pattern, html)
            draw_date = date_match.group(1) if date_match else None
            date_list = draw_date.split("-")[1:]
            month, day = date_list
            date_out = str(int(month)) + "월 " + day + "일"
            # 당첨번호 추출
            numbers_pattern = r'<li class="ball ball\d+ active"><div class="shape"><span>(\d+)</span></div></li>'
            numbers_raw = re.findall(numbers_pattern, html)
            numbers = numbers_raw[:-1]
            # 정렬된 번호(보너스 번호 포함)
            main_numbers = sorted(numbers[:-1])  # 마지막 번호는 보너스 번호이므로 제외하고 정렬
            bonus_number = numbers[-1]  # 마지막 번호가 보너스 번호
            main_numbers.append(bonus_number)
            main_numbers.insert(0, date_out)
        except:
            main_numbers = ["-", "-", "-", "-", "-", "-", "-", "-"]
        return main_numbers

    def philippine_get(self): # 번호 6개
        try:
            url = "https://www.pcso.gov.ph/SearchLottoResult.aspx"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            html = response.text
            pattern = r"<td[^>]*>\s*Megalotto 6/45\s*</td>\s*<td[^>]*>\s*([\d\-]+)\s*</td>\s*<td[^>]*>\s*([\d/]+)\s*</td>"
            match = re.search(pattern, html)
            winning_numbers = list(map(str, sorted(match.group(1).split("-"), key=int)))
            winning_numbers = list(map(str, winning_numbers))
            draw_date = match.group(2).split("/")[:-1]
            month, day = draw_date
            date_out = str(int(month)) + "월 " + str(int(day)) + "일"
            winning_numbers.insert(0, date_out)
        except:
            winning_numbers = ["-", "-", "-", "-", "-", "-", "-"]
        return winning_numbers

    def nederland_get(self): # 번호 6개 보너스 1개
        try:
            url = "https://lotto.nederlandseloterij.nl/trekkingsuitslag"
            response = requests.get(url)
            html = response.text
            month_map = {
                "januari": "1월 ", "februari": "2월 ", "maart": "3월 ",
                "april": "4월 ", "mei": "5월 ", "juni": "6월 ",
                "juli": "7월 ", "augustus": "8월 ", "september": "9월 ",
                "oktober": "10월 ", "november": "11월 ", "december": "12월 "
            }
            # 정규식 패턴 (날짜 추출)
            pattern_date = r'(\d{1,2}) (\w+) (\d{4})'
            match_date = re.search(pattern_date, html)
            day, dutch_month, year = match_date.groups()
            month = month_map.get(dutch_month, dutch_month)  # 영어 월로 변환
            date_out = month + day + "일"
            pattern = r'ticketNumberNumber_oxjw1_21">(\d+)</span>'
            winning_numbers = re.findall(pattern, html)[:7]
            winning_numbers.insert(0, date_out)
        except:
            winning_numbers = ["-", "-", "-", "-", "-", "-", "-", "-"]
        return winning_numbers

    def newzealand_get(self): # 번호 6개 보너스 1개
        try:
            url = "https://gateway.mylotto.co.nz/api/results/v1/results/lotto"
            response = requests.get(url).json()
            draw_date = response["lotto"]["drawDate"]
            winning_numbers = response["lotto"]["lottoWinningNumbers"]["numbers"]
            bonus_ball = response["lotto"]["lottoWinningNumbers"]["bonusBalls"]
            month, day = map(str, (map(int, draw_date.split("-")[1:])))
            date_out = month +"월 " + day + "일"
            winning_numbers.append(bonus_ball)
            winning_numbers.insert(0, date_out)
        except:
            winning_numbers = ["-", "-", "-", "-", "-", "-", "-", "-"]
        return winning_numbers

    def newyork_get(self):
        try:
            url = "https://nylottery.ny.gov/drupal-api/api/v2/winning_numbers?_format=json&nid=26&page=0"
            response = requests.get(url).json()
            latest_draw = response["rows"][0]  # 첫 번째 요소가 가장 최근 데이터임
            draw_date = latest_draw["date"]
            winning_numbers = latest_draw["winning_numbers"]
            bonus_number = latest_draw["bonus_number"]
            month, day = map(str, (map(int, draw_date.split("-")[1:])))
            date_out = month +"월 " + day + "일"
            winning_numbers.append(bonus_number)
            winning_numbers.insert(0, date_out)
        except:
            winning_numbers = ["-", "-", "-", "-", "-", "-", "-", "-"]
        return winning_numbers

    def euro_get(self):
        try:
            url = "https://www.euro-millions.com/results"
            response = requests.get(url)
            html = response.text

            # 날짜 변환용 딕셔너리
            month_map = {
                "January": "1월", "February": "2월", "March": "3월", "April": "4월",
                "May": "5월", "June": "6월", "July": "7월", "August": "8월",
                "September": "9월", "October": "10월", "November": "11월", "December": "12월"
            }

            # 날짜 추출 (예: "28th March 2025")
            date_pattern = re.findall(r'(\d{1,2})(?:<sup>.*?</sup>)?\s+([A-Za-z]+)\s+\d{4}', html)
            dates = [f"{month_map[month]} {int(day)}일" for day, month in date_pattern]

            # 당첨 번호 추출
            numbers_pattern = re.findall(r'<li class="resultBall ball">(\d+)</li>', html)
            lucky_numbers_pattern = re.findall(r'<li class="resultBall lucky-star">(\d+)</li>', html)

            # 당첨 번호 그룹화 (5개 + 럭키 스타 2개)
            draw_results = [
                {
                    "date": dates[i // 5],  # 5개씩 묶이므로 인덱스 계산
                    "numbers": numbers_pattern[i:i + 5],
                    "lucky_numbers": lucky_numbers_pattern[i // 5 * 2:i // 5 * 2 + 2]
                }
                for i in range(0, len(numbers_pattern), 5)
            ]

            # 최신 결과 변환
            result = draw_results[0]
            output = [result["date"], *result["numbers"], *result["lucky_numbers"]]
        except:
            output = ["-", "-", "-", "-", "-", "-", "-", "-"]
        return output

if __name__ == "__main__":
    lotto = AboardLotto()
    lotto.save_to_json()
