# caimg
for MetaFluor data analysis

## caimg.py for python
still under active development

Usage:
```Python
drawpic(fileName + '.xlsx')
```

## Experiment.m for MatLab
dormant state (last update: May, 2016)

Usage:
```Matlab
[~, sheets] = xlsfinfo(char(fileName));
sheetName = sheets(1)

exp = Experiment(fileName, sheetName);
exp = exp.normalize();
h = exp.plot();  
```

example: test.m
