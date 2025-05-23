# 按照款号整理好的文件夹

```
cd /Users/chenfangwei/Desktop/python-erpimage
source ./venv/bin/activate
python main.py <dir>

# 成功之后
scp <output_dir>/* tencent:/srv/www/goserver-wms-dev/images/<品牌>
```

`<dir>`例如兄华，箐箐贵族

# 平铺的文件夹

```
python main.py <dir> -f  # flattern
```





