cookie = {a.split("=")[0]:a.split("=")[1] for a in "SESSIONID=1234567890;USERID=xu.zhang@presoft.com.cn".split(";")}
print(cookie.get('abc'))