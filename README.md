# 使用Django搭建个人博客
---

## 项目简介

- 使用`Python Django`框架作为网站后端, 开发个人博客

---
## 部署方案

- 部署环境: `ubuntu server 18.04` (阿里云)
- Lnmp方案: `Linux` + `Nginx` + `MariaDB` + `Python Django` (with `Gunicorn`) 

---
## 开发环境

- 系统环境: `Manjaro Linux 18` (社区版DDE桌面)

---
## 前端

- `Materialize` v1.0.0 (快速实现谷歌的`Materia Design`设计风格)
- `jQuery` v3.4.1 (实现Ajax和DOM操作)
- `Editor.md` v1.5.0 (开源在线Markdown编辑器)
- `FontAwesome` v4.7.0 (使用部分图标)

---
## 后端

- `Django` v2.2.4 (2.2为LTS长期支持版本)
- `MariaDB` v10.4.7
- `Nginx`

---
## 主站更新日志

### v0.9.5(第二版)

发布日期: 2019-08-28

#### 代码风格优化

- python和js中尽量使用单引号, 网页模板中以双引号为主
- 后端API命名更加整齐规范
- 更多的强迫症细节

#### 前端细节修改

- 更多的使用Materialize框架的CSS类和js方法: [Document](https://materializecss.com)

#### views.py

- 视图函数中使用视图装饰器: [View decorators-Allowed HTTP methods](https://docs.djangoproject.com/zh-hans/2.2/topics/http/decorators/)

#### base.html

- footer Copyright年份自动更新
- footer grid调整
- 管理员选项迁移到fixed-action-btn中
- 导航栏使用container自动调整宽度

#### 管理员登录页面

- 管理员登录页面回车键快速登录(回车触发按钮点击事件)
- 为了移动端的体验更美观统一, 管理员登录页面弹窗弃用alter, 采用materialize框架中的对话框实现
- 上述弹窗可以用回车键确认

#### Admin页面

- 页面汉化
- 优化多对多关系的格式化输出

#### 文章上传页面

- form表单使用grid动态调整宽度
- `input file` js校验文件类型
- 使用ajax实现多选输入的即时新增选项(实为数据对象)
- 使用H5 sessionStorage 实现刷新后保留输入的数据, 但是之前上传的本地文件需要重新上传


#### 文章模型

- 支持多作者
- 博客文章以markdown文件的形式储存

#### 文章预览页面

- 解决Materialize框架与Editor.md框架在预定义CSS上的冲突

#### 文章二次编辑页面

- 新增文章二次编辑页面

#### 主页

- 使用container自动调整宽度
- 新增侧栏
- 子页面多重继承网页模板

#### 主页侧栏

- 新增头像card
- 新增网站简介card
- 新增作者/分类/标签card
- 新增精选项目card
- 新增友链card
- 新增音乐播放器card

#### 子页面

- 新增tags子页面
- 新增categories子页面
- 新增authors子页面

#### .gitignore

- 忽略所有上传文件

#### 图片上传页面

- js功能和代码风格优化

#### 图片浏览界面

- 界面全新设计, 取消原瀑布流方案

---

### v0.9.0(第一版)

发布日期: 2019-03-08

- 添加移动端导航侧栏
- 添加管理员登录页面
- 添加在线图床功能, 包括上传页面和总览页面, 总览页面采用瀑布流方案
- 文章上传页面采用开源项目`Editor.md`作为markdown在线编辑器
- 实现文章点击量的统计和显示
- 添加读书专栏
- 添加关于页面
- 以及个人博客该有的其他基本功能