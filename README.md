# Django_coursework

Проект "Основы веб-разработки на Django": сервис управления рассылками, администрирования и получения статистики.

Проект содержит три приложения: сервис управления (management_service), пользователи (users) и блог со статьями (blog).

Сущности системы management_service:
* Клиент сервиса (Client)
* Рассылка (Mailing)
* Сообщение для рассылки (Message)
* Логи рассылки (MailingLogs)




Запуск рассылок через команды: `mailing_day, mailing_week или mailing_month`.

Запуск рассылки осуществляется при помощи cron. Пример настройки cron: 

```
*/30 * * * * python3 path_to_project/Django_coursework/manage.py mailing_day
@daily python3 path_to_project/Django_coursework/manage.py mailing_week
@weekly python3 path_to_project/Django_coursework/manage.py mailing_month
```

Запуск сайта: `runserver`.




