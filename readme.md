## Хабрапрокси

Простой http-прокси-сервер, запускаемый локально, который показывает содержимое страниц Хабра. Прокси модифицирует текст на страницах следующим образом: после каждого слова из шести букв должен стоять значок «™».
При навигации по ссылкам, которые ведут на другие страницы хабра, браузер остаётся на адресе прокси

Запуск: `docker-compose up --build`
Локальная установка: `./cli/install.sh`
Локальный запуск: `./cli/start.sh`
Тесты: `./cli/tests.sh`
