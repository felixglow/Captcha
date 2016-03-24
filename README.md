# Captcha

用途:
----
  生成图片验证码
  可作为django的app使用
  
实现:
----
  依赖python的第三方库Pillow
  mysql生成验证码及对应序列号，存储在mysql
  通过StringIO生成图片并作旋转模糊处理，返回'image/png'类型
  
使用：
----
  1.Captcha放入django根目录下
  2.项目主urls中include改app的url
  3.settings文件apps中加入Captcha
  4.将app中captcha_settings文件中内容拷贝至项目settings
  5.项目根目录执行
    ```python
    python manage.py syncdb 
    ```
    或 
    ```python
    python manage.py migrate
    ```
    
申明：
----
  项目是为了以后开发方便，也参考其他项目，自己按需要修改。
