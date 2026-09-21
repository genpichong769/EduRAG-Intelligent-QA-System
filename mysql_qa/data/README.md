# FAQ source data

本目录用于存放导入 MySQL 的本地 FAQ 数据。原始 FAQ CSV 含内部地址与课程数据，因此不进入 Git。

CSV 至少需要以下三列：

```text
学科名称,问题,答案
```

`MySQLClient.create_table()` 会创建 `jpkb` 表，`MySQLClient.insert_data(csv_path)` 会导入上述列。请仅使用有权公开或处理的数据。
