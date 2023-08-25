# AWD动态防守PLUS

## 部署

我们直接在实体机部署，修改两个文件里的ssh信息和路径信息。

```
hostname = 'x.x.x.x'
username = 'xxxxx'
password = 'xxxx'
directory_path = '/var/www/html'
```

## 使用

在比赛中运行`get_avoid_file_list.py`

接着会生成一个`avoid_file_list.txt`，这个文件里面保存的是初始文件路径列表，如果出现不合理的文件，直接在文档里删掉这个路径。

接着运行`monitoring.py`

这样会自动删除不在列表中的文件，已经在列表中的文件则不会变动。

## 说明

和普通版的唯一区别，就是多了个文件规避列表，区分哪些是正常文件和非正常文件。方便CTFer少动手，多动脑。