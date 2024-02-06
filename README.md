# Сервис мониторинга продаж масштабных моделей (Формулы 1) на Ebay

### _Проект выполнен в рамках курса Otus - Python Developper. Basic_

## Описание основного use case сценария
Пользователь заполняет форму, указывая основную информацию о модели или же вставляет ссылку с ebay (на данный момент
более эффективный вариант ввиду большого количества доп. информации, которую желательно/необходимо указать для 
нахождения конкретной модели). Затем происходит парсинг страницы с дальнейшим занесением модели в коллекцию пользователя, 
а так же появляется информация о каждой проданной модели за последние 90 дней (максимально доступный интервал, который
предоставляет Ebay). При переходе на страницу коллекции один раз в день происходить расчет минимальной и максимальной цены
коллекции на основе полученных цен моделей (или пользователь самостоятельно может стригерить расчет по кнопке)