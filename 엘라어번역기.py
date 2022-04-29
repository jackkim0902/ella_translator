#자모음 분해 출처 : https://github.com/neotune/python-korean-handler/blob/master/korean_handler.py

# -*- coding: utf-8 -*-
import re
import sys
from PIL import Image,ImageDraw,ImageFont
"""
    초성 중성 종성 분리 하기
	유니코드 한글은 0xAC00 으로부터
	초성 19개, 중성21개, 종성28개로 이루어지고
	이들을 조합한 11,172개의 문자를 갖는다.
	한글코드의 값 = ((초성 * 21) + 중성) * 28 + 종성 + 0xAC00
	(0xAC00은 'ㄱ'의 코드값)
	따라서 다음과 같은 계산 식이 구해진다.
	유니코드 한글 문자 코드 값이 X일 때,
	초성 = ((X - 0xAC00) / 28) / 21
	중성 = ((X - 0xAC00) / 28) % 21
	종성 = (X - 0xAC00) % 28
	이 때 초성, 중성, 종성의 값은 각 소리 글자의 코드값이 아니라
	이들이 각각 몇 번째 문자인가를 나타내기 때문에 다음과 같이 다시 처리한다.
	초성문자코드 = 초성 + 0x1100 //('ㄱ')
	중성문자코드 = 중성 + 0x1161 // ('ㅏ')
	종성문자코드 = 종성 + 0x11A8 - 1 // (종성이 없는 경우가 있으므로 1을 뺌)
"""
# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
#ㅏ ㅑ ㅓ ㅕ ㅗ ㅛ ㅜ ㅠ ㅡ ㅣ 
#0  2  4  6  8 12 13 17 18 20
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
#ㄱ ㄴ ㄷ ㄹ ㅁ  ㅂ  ㅅ ㅇ ㅈ  ㅊ ㅋ ㅌ ㅍ ㅎ
#1  4  7  8  16 17  19 21 22 23 24 25 26 27
def convert(test_keyword):
    split_keyword_list = list(test_keyword)
    #print(split_keyword_list)

    result = list()
    for keyword in split_keyword_list:
        # 한글 여부 check 후 분리
        if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
            flag1 = False
            flag2 = False
            flag3 = False
            if keyword in CHOSUNG_LIST:
                flag1 = True
                char1 = CHOSUNG_LIST.index(keyword)
            elif keyword in JUNGSUNG_LIST:
                flag2 = True
                char2 = JUNGSUNG_LIST.index(keyword)
            elif keyword in JONGSUNG_LIST:
                flag3 = True
                char3 = JONGSUNG_LIST.index(keyword)
            else:
                char_code = ord(keyword) - BASE_CODE
                char1 = int(char_code / CHOSUNG)
                #print('초성 : {}'.format(CHOSUNG_LIST[char1]))
                char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
                #print('중성 : {}'.format(JUNGSUNG_LIST[char2]))
                char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
                flag1 = True
                flag2 = True
                flag3 = True
                
            if flag1: #초성
                if char1 == 1: #ㄲ
                    result.append(CHOSUNG_LIST[0])
                    result.append(CHOSUNG_LIST[0])
                elif char1 == 4: #ㄸ
                    result.append(CHOSUNG_LIST[3])
                    result.append(CHOSUNG_LIST[3])
                elif char1 == 8: #ㅃ
                    result.append(CHOSUNG_LIST[7])
                    result.append(CHOSUNG_LIST[7])
                elif char1 == 10: #ㅆ
                    result.append(CHOSUNG_LIST[9])
                    result.append(CHOSUNG_LIST[9])
                elif char1 == 13: #ㅉ
                    result.append(CHOSUNG_LIST[12])
                    result.append(CHOSUNG_LIST[12])    
                else:
                    result.append(CHOSUNG_LIST[char1])
            
            if flag2: #중성
                if char2 == 1: #ㅐ
                    result.append(JUNGSUNG_LIST[0])
                    result.append(JUNGSUNG_LIST[20])
                elif char2 == 3: #ㅒ
                    result.append(JUNGSUNG_LIST[2])
                    result.append(JUNGSUNG_LIST[20])
                elif char2 == 5: #ㅔ
                    result.append(JUNGSUNG_LIST[4])
                    result.append(JUNGSUNG_LIST[20])
                elif char2 == 7: #ㅖ
                    result.append(JUNGSUNG_LIST[6])
                    result.append(JUNGSUNG_LIST[20])
                elif char2 == 9: #ㅘ
                    result.append(JUNGSUNG_LIST[8])
                    result.append(JUNGSUNG_LIST[0])
                elif char2 == 10: #ㅙ
                    result.append(JUNGSUNG_LIST[8])
                    result.append(JUNGSUNG_LIST[0])
                    result.append(JUNGSUNG_LIST[20])
                elif char2 == 11: #ㅚ
                    result.append(JUNGSUNG_LIST[8])
                    result.append(JUNGSUNG_LIST[20])
                elif char2 == 14: #ㅝ
                    result.append(JUNGSUNG_LIST[13])
                    result.append(JUNGSUNG_LIST[4])
                elif char2 == 15: #ㅞ
                    result.append(JUNGSUNG_LIST[13])
                    result.append(JUNGSUNG_LIST[4])
                    result.append(JUNGSUNG_LIST[20])
                elif char2 == 16: #ㅟ
                    result.append(JUNGSUNG_LIST[13])
                    result.append(JUNGSUNG_LIST[20])
                elif char2 == 19: #ㅢ
                    result.append(JUNGSUNG_LIST[18])
                    result.append(JUNGSUNG_LIST[20])
                else:
                    result.append(JUNGSUNG_LIST[char2])
            
            if flag3: #종성
                if char3==0:
                    #result.append('#')
                    pass
                else:
                    if char3 == 2: #ㄲ
                        result.append(JONGSUNG_LIST[1])
                        result.append(JONGSUNG_LIST[1])
                    elif char3 == 3: #ㄳ
                        result.append(JONGSUNG_LIST[1])
                        result.append(JONGSUNG_LIST[19])
                    elif char3 == 5: #ㄵ
                        result.append(JONGSUNG_LIST[4])
                        result.append(JONGSUNG_LIST[22])
                    elif char3 == 6: #ㄶ
                        result.append(JONGSUNG_LIST[4])
                        result.append(JONGSUNG_LIST[27])
                    elif char3 == 9: #ㄺ
                        result.append(JONGSUNG_LIST[8])
                        result.append(JONGSUNG_LIST[1])
                    elif char3 == 10: #ㄻ
                        result.append(JONGSUNG_LIST[8])
                        result.append(JONGSUNG_LIST[16])
                    elif char3 == 11: #ㄼ
                        result.append(JONGSUNG_LIST[8])
                        result.append(JONGSUNG_LIST[17])
                    elif char3 == 12: #ㄽ
                        result.append(JONGSUNG_LIST[8])
                        result.append(JONGSUNG_LIST[19])
                    elif char3 == 13: #ㄾ
                        result.append(JONGSUNG_LIST[8])
                        result.append(JONGSUNG_LIST[25])
                    elif char3 == 14: #ㄿ
                        result.append(JONGSUNG_LIST[8])
                        result.append(JONGSUNG_LIST[26])
                    elif char3 == 15: #ㅀ
                        result.append(JONGSUNG_LIST[8])
                        result.append(JONGSUNG_LIST[27])
                    elif char3 == 18: #ㅄ
                        result.append(JONGSUNG_LIST[17])
                        result.append(JONGSUNG_LIST[19])
                    elif char3 == 20: #ㅆ
                        result.append(JONGSUNG_LIST[19])
                        result.append(JONGSUNG_LIST[19])
                    else:
                        result.append(JONGSUNG_LIST[char3])
                    #print('종성 : {}'.format(JONGSUNG_LIST[char3]))
        else:
            result.append(keyword)
    # result
    #print("".join(result))
    return result

def make_image(splited_str, mean):
    
    #한글을 영문자로 바꾸기
    draw_text = ""
    for keyword in splited_str:
        if keyword == "ㄱ":
            draw_text += "r"
        elif keyword == "ㄴ":
            draw_text += "s"
        elif keyword == "ㄷ":
            draw_text += "e"
        elif keyword == "ㄹ":
            draw_text += "f"
        elif keyword == "ㅁ":
            draw_text += "a"
        elif keyword == "ㅂ":
            draw_text += "q"
        elif keyword == "ㅅ":
            draw_text += "t"
        elif keyword == "ㅇ":
            draw_text += "d"
        elif keyword == "ㅈ":
            draw_text += "w"
        elif keyword == "ㅊ":
            draw_text += "c"
        elif keyword == "ㅋ":
            draw_text += "z"
        elif keyword == "ㅌ":
            draw_text += "x"
        elif keyword == "ㅍ":
            draw_text += "v"
        elif keyword == "ㅎ":
            draw_text += "g"
        elif keyword == "ㅏ":
            draw_text += "k"
        elif keyword == "ㅑ":
            draw_text += "i"
        elif keyword == "ㅓ":
            draw_text += "j"
        elif keyword == "ㅕ":
            draw_text += "u"
        elif keyword == "ㅗ":
            draw_text += "h"
        elif keyword == "ㅛ":
            draw_text += "y"
        elif keyword == "ㅜ":
            draw_text += "n"
        elif keyword == "ㅠ":
            draw_text += "b"
        elif keyword == "ㅡ":
            draw_text += "m"
        elif keyword == "ㅣ":
            draw_text += "l"
        else:
            draw_text += keyword
    
    # 이미지로 출력할 글자 및 폰트 지정 
    #draw_text = 'rse'
    font = ImageFont.truetype("엘라어.ttf", 100)
    
    # 이미지 사이즈 지정
    text_width = 50*len(draw_text)
    text_height = 100
    
    # 이미지 객체 생성 (배경 검정)
    canvas = Image.new('RGB', (text_width, text_height), "white")
    
    # 가운데에 그리기 (폰트 색: 하양)
    draw = ImageDraw.Draw(canvas)
    w, h = font.getsize(draw_text)
    draw.text(((text_width-w)/2.0,(text_height-h)/2.0), draw_text, 'black', font)
    
    # png로 저장 및 출력해서 보기
    canvas.save(mean+'.png', "PNG")
    #canvas.show()


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        inputfile = open(sys.argv[1], 'r')
        for line in inputfile.readlines():
            convert(line)
    else:
        test_keyword = input("input your text:")
        #print(convert(test_keyword))
        make_image(convert(test_keyword), test_keyword)