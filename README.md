# rss 数据入库

![fetch rss to mysql](https://github.com/lizhaode/nyaa-rss/workflows/fetch%20rss%20to%20mysql/badge.svg)

`https://sukebei.nyaa.si/` 提供的 RSS 拉取

## 用法

- fork 这个项目
- 在你的 MySQL 中执行 `rss.sql` 创建表
- 在配置中的 `Secrects` 下创建 `host` `user` `passowrd` `database` `port`


## 功能

每隔一个小时，就会拉取一次 RSS 的内容更新到数据库中
