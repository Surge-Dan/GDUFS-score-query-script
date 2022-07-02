import pytesseract
import requests
import re
from PIL import Image


# 1.验证码图片识别处理
def ca(filename: str) -> str:
    # Preprocess image for better OCR result.
    def clear_image(image: Image):
        def get_noise_color(image: Image):
            for y in range(1, image.size[1] - 1):
                # get the non-white colour at col 2
                (r, g, b) = image.getpixel((2, y))
                if r < 255 and g < 255 and b < 255:
                    return r, g, b

        image = image.convert('RGB')
        width = image.size[0]
        height = image.size[1]
        noise_color = get_noise_color(image)
        for x in range(width):
            for y in range(height):
                # remove borders & interference colours
                rgb = image.getpixel((x, y))
                if (x == 0 or y == 0 or x == width - 1 or y == height - 1
                        or rgb == noise_color or rgb[1] > 100):
                    image.putpixel((x, y), (255, 255, 255))
        return image

    image = Image.open(filename)
    image_grayscale = clear_image(image).convert('L')  # grayscale
    result: str = pytesseract.image_to_string(image_grayscale).strip()
    return ''.join(ch for ch in result if ch.isalnum())

# 验证码识别如上 调用形式如 ca("图片名称")即可


# 2.模拟登录
# 2.1 获取验证码并保存
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
}


def login(username, password):
    while True:
        login_url = 'https://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap'


def login(username, password):
    # 识别次数
    times = 0
    while True:
        login_url = 'https://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap'
        # 获取验证码url并下载
        resp = session.post(url=login_url, headers=headers).text
        verify_code_re = re.compile(r'<img  src="(.*?)" id="SafeCodeImg"', re.S)
        verify_code_url = re.findall(verify_code_re, resp)
        verify_url = f'https://jxgl.gdufs.edu.cn{verify_code_url[0]}'
        verify_content = session.get(verify_url, headers=headers).content
        # 保存验证码图片
        with open('verify.jpg', 'wb') as f:
            f.write(verify_content)
        # 识别验证码
        verify_code = ca('verify.jpg')
        # print(verify_code)
        data = {
            'USERNAME': username,
            'PASSWORD': password,
            'RANDOMCODE': verify_code,
        }
        page_text_login = session.post(url=login_url, headers=headers, data=data).text
        # print(page_text_login)
        # 判断验证码是否识别成功即（是否登录成功）
        # 如果尝试次数到达10次就停止，防止因为用户误输密码或者学号而导致的死循环。
        if times >= 10:
            print('验证码识别错误或者密码或者学号错误。请检查密码或者学号，如无误请重新运行！')
            break
        if "湖南强智科技教务系统" in page_text_login:
            print('模拟登录成功')
            print('======================================================')
            score_url = 'https://jxgl.gdufs.edu.cn/jsxsd/kscj/cjcx_list'
            check_score(score_url)
            break
        else:
            # 识别次数加1
            times += 1
            print('验证码识别错误')
            continue


# 3. 查成绩
def check_score(score_url):
    resp = session.get(score_url, headers=headers)
    # re提取课程名称和分数
    name_re = re.compile(r'<td align="left">(.*?)</td>', re.S)
    name = re.findall(name_re, resp.text)
    name_list = []
    for i in range(1, len(name) + 1, 2):
        name_list.append(name[i])
    score_re = re.compile(r'<td style=".*?".*?">(.*?)</a></td>', re.S)
    score = re.findall(score_re, resp.text)
    for i in range(len(name_list)):
        print(name_list[i], score[i])
    resp.close()


# 4. 主函数
if __name__ == '__main__':
    # 输入学号和密码
    while True:
        username = input('Please input you username: ')
        if len(username) != 11:
            print('Invalid username')
            continue
        else:
            break
    password = input('Please input your password: ')
    # 开始登录
    login(username, password)
