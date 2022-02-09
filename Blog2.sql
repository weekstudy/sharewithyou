-- MySQL dump 10.13  Distrib 5.7.20, for macos10.12 (x86_64)
--
-- Host: localhost    Database: Blog2
-- ------------------------------------------------------
-- Server version	5.7.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `articlesapp_articlepost`
--

DROP TABLE IF EXISTS `articlesapp_articlepost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articlesapp_articlepost` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `body` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `author_id` int(11) NOT NULL,
  `total_views` int(10) unsigned NOT NULL,
  `column_id` bigint(20) DEFAULT NULL,
  `avatar_svg` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `articlesapp_articlepost_author_id_6a09a8f8_fk_auth_user_id` (`author_id`),
  KEY `articlesapp_articlep_column_id_795865ba_fk_articlesa` (`column_id`),
  CONSTRAINT `articlesapp_articlep_column_id_795865ba_fk_articlesa` FOREIGN KEY (`column_id`) REFERENCES `articlesapp_category` (`id`),
  CONSTRAINT `articlesapp_articlepost_author_id_6a09a8f8_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articlesapp_articlepost`
--

LOCK TABLES `articlesapp_articlepost` WRITE;
/*!40000 ALTER TABLE `articlesapp_articlepost` DISABLE KEYS */;
INSERT INTO `articlesapp_articlepost` VALUES (1,'搭建个人博客笔记','- 配置环境\r\n- 学习命令','2021-12-22 12:46:00.000000','2021-12-30 21:12:03.881612',1,44,1,''),(2,'搭建个人博客（2）','- 学习url配置\r\n- 学习模板\r\n- 学习Model\r\n```python\r\nimport os\r\nimport time\r\nimport hashlib\r\nimport tkinter.messagebox  # 弹窗库\r\nfrom tkinter import *\r\nimport markdown\r\n\r\nfrom django.shortcuts import render\r\nfrom django.http import HttpResponse\r\n\r\nfrom django.contrib import messages\r\n\r\nfrom sharewithyou.settings import MEDIA_ROOT\r\n\r\nfrom .models import ArticlePost\r\n\r\n\r\n# Create your views here.\r\ndef article_list(request):\r\n    # 取出所有博客文章\r\n    articles = ArticlePost.objects.all()\r\n    # 需要传递给模板（templates）的对象\r\n    context = {\'articles\': articles}\r\n    # render函数：载入模板，并返回context对象\r\n    return render(request, \'article/all_articles.html\', context)\r\n\r\n\r\ndef show_article(request, id):\r\n    \"\"\"\r\n    展示文章详情\r\n    :param request:\r\n    :param id:\r\n    :return:\r\n    \"\"\"\r\n    # 取出相应的文章\r\n    total = len(ArticlePost.objects.all())\r\n    print(\'id-----\',id)\r\n    article = ArticlePost.objects.get(id=id)\r\n    article.body = markdown.markdown(article.body,\r\n                                     extensions=[\r\n                                         # 包含 缩写、表格等常用扩展\r\n                                         \'markdown.extensions.extra\',\r\n                                         # 语法高亮扩展\r\n                                         \'markdown.extensions.codehilite\',\r\n                                     ])\r\n    if int(id + 1) <= total:\r\n        next_article = ArticlePost.objects.get(id=id + 1)\r\n        # 需要传递给模板的对象\r\n        context = {\'article\': article, \'next_article\': next_article}\r\n    else:\r\n        next_article = ArticlePost.objects.get(id=id-1)\r\n        context = {\'article\': article, \'next_article\': next_article}\r\n    # 载入模板，并返回context对象\r\n    return render(request, \'article/show_article.html\', context)\r\n\r\n\r\ndef upload(request):\r\n    \"\"\"\r\n    上传图片文件，\r\n    :param request:\r\n    :return:\r\n    \"\"\"\r\n    context = {\'success\': True}\r\n    if request.method == \"GET\":  # 请求\r\n        return render(request, \'test/test_upload.html\', )\r\n    elif request.method == \"POST\":\r\n        # FILES只接收上传信息？？\r\n        my_file = request.FILES.get(\"pic\", None)  # 获取上传的文件，如果没有文件，则默认为None\r\n        # print(\'my_file.name\', my_file.name)\r\n        # print(\'myfile\', my_file)\r\n        # print(type(my_file))\r\n        # # 普通数据还是用POST\r\n        # print(request.POST.get(\'title\'))\r\n        # print(request.POST.get(\'title\'))\r\n        if not my_file:\r\n            return HttpResponse(\"no files for upload!\")\r\n        # destination=open(os.path.join(\'upload\',myFile.name),\'wb+\')\r\n        filename = get_name() + \'.\' + my_file.name.split(\'.\').pop()\r\n        save_dir = os.path.join(MEDIA_ROOT, \'test\')\r\n        filename = os.path.join(save_dir, filename)\r\n        destination = open(filename, \'wb+\')  # 打开特定的文件进行二进制的写操作\r\n        for chunk in my_file.chunks():  # 分块写入文件\r\n            destination.write(chunk)\r\n        destination.close()\r\n        # tkinter.messagebox.showinfo(\'提示\', \'登录成功\')\r\n        # mainloop()\r\n        # 这里应该要数据库里面存在了才能设置上传成功\r\n        if filename in os.listdir(save_dir):\r\n            context = {\'success\': True, \'title\': request.POST.get(\'title\'), \'filename\': my_file.name}\r\n    else:\r\n        context = {\'success\': False}\r\n\r\n    # messages.success(request,\"哈哈哈哈\")\r\n    return render(request, \'test/test_upload.html\', context)\r\n\r\n\r\ndef get_name():\r\n    md5 = hashlib.md5()\r\n    md5.update(bytes(str(time.perf_counter()), encoding=\'utf8\'))\r\n    # md5 = hashlib.md5()\r\n    # s = \"password\" + \"salt\"\r\n    # md5.update(s.encode())\r\n    # md5.hexdigest()\r\n    # \'b305cadbb3bce54f3aa59c64fec00dea\'\r\n    return md5.hexdigest()\r\n\r\n\r\n```','2015-12-22 12:47:00.000000','2021-12-30 21:11:42.532652',1,12,1,''),(3,'目标检测算法之yolo系列(1)','体检测的两个步骤可以概括为：\r\n\r\n步骤一：检测目标位置（生成矩形框）\r\n\r\n步骤二：对目标物体进行分类\r\n\r\n物体检测主流的算法框架大致分为one-stage与two-stage。two-stage算法代表有R-CNN系列，one-stage算法代表有Yolo系列。按笔者理解，two-stage算法将步骤一与步骤二分开执行，输入图像先经过候选框生成网络（例如faster rcnn中的RPN网络），再经过分类网络；one-stage算法将步骤一与步骤二同时执行，输入图像只经过一个网络，生成的结果中同时包含位置与类别信息。two-stage与one-stage相比，精度高，但是计算量更大，所以运算较慢。\r\n\r\n创新\r\nYOLO将物体检测作为回归问题求解，而且可以实现end-to-end的训练网络，完成从原始图像的输入到物体位置和类别的输出。\r\n从网络设计上，YOLO与rcnn、fast rcnn及faster rcnn的区别在于：\r\n\r\nYOLO训练和检测均是在一个单独网络中进行。YOLO没有显示地求取region proposal的过程。而rcnn/fast rcnn 采用分离的模块（独立于网络之外的selective search方法）求取候选框（可能会包含物体的矩形区域），训练过程因此也是分成多个模块进行。Faster rcnn使用RPN（region proposal network）卷积网络替代rcnn/fast rcnn的selective\r\nsearch模块，将RPN集成到fast rcnn检测网络中，得到一个统一的检测网络。尽管RPN与fast rcnn共享卷积层，但是在模型训练过程中，需要反复训练RPN网络和fast rcnn网络（注意这两个网络核心卷积层是参数共享的）。\r\n这里可以说明fasterRcnn如何训练？\r\nYOLO将物体检测作为一个回归问题进行求解，输入图像经过一次inference，便能得到图像中所有物体的位置和其所属类别及相应的置信概率。而rcnn/fast rcnn/faster rcnn将检测结果分为两部分求解：物体类别（分类问题），物体位置即bounding box（回归问题）','2021-12-23 01:11:00.000000','2021-12-31 11:57:08.767278',1,194,4,'article_svg/20211231/vector_landscape_3.svg'),(4,'Django测试markdown目录','# 一级标题\r\n## 二级标题\r\n### 三级标题\r\n#### 四级标题\r\n##### 五级标题\r\n###### 六级标题 \r\n- 文本1\r\n- 文本2\r\n- 文本3','2021-06-24 09:03:02.875000','2021-12-26 13:01:38.527206',1,44,1,''),(5,'目标检测yolov2','主要是增加了8个trick\r\n与faster R-cnn相比，召回率偏低，因此需要解决召回率的问题，\r\n\r\n\r\n- 1、Batch Normalization \r\n检测系列的网络结构中，BN逐渐变成了标配。在Yolo的每个卷积层中加入BN之后，mAP提升了2%，并且去除了Dropout。\r\n-  2、High Resolution Classifie\r\n在Yolov1中，网络的backbone部分会在ImageNet数据集上进行预训练，训练时网络输入图像的分辨率为224*224。在v2中，将分类网络在输入图片分辨率为448*448的ImageNet数据集上训练10个epoch，再使用检测数据集（例如coco）进行微调。高分辨率预训练使mAP提高了大约4%。\r\n-  3、Convolutional With Anchor Boxes\r\n根据faster r-cnn的结果，表明在anchor box上更容易。神经网络不对预测矩形框的宽高的绝对值进行预测，而是预测与Anchor框的偏差（offset），每个格点指定n个Anchor框。在训练时，最接近ground truth的框产生loss，其余框不产生loss。在引入Anchor Box操作后，mAP由69.5下降至69.2，原因在于，每个格点预测的物体变多之后，召回率大幅上升，准确率有所下降，总体mAP略有下降。\r\n- 4、Dimension Clusters \r\nFaster R-CNN中的九个Anchor Box的宽高是事先设定好的比例大小，一共设定三个面积大小的矩形框，每个矩形框有三个宽高比：1:1，2:1，1:2，总共九个框。而在v2中，Anchor Box的宽高不经过人为获得，而是将训练数据集中的矩形框全部拿出来，用kmeans聚类得到先验框的宽和高。例如使用5个Anchor Box，那么kmeans聚类的类别中心个数设置为5。加入了聚类操作之后，引入Anchor Box之后，mAP上升。\r\n- 5、Direct location prediction\r\nYolo中的位置预测方法很清晰，就是相对于左上角的格点坐标预测偏移量。具体公式参见OneNote笔记\r\n- 6、Fine-Grained Features\r\n通过一个passthrough层，p将26*26*1的特征图，变成13*13*4的特征图，在这一次操作中不损失细粒度特征，相当于是将空间信息在深度方向保存\r\n-  7、Multi-Scale Training\r\n很关键的一点是，Yolo v2中只有卷积层与池化层，所以对于网络的输入大小，并没有限制，整个网络的降采样倍数为32，只要输入的特征图尺寸为32的倍数即可，如果网络中有全连接层，就不是这样了。所以Yolo v2可以使用不同尺寸的输入图片训练。\r\n\r\n作者使用的训练方法是，在每10个batch之后，就将图片resize成{320, 352, ..., 608}中的一种。不同的输入，最后产生的格点数不同，比如输入图片是320*320，那么输出格点是10*10，如果每个格点的先验框个数设置为5，那么总共输出500个预测结果；如果输入图片大小是608*608，输出格点就是19*19，共1805个预测结果。\r\n在引入了多尺寸训练方法后，迫使卷积核学习不同比例大小尺寸的特征。当输入设置为544*544甚至更大，Yolo v2的mAP已经超过了其他的物体检测算法。\r\n但是效率很低，在v3中就引入了FPN\r\n\r\n- 8、Faster——Darknet-19','2020-12-26 12:54:00.000000','2021-12-27 13:50:27.690269',1,24,3,''),(20,'Django之测试上传文章封面','- 在model中增加一个字段ImageField \r\n- 修改ModelForm表单\r\n- 然后修改视图函数中如何处理提交的数据\r\n- 修改前端的显示数据','2020-12-27 02:11:38.024000','2021-12-27 02:11:38.066442',1,14,1,''),(35,'python之时间模块time，datetime','```python\r\n#!/usr/bin/python\r\n# -*- coding: UTF-8 -*-\r\n \r\nimport time\r\n \r\n# 格式化成2016-03-20 11:45:39形式\r\nprint time.strftime(\"%Y-%m-%d %H:%M:%S\", time.localtime()) \r\n \r\n# 格式化成Sat Mar 28 22:24:24 2016形式\r\nprint time.strftime(\"%a %b %d %H:%M:%S %Y\", time.localtime()) \r\n  \r\n# 将格式字符串转换为时间戳\r\na = \"Sat Mar 28 22:24:24 2016\"\r\nprint time.mktime(time.strptime(a,\"%a %b %d %H:%M:%S %Y\"))\r\n\r\n```\r\n### 1. str类型的日期转换为时间戳\r\n```python\r\n# 字符类型的时间\r\ntss1 = \'2013-10-10 23:40:00\'\r\n# 转为时间数组\r\ntimeArray = time.strptime(tss1, \"%Y-%m-%d %H:%M:%S\")\r\nprint timeArray\r\n# timeArray可以调用tm_year等\r\nprint timeArray.tm_year   # 2013\r\n# 转为时间戳\r\ntimeStamp = int(time.mktime(timeArray))\r\nprint timeStamp  # 1381419600\r\n\r\n\r\n# 结果如下\r\ntime.struct_time(tm_year=2013, tm_mon=10, tm_mday=10, tm_hour=23, tm_min=40, tm_sec=0, tm_wday=3, tm_yday=283, tm_isdst=-1)\r\n2013\r\n1381419600\r\n```\r\n### 2.更改str类型日期的显示格式\r\n\r\n```python\r\n\r\ntss2 = \"2013-10-10 23:40:00\"\r\n# 转为数组\r\ntimeArray = time.strptime(tss2, \"%Y-%m-%d %H:%M:%S\")\r\n# 转为其它显示格式\r\notherStyleTime = time.strftime(\"%Y/%m/%d %H:%M:%S\", timeArray)\r\nprint otherStyleTime  # 2013/10/10 23:40:00\r\n\r\ntss3 = \"2013/10/10 23:40:00\"\r\ntimeArray = time.strptime(tss3, \"%Y/%m/%d %H:%M:%S\")\r\notherStyleTime = time.strftime(\"%Y-%m-%d %H:%M:%S\", timeArray)\r\nprint otherStyleTime  # 2013-10-10 23:40:00\r\n```\r\n### 3.时间戳转换为指定格式的日期\r\n\r\n```python\r\n# 使用time\r\ntimeStamp = 1381419600\r\ntimeArray = time.localtime(timeStamp)\r\notherStyleTime = time.strftime(\"%Y--%m--%d %H:%M:%S\", timeArray)\r\nprint(otherStyleTime)   # 2013--10--10 23:40:00\r\n# 使用datetime\r\ntimeStamp = 1381419600\r\ndateArray = datetime.datetime.fromtimestamp(timeStamp)\r\notherStyleTime = dateArray.strftime(\"%Y--%m--%d %H:%M:%S\")\r\nprint(otherStyleTime)   # 2013--10--10 23:40:00\r\n# 使用datetime，指定utc时间，相差8小时\r\ntimeStamp = 1381419600\r\ndateArray = datetime.datetime.utcfromtimestamp(timeStamp)\r\notherStyleTime = dateArray.strftime(\"%Y--%m--%d %H:%M:%S\")\r\nprint(otherStyleTime)   # 2013--10--10 15:40:00\r\n```\r\n### 4.获取当前时间并且用指定格式显示\r\n\r\n```python\r\n# time获取当前时间戳\r\nnow = int(time.time())     # 1533952277\r\ntimeArray = time.localtime(now)\r\nprint timeArray\r\notherStyleTime = time.strftime(\"%Y--%m--%d %H:%M:%S\", timeArray)\r\nprint otherStyleTime\r\n\r\n# 结果如下\r\ntime.struct_time(tm_year=2018, tm_mon=8, tm_mday=11, tm_hour=9, tm_min=51, tm_sec=17, tm_wday=5, tm_yday=223, tm_isdst=0)\r\n2018--08--11 09:51:17\r\n\r\n\r\n# datetime获取当前时间，数组格式\r\nnow = datetime.datetime.now()\r\nprint now\r\notherStyleTime = now.strftime(\"%Y--%m--%d %H:%M:%S\")\r\nprint otherStyleTime\r\n\r\n# 结果如下：\r\n2018-08-11 09:51:17.362986\r\n2018--08--11 09:51:17\r\n```','2020-12-27 07:08:23.104000','2021-12-27 07:08:23.109752',1,12,1,''),(36,'测试ImageFiled','测试ImageFiled','2020-12-27 08:30:28.767000','2021-12-27 08:30:28.808350',1,2,1,''),(38,'测试上传svg','无','2019-12-27 08:44:43.518000','2021-12-27 08:44:43.526260',1,0,1,''),(39,'测试上传svg','无','2019-11-27 08:45:48.869000','2021-12-27 08:45:48.877471',1,0,1,''),(40,'上传svg','无','2019-11-27 09:04:08.806000','2021-12-27 09:04:08.810242',1,0,1,''),(41,'上传svg','无','2018-05-27 09:04:53.275000','2021-12-27 09:04:53.279267',1,0,1,''),(42,'上传svg','无','2018-12-27 09:05:09.183000','2021-12-27 12:47:18.797464',1,7,9,'article_svg/20211227/vecteezy_night-city-water-reflection-landscape-illustration_.svg'),(43,'上传svg','无','2018-12-27 09:07:08.501000','2021-12-27 10:18:22.595487',1,8,9,'article_svg/20211227/vecteezy_night-city-water-reflection-landscape-illustration_.jpg'),(44,'上传svg','无','2017-12-27 09:11:10.170000','2021-12-27 10:07:28.855471',1,3,9,'article_svg/20211227/vector_landscape_2.svg'),(45,'上传svg3','修改图片3','2016-12-27 09:11:46.825000','2021-12-27 10:01:04.776050',1,20,1,'article_svg/20211227/vector_landscape_1.svg'),(46,'测试上传svg','无','2018-12-27 09:15:51.337000','2021-12-28 07:09:26.466450',1,4,1,''),(47,'测试上传svg','无','2020-12-27 09:18:14.784000','2021-12-27 13:58:05.146648',1,124,1,''),(48,'测试网站','马克思的时间内的开始缴纳的卡是能看到你十多年开始你付款jksndfa','2021-12-31 21:14:03.160089','2021-12-31 21:14:03.161571',1,6,4,'article_svg/20211231/cover2.webp'),(49,'测试','# Linux之vi 操作\r\n\r\n#### 命令模式\r\n\r\n##### 在每次运行Vim编辑器时，默认进入命令模式，此时需要先切换到输入模式后再进行文档编写工作，而每次在编写完文档后需要先返回命令模式，然后再进入末行模式，执行文档的保存或退出操作。在Vim中，无法直接从输入模式切换到末行模式。\r\n```vim\r\ndd	删除（剪切）光标所在整行\r\n5dd	删除（剪切）从光标处开始的5行\r\nyy	复制光标所在整行\r\n5yy	复制从光标处开始的5行\r\nn	显示搜索命令定位到的下一个字符串\r\nN	显示搜索命令定位到的上一个字符串\r\nu	撤销上一步的操作\r\np	将之前删除（dd）或复制（yy）过的数据粘贴到光标后面\r\n```\r\n#### 末行模式\r\n##### 末行模式主要用于保存或退出文件，以及设置Vim编辑器的工作环境，还可以让用户执行外部的Linux命令或跳转到所编写文档的特定行数。要想切换到末行模式，在命令模式中输入一个冒号就可以了\r\n\r\n```bash\r\n\r\n命令	作用\r\n:w	保存\r\n:q	退出\r\n:q!	强制退出（放弃对文档的修改内容）\r\n:wq!	强制保存退出\r\n:set nu	显示行号\r\n:set nonu	不显示行号\r\n:命令	执行该命令\r\n:整数	跳转到该行\r\n:s/one/two	将当前光标所在行的第一个one替换成two\r\n:s/one/two/g	将当前光标所在行的所有one替换成two\r\n:%s/one/two/g	将全文中的所有one替换成two\r\n?字符串	在文本中从下至上搜索该字符串\r\n/字符串\r\n```	\r\n\r\n\r\n- 复制一行\r\n\r\nlinux vi面板如何复制一行\r\n把光标移动到要复制的行上\r\n按yy\r\n把光标移动到要复制的位置\r\n按p\r\n- 删除一行 \r\n:dd\r\n- 剪切一行\r\ndd\r\n- 设置显示行号\r\n:set nu(number)\r\n- 多行注释\r\n```bash\r\n:<<!\r\n# 要注释的内容\r\n!\r\n\r\n```\r\n\r\n\r\n```bash\r\n\r\n# 查找\r\n?要查找的内容\r\n# 将光标移动到要查找的单词上\r\nshift+*\r\n\r\n\r\n```','2022-01-04 11:00:24.629185','2022-01-04 11:00:44.792918',1,2,6,'article_svg/20220104/vector_landscape_1.svg');
/*!40000 ALTER TABLE `articlesapp_articlepost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articlesapp_category`
--

DROP TABLE IF EXISTS `articlesapp_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articlesapp_category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articlesapp_category`
--

LOCK TABLES `articlesapp_category` WRITE;
/*!40000 ALTER TABLE `articlesapp_category` DISABLE KEYS */;
INSERT INTO `articlesapp_category` VALUES (1,'Django','2021-12-26 12:22:00.000000'),(2,'Machine Learning','2021-12-26 12:23:00.000000'),(3,'Deep Learning','2021-12-26 12:23:00.000000'),(4,'Object Detection','2021-12-26 12:24:00.000000'),(5,'Face Recognition','2021-12-28 07:25:00.000000'),(6,'Linux','2021-12-28 07:27:00.000000'),(7,'Python','2021-12-28 07:27:00.000000'),(8,'Other','2021-12-28 07:27:00.000000'),(9,'Algorithm','2021-12-28 07:28:00.000000');
/*!40000 ALTER TABLE `articlesapp_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add article post',7,'add_articlepost'),(26,'Can change article post',7,'change_articlepost'),(27,'Can delete article post',7,'delete_articlepost'),(28,'Can view article post',7,'view_articlepost'),(29,'Can add comment',8,'add_comment'),(30,'Can change comment',8,'change_comment'),(31,'Can delete comment',8,'delete_comment'),(32,'Can view comment',8,'view_comment'),(33,'Can add category',9,'add_category'),(34,'Can change category',9,'change_category'),(35,'Can delete category',9,'delete_category'),(36,'Can view category',9,'view_category'),(37,'Can add tag',10,'add_tag'),(38,'Can change tag',10,'change_tag'),(39,'Can delete tag',10,'delete_tag'),(40,'Can view tag',10,'view_tag'),(41,'Can add tagged item',11,'add_taggeditem'),(42,'Can change tagged item',11,'change_taggeditem'),(43,'Can delete tagged item',11,'delete_taggeditem'),(44,'Can view tagged item',11,'view_taggeditem'),(45,'Can add 资源链接',12,'add_resources'),(46,'Can change 资源链接',12,'change_resources'),(47,'Can delete 资源链接',12,'delete_resources'),(48,'Can view 资源链接',12,'view_resources');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$260000$naKULCCGeIviAQqyC4t1MG$Zgdg1FSs2XNHK0+4GN0iQ/bO19K5yJzySKdnzxuYuts=','2022-01-04 00:28:46.867138',1,'zhouqiang','','','zhouqiangweek@foxmail.com',1,1,'2021-12-22 12:45:16.255119');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_comment`
--

DROP TABLE IF EXISTS `comment_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_comment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `body` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `article_id` bigint(20) NOT NULL,
  `critic` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_comment_article_id_3cc364fc_fk_articlesa` (`article_id`),
  CONSTRAINT `comment_comment_article_id_3cc364fc_fk_articlesa` FOREIGN KEY (`article_id`) REFERENCES `articlesapp_articlepost` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_comment`
--

LOCK TABLES `comment_comment` WRITE;
/*!40000 ALTER TABLE `comment_comment` DISABLE KEYS */;
INSERT INTO `comment_comment` VALUES (21,'<p>留言&hellip;&hellip;😁!</p>','2021-12-25 15:00:43.834547',4,':spouting_whale:'),(22,'留言……😁!','2021-12-27 07:21:32.639151',35,':person_wearing_turban:'),(23,'<pre>\r\n<code class=\"language-python\">\r\n\r\ndef getN(N):\r\n    n = 0\r\n    while n&lt;N:\r\n        yield n\r\n        n+=1\r\ng = getN(10)\r\nwhile True:\r\n    try:\r\n        print(next(g),end=\'\\t\')\r\n    except StopIteration:\r\n        break #跳出循环\r\n</code></pre>\r\n\r\n<p>&nbsp;</p>','2021-12-27 14:26:33.748786',47,'A'),(24,'留言……😁!','2021-12-28 03:15:06.623141',47,':princess:'),(25,'# 1\r\n## 2\r\n### 3','2021-12-28 03:15:30.842558',47,':deciduous_tree:'),(26,'# Linux之vi 操作\r\n\r\n#### 命令模式\r\n\r\n##### 在每次运行Vim编辑器时，默认进入命令模式，此时需要先切换到输入模式后再进行文档编写工作，而每次在编写完文档后需要先返回命令模式，然后再进入末行模式，执行文档的保存或退出操作。在Vim中，无法直接从输入模式切换到末行模式。\r\n```vim\r\ndd	删除（剪切）光标所在整行\r\n5dd	删除（剪切）从光标处开始的5行\r\nyy	复制光标所在整行\r\n5yy	复制从光标处开始的5行\r\nn	显示搜索命令定位到的下一个字符串\r\nN	显示搜索命令定位到的上一个字符串\r\nu	撤销上一步的操作\r\np	将之前删除（dd）或复制（yy）过的数据粘贴到光标后面','2021-12-28 03:21:17.451482',47,':pig_face:');
/*!40000 ALTER TABLE `comment_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-12-22 12:47:00.356155','1','搭建个人博客笔记',1,'[{\"added\": {}}]',7,1),(2,'2021-12-22 12:48:59.586909','2','搭建个人博客（2）',1,'[{\"added\": {}}]',7,1),(3,'2021-12-22 15:38:49.648311','2','搭建个人博客（2）',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',7,1),(4,'2021-12-23 01:12:19.484564','3','目标检测算法之yolo系列（1）',1,'[{\"added\": {}}]',7,1),(5,'2021-12-23 03:48:02.093586','5','Linux之Vim操作',3,'',7,1),(6,'2021-12-24 16:49:51.196951','5','',3,'',8,1),(7,'2021-12-25 14:47:10.008199','2','留言……',3,'',8,1),(8,'2021-12-25 14:47:10.012539','3','留言……!',3,'',8,1),(9,'2021-12-25 14:47:10.013729','4','留言……',3,'',8,1),(10,'2021-12-25 14:47:10.014935','6','留言……!',3,'',8,1),(11,'2021-12-25 14:47:10.015619','7','111',3,'',8,1),(12,'2021-12-25 14:52:25.961303','2','留言……',3,'',8,1),(13,'2021-12-25 14:52:25.966218','3','留言……!',3,'',8,1),(14,'2021-12-25 14:52:25.967294','4','留言……',3,'',8,1),(15,'2021-12-25 14:52:25.969501','6','留言……!',3,'',8,1),(16,'2021-12-25 14:52:25.976315','7','111',3,'',8,1),(17,'2021-12-25 14:57:46.128206','1','hhh',3,'',8,1),(18,'2021-12-25 14:57:56.019707','10','',3,'',8,1),(19,'2021-12-25 14:58:35.564386','8','留言……!',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',8,1),(20,'2021-12-25 14:58:42.717312','8','留言……!',3,'',8,1),(21,'2021-12-25 14:58:49.615582','12','',3,'',8,1),(22,'2021-12-25 14:58:56.902008','14','',3,'',8,1),(23,'2021-12-25 14:59:03.416558','16','',3,'',8,1),(24,'2021-12-25 15:00:04.283021','9','留言……!',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',8,1),(25,'2021-12-25 15:00:12.872579','11','留言……!',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',8,1),(26,'2021-12-25 15:00:20.650490','13','留言……!',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',8,1),(27,'2021-12-25 15:00:26.071661','17','留言……!',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',8,1),(28,'2021-12-25 15:00:36.080834','2','留言……',3,'',8,1),(29,'2021-12-25 15:00:36.083647','3','留言……!',3,'',8,1),(30,'2021-12-25 15:00:36.085175','4','留言……',3,'',8,1),(31,'2021-12-25 15:00:36.088071','6','留言……!',3,'',8,1),(32,'2021-12-25 15:00:36.089639','7','111',3,'',8,1),(33,'2021-12-25 15:00:36.091221','9','留言……!',3,'',8,1),(34,'2021-12-25 15:00:36.094745','11','留言……!',3,'',8,1),(35,'2021-12-25 15:00:36.097123','13','留言……!',3,'',8,1),(36,'2021-12-25 15:00:36.097925','15','留言……!',3,'',8,1),(37,'2021-12-25 15:00:36.099032','17','留言……!',3,'',8,1),(38,'2021-12-25 15:00:36.099925','18','njnjnj',3,'',8,1),(39,'2021-12-25 15:00:36.100730','19','留言bjhjhjn',3,'',8,1),(40,'2021-12-25 15:00:36.101482','20','hjhjjjknkj',3,'',8,1),(41,'2021-12-26 12:23:23.063557','1','Django',1,'[{\"added\": {}}]',9,1),(42,'2021-12-26 12:23:44.390416','2','Machine Learning',1,'[{\"added\": {}}]',9,1),(43,'2021-12-26 12:24:07.987775','3','Deep Learning',1,'[{\"added\": {}}]',9,1),(44,'2021-12-26 12:24:48.941023','4','目测检测',1,'[{\"added\": {}}]',9,1),(45,'2021-12-26 12:25:48.894458','3','目标检测算法之yolo系列(1)',2,'[{\"changed\": {\"fields\": [\"Column\"]}}]',7,1),(46,'2021-12-26 12:26:23.501625','2','搭建个人博客（2）',2,'[{\"changed\": {\"fields\": [\"Column\"]}}]',7,1),(47,'2021-12-26 12:26:43.395081','1','搭建个人博客笔记',2,'[{\"changed\": {\"fields\": [\"Column\"]}}]',7,1),(48,'2021-12-27 01:28:50.650236','9','Django之测试上传文章封面',2,'[{\"changed\": {\"fields\": [\"Avatar\"]}}]',7,1),(49,'2021-12-27 01:29:09.213913','8','bjbnj',3,'',7,1),(50,'2021-12-27 01:29:09.217214','7','jnj',3,'',7,1),(51,'2021-12-27 01:32:29.477763','6','目标检测之yolox',2,'[]',7,1),(52,'2021-12-27 01:39:17.795205','6','目标检测之yolox',2,'[{\"changed\": {\"fields\": [\"Avatar\"]}}]',7,1),(53,'2021-12-27 01:39:36.676663','5','目标检测yolov2',2,'[{\"changed\": {\"fields\": [\"Avatar\"]}}]',7,1),(54,'2021-12-27 02:59:53.362027','19','Django之测试上传文章封面',2,'[]',7,1),(55,'2021-12-27 03:28:31.938711','25','河南省今年',3,'',7,1),(56,'2021-12-27 03:28:31.942275','24','河南省今年',3,'',7,1),(57,'2021-12-27 03:28:31.943650','23','河南省今年',3,'',7,1),(58,'2021-12-27 03:28:31.945080','22','河南省今年',3,'',7,1),(59,'2021-12-27 03:36:48.548998','19','Django之测试上传文章封面',3,'',7,1),(60,'2021-12-27 03:36:48.553085','18','Django之测试上传文章封面',3,'',7,1),(61,'2021-12-27 03:36:57.387006','17','Django之测试上传文章封面',3,'',7,1),(62,'2021-12-27 03:36:57.389549','16','Django之测试上传文章封面',3,'',7,1),(63,'2021-12-27 03:36:57.390416','15','Django之测试上传文章封面',3,'',7,1),(64,'2021-12-27 03:36:57.392964','14','Django之测试上传文章封面',3,'',7,1),(65,'2021-12-27 03:37:07.171472','13','Django之测试上传文章封面',3,'',7,1),(66,'2021-12-27 03:37:07.174325','12','Django之测试上传文章封面',3,'',7,1),(67,'2021-12-27 03:37:07.175171','11','Django之测试上传文章封面',3,'',7,1),(68,'2021-12-27 03:37:07.175964','10','Django之测试上传文章封面',3,'',7,1),(69,'2021-12-27 03:37:07.176878','9','Django之测试上传文章封面',3,'',7,1),(70,'2021-12-27 06:23:23.935247','33','sdsd',3,'',7,1),(71,'2021-12-27 06:23:23.937311','29','k',3,'',7,1),(72,'2021-12-27 14:26:33.751433','23','<pre>\r\n<code class=\"',1,'[{\"added\": {}}]',8,1),(73,'2021-12-28 02:14:51.697584','21','<p>留言&hellip;&hellip',2,'[{\"changed\": {\"fields\": [\"Body\"]}}]',8,1),(74,'2021-12-28 07:08:49.947493','10','dfds',3,'',10,1),(75,'2021-12-28 07:08:49.949399','9','dsds',3,'',10,1),(76,'2021-12-28 07:08:49.950336','3','jnjn',3,'',10,1),(77,'2021-12-28 07:08:49.950883','8','klll',3,'',10,1),(78,'2021-12-28 07:08:49.951400','25','L',3,'',10,1),(79,'2021-12-28 07:08:49.951882','7','mm',3,'',10,1),(80,'2021-12-28 07:08:49.952387','2','nj',3,'',10,1),(81,'2021-12-28 07:08:49.952910','24','O',3,'',10,1),(82,'2021-12-28 07:08:49.953384','23','Y',3,'',10,1),(83,'2021-12-28 07:08:49.953844','1','yolox',3,'',10,1),(84,'2021-12-28 07:08:49.954742','12','五',3,'',10,1),(85,'2021-12-28 07:08:49.955313','27','列',3,'',10,1),(86,'2021-12-28 07:08:49.955848','18','图',3,'',10,1),(87,'2021-12-28 07:08:49.956434','4','图片封面',3,'',10,1),(88,'2021-12-28 07:08:49.957263','20','封',3,'',10,1),(89,'2021-12-28 07:08:49.957744','6','没有图片封面',3,'',10,1),(90,'2021-12-28 07:08:49.958162','29','测试',3,'',10,1),(91,'2021-12-28 07:08:49.958585','16','片',3,'',10,1),(92,'2021-12-28 07:08:49.959002','22','系',3,'',10,1),(93,'2021-12-28 07:08:49.959396','14','面',3,'',10,1),(94,'2021-12-28 07:25:32.798404','4','Object Detect',2,'[{\"changed\": {\"fields\": [\"Title\"]}}]',9,1),(95,'2021-12-28 07:26:01.780627','5','Face Recoginition',1,'[{\"added\": {}}]',9,1),(96,'2021-12-28 07:27:08.926220','5','Face Recognition',2,'[{\"changed\": {\"fields\": [\"Title\"]}}]',9,1),(97,'2021-12-28 07:27:23.586603','6','Linux',1,'[{\"added\": {}}]',9,1),(98,'2021-12-28 07:27:40.484885','7','Python',1,'[{\"added\": {}}]',9,1),(99,'2021-12-28 07:27:54.244320','8','Other',1,'[{\"added\": {}}]',9,1),(100,'2021-12-28 07:28:56.975104','9','Algothrim',1,'[{\"added\": {}}]',9,1),(101,'2021-12-30 23:06:57.148259','1','Resources object (1)',1,'[{\"added\": {}}]',12,1),(102,'2021-12-31 09:52:10.035003','3','Resources object (3)',1,'[{\"added\": {}}]',12,1),(103,'2021-12-31 10:58:11.467591','4','Resources object (4)',1,'[{\"added\": {}}]',12,1),(104,'2021-12-31 14:13:41.522236','6','Resources object (6)',1,'[{\"added\": {}}]',12,1),(105,'2021-12-31 22:55:34.537472','32','',3,'',10,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(7,'articlesapp','articlepost'),(9,'articlesapp','category'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(8,'comment','comment'),(5,'contenttypes','contenttype'),(12,'resourceapp','resources'),(6,'sessions','session'),(10,'taggit','tag'),(11,'taggit','taggeditem');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-12-22 12:41:07.426549'),(2,'auth','0001_initial','2021-12-22 12:41:07.936898'),(3,'admin','0001_initial','2021-12-22 12:41:08.059336'),(4,'admin','0002_logentry_remove_auto_add','2021-12-22 12:41:08.072227'),(5,'admin','0003_logentry_add_action_flag_choices','2021-12-22 12:41:08.080690'),(6,'articlesapp','0001_initial','2021-12-22 12:41:08.150845'),(7,'contenttypes','0002_remove_content_type_name','2021-12-22 12:41:08.221597'),(8,'auth','0002_alter_permission_name_max_length','2021-12-22 12:41:08.261386'),(9,'auth','0003_alter_user_email_max_length','2021-12-22 12:41:08.298520'),(10,'auth','0004_alter_user_username_opts','2021-12-22 12:41:08.304209'),(11,'auth','0005_alter_user_last_login_null','2021-12-22 12:41:08.341318'),(12,'auth','0006_require_contenttypes_0002','2021-12-22 12:41:08.343401'),(13,'auth','0007_alter_validators_add_error_messages','2021-12-22 12:41:08.348915'),(14,'auth','0008_alter_user_username_max_length','2021-12-22 12:41:08.386019'),(15,'auth','0009_alter_user_last_name_max_length','2021-12-22 12:41:08.423197'),(16,'auth','0010_alter_group_name_max_length','2021-12-22 12:41:08.457851'),(17,'auth','0011_update_proxy_permissions','2021-12-22 12:41:08.465038'),(18,'auth','0012_alter_user_first_name_max_length','2021-12-22 12:41:08.502791'),(19,'sessions','0001_initial','2021-12-22 12:41:08.555831'),(20,'articlesapp','0002_articlepost_total_views','2021-12-23 15:01:41.661523'),(21,'comment','0001_initial','2021-12-24 13:39:38.222510'),(22,'comment','0002_auto_20211224_2254','2021-12-24 14:55:01.701466'),(23,'articlesapp','0003_auto_20211226_2021','2021-12-26 12:22:07.687067'),(24,'taggit','0001_initial','2021-12-26 13:11:46.632725'),(25,'taggit','0002_auto_20150616_2121','2021-12-26 13:11:46.667120'),(26,'taggit','0003_taggeditem_add_unique_index','2021-12-26 13:11:46.705816'),(27,'articlesapp','0004_articlepost_tags','2021-12-26 13:11:46.718350'),(28,'articlesapp','0005_articlepost_cover','2021-12-26 14:33:24.494834'),(29,'articlesapp','0006_remove_articlepost_cover','2021-12-26 14:55:07.248961'),(30,'articlesapp','0007_articlepost_avatar','2021-12-27 01:11:09.475627'),(31,'articlesapp','0008_alter_articlepost_avatar','2021-12-27 04:43:52.134441'),(32,'articlesapp','0009_remove_articlepost_avatar','2021-12-27 04:45:03.725033'),(33,'articlesapp','0010_articlepost_avatar','2021-12-27 04:47:43.321573'),(34,'articlesapp','0011_alter_articlepost_avatar','2021-12-27 05:09:39.961863'),(35,'articlesapp','0012_auto_20211227_1626','2021-12-27 08:26:23.578258'),(36,'articlesapp','0013_alter_articlepost_avatar2','2021-12-27 08:44:17.947225'),(37,'articlesapp','0014_auto_20211227_1703','2021-12-27 09:03:31.050340'),(38,'articlesapp','0015_remove_articlepost_avatar_img','2021-12-27 09:10:33.492676'),(39,'comment','0003_alter_comment_body','2021-12-27 14:12:32.587318'),(40,'resourceapp','0001_initial','2021-12-30 23:00:41.713914'),(41,'resourceapp','0002_alter_resources_options','2021-12-30 23:02:51.554243'),(42,'resourceapp','0003_resources_url2','2021-12-31 10:56:06.152103');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('93i6fm2n75s876gr44kwu298v3k8y4n5','e30:1n0I0R:HsoUQGb03v0vOkNGxc-zXWNvSF2dgj-bcWUz_U1TclI','2022-01-06 06:55:15.434912');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_resource`
--

DROP TABLE IF EXISTS `t_resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_resource` (
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
  `download_count` int(11) NOT NULL,
  `url2` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_resource`
--

LOCK TABLES `t_resource` WRITE;
/*!40000 ALTER TABLE `t_resource` DISABLE KEYS */;
INSERT INTO `t_resource` VALUES ('2021-12-30 23:03:00.000000','2022-01-02 13:28:35.174889',1,'emoji.txt','media/resources/emoji.txt',9,'resources/emoji.txt'),('2021-12-31 10:56:00.000000','2022-01-02 13:28:47.544448',4,'1706-transformer.pdf','media/resources/1706-transformer.pdf',8,'resources/1706-transformer.pdf'),('2021-12-31 11:09:10.000000','2022-01-02 13:28:43.901120',5,'图像分割论文.JPG','media/resources/图像分割论文.JPG',218,'resources/图像分割论文.JPG'),('2021-12-31 14:10:00.000000','2022-01-04 11:12:44.275412',6,'Encanto.torrent','media/resources/Encanto.torrent',9,'resources/Encanto.torrent');
/*!40000 ALTER TABLE `t_resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taggit_tag`
--

DROP TABLE IF EXISTS `taggit_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taggit_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taggit_tag`
--

LOCK TABLES `taggit_tag` WRITE;
/*!40000 ALTER TABLE `taggit_tag` DISABLE KEYS */;
INSERT INTO `taggit_tag` VALUES (30,'测试',''),(33,'yolov1','yolov1'),(35,'单阶段检测算法','_2'),(36,'markdown','markdown'),(37,'django','django'),(39,'目标检测','_3'),(40,'command','command');
/*!40000 ALTER TABLE `taggit_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taggit_taggeditem`
--

DROP TABLE IF EXISTS `taggit_taggeditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taggit_taggeditem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taggit_taggeditem_content_type_id_object_id_tag_id_4bb97a8e_uniq` (`content_type_id`,`object_id`,`tag_id`),
  KEY `taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id` (`tag_id`),
  KEY `taggit_taggeditem_object_id_e2d7d1df` (`object_id`),
  KEY `taggit_taggeditem_content_type_id_object_id_196cc965_idx` (`content_type_id`,`object_id`),
  CONSTRAINT `taggit_taggeditem_content_type_id_9957a03c_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `taggit_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taggit_taggeditem`
--

LOCK TABLES `taggit_taggeditem` WRITE;
/*!40000 ALTER TABLE `taggit_taggeditem` DISABLE KEYS */;
INSERT INTO `taggit_taggeditem` VALUES (52,1,7,37),(50,2,7,36),(51,2,7,37),(53,3,7,33),(54,3,7,35),(45,46,7,30),(55,48,7,39),(57,49,7,40);
/*!40000 ALTER TABLE `taggit_taggeditem` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-05 15:29:17
