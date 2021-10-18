Запуск линтера:
```bash
flake8 --max-line-length=120 '.\HW 01\'
cd '.\HW 01\' && pylint --max-line-length=120 '.\tictacgame' && cd ..
```

Запуск тестов:
```bash
py.test '.\HW 01\tests.py' --cov-append --cov-report xml:cov.xml --cov tictacgame --cov tests
```

Запуск игры:
```bash
python '.\HW 01\main.py' -h
>>> usage: main.py [-h] [-n N_ROWS] [-k N_COLUMNS] [-p N_MARKS]
>>> 
>>> optional arguments:
>>> -h, --help            show this help message and exit    
>>> -n N_ROWS, --n_rows N_ROWS
>>> -k N_COLUMNS, --n_columns N_COLUMNS
>>> -p N_MARKS, --n_marks N_MARKS

python '.\HW 01\main.py'
```
