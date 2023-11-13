# БТ. Заказ от Федерации Спортивного Туризма России (ФСТР)
Когда турист поднимется на перевал, он сфотографирует его и внесёт нужную информацию с помощью мобильного приложения:
 - координаты объекта и его высоту;
 - название объекта;
 - несколько фотографий;
 - информацию о пользователе, который передал данные о перевале:
     - имя пользователя (ФИО строкой);
     - почта;
     - телефон.
После этого турист нажмёт кнопку «Отправить» в мобильном приложении. Мобильное приложение вызовет метод submitData твоего REST API.


# Описание реализации.
В рамках данного проекта создана база данных, написаны классы по работе с БД и реализованы следующие методы для Rest API:
1. Метод POST submitData (http://127.0.0.1:8000/submitData/).
    Метод submitData принимает JSON в теле запроса с информацией о перевале. Предоставленный пример такого JSON-а:
    {
      "beauty_title": "пер. ",
      "title": "Пхия",
      "other_titles": "Триев",
      "connect": "",
      "add_time": "2021-09-22 13:18:13",
      "user": {"email": "qwerty@mail.ru",
            "fam": "Пупкин",
    		 "name": "Василий",
		     "otc": "Иванович",
            "phone": "+7 555 55 55"},
      "coords":{
      "latitude": "45.3842",
      "longitude": "7.1525",
      "height": "1200"},
      "level":{"winter": "",
      "summer": "1А",
      "autumn": "1А",
      "spring": ""},
      "images": [{"data":"<картинка1>", "title":"Седловина"}, {"data":"<картинка>", "title":"Подъём"}]
    }

    Результат выполнения метода: JSON
     - status — код HTTP, целое число:
         - 500 — ошибка при выполнении операции;
         - 400 — Bad Request (при нехватке полей);
         - 200 — успех.
     - message — строка:
         - Причина ошибки (если она была);
         - Отправлено успешно;
         - Если отправка успешна, дополнительно возвращается id вставленной записи.
     - id — идентификатор, который был присвоен объекту при добавлении в базу данных.

    Примеры:
     - { "status": 500, "message": "Ошибка подключения к базе данных","id": null}
     - { "status": 200, "message": null, "id": 42 }

    Выполенные в спринте-1 задачи:
        1. Создание базы данных.
        2. Создание класса по работе с данными (добавление новых значений в таблицу перевалов).
        3. Написание REST API, вызывающего метод из класса по работе с данными.

3. Метод GET /submitData/<id>
    Например: http://127.0.0.1:8000/get/submitData/8
    Это метод получения одной записи (перевала) по её id.
    Выводит всю информацию об объекте, в том числе статус модерации.

4. Метод PATCH /submitData/<id>
    Например: http://127.0.0.1:8000/patch/submitData/8
    Редактирование существующей записи (замена), если она в статусе new.
    Редактировать можно все поля, кроме тех, что содержат в себе ФИО, адрес почты и номер телефона.
    Метод принимает тот же самый json, обработка которого реализована в методе submitData.
    В качестве результата возвращает два значения:
         - status=status.HTTP_200_OK — если успешно удалось отредактировать запись в базе данных.
         - status=status.HTTP_400_BAD_REQUEST — в противном случае.
             * message — текст стандартный для указанных статусов .
    
    * Принимаемый на фход json в общем случае такой же, но для корректного обновления нужно оставлять в нем только изменяемые элементы
    * Обращаю внимание, что обновление координат объекта происходит через отдельный сериализатор (get-coords/submitData/<int:pk>): http://127.0.0.1:8000/get-coords/submitData/8
    * В данной реализации информация о пользователе выводится в виде его ID. Редактирование информации о пользователе фактически запрещена
    * Реализован просмотр статуса: http://127.0.0.1:8000/get-status/submitData/2

5. GET /submitData/?user__email=<email>
    Например: http://127.0.0.1:8000/](http://127.0.0.1:8000/get-useremail/submitData/?user__email=qwerty11@mail.ru)
    Получить список данных обо всех объектах, которые пользователь с почтой <email> отправил на сервер.
