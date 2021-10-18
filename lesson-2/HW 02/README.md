Запуск линтера:
```bash
flake8 --max-line-length=120 '.\HW 02\'
cd '.\HW 02\' && pylint --max-line-length=120 '.\custom_list' && pylint --max-line-length=120 '.\custom_meta' && cd ..
```

Запуск тестов:
```bash
py.test 'HW 02' --cov-append --cov-report xml:cov.xml --cov custom_list --cov custom_meta
```
