# GodaddyDDNS

Introduction简介
---
A python script for dynamically updating a GoDaddy DNS record, when IP address changes.<br>
用Py脚本实现自动更新DNS记录,监测本地IP变化。<br>

重要的一点，该脚本会先取回现有的DNS解析记录合并后再更新指定记录，避免提交新记录而引发其他记录丢失  : )

Dependencies依赖
---
This program was written and tested using Python 3<br>

Config配置
---
Modify the following configuration只需要修改代码中的以下配置项：<br>

你的域名：DOMAIN_NAME<br>
接口密钥：API_KEY<br>
接口加密：API_SECRET<br>
DNS记录名：record_name<br>

Documentations参考文档
---
[Godaddy官方文档](https://developer.godaddy.com/doc/endpoint/domains "Domains API")<br>
[Fix Error# SSL: CERTIFICATE_VERIFY_FAILED](https://blog.csdn.net/huryer/article/details/122728478)<br>
<https://www.instructables.com/Quick-and-Dirty-Dynamic-DNS-Using-GoDaddy><br>

