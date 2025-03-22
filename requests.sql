SELECT* FROM studied_users;
select *  from users;
select * from words;

insert into words(word_eng,word_rus)
values 
('Cat','Кот'),
('Dog','Собака'),
('Book','Книга'),
('Table','Стол'),
('Chair','Стул'),
('House','Дом'),
('Water','Вода'),
('Food','Еда'),
('Sun','Солнце'),
('Tree','Дерево');
insert into words(word_eng,word_rus)
values 
('Car', 'Машина'),
('Street', 'Улица'),
('School', 'Школа'),
('City', 'Город'),
('Friend', 'Друг'),
('Family', 'Семья'),
('Music', 'Музыка'),
('Love', 'Любовь'),
('Game', 'Игра'),
('Light', 'Свет'),
('Night', 'Ночь'),
('Day', 'День'),
('Phone', 'Телефон'),
('Computer', 'Компьютер'),
('Hand', 'Рука'),
('Foot', 'Нога'),
('Eye', 'Глаз'),
('Heart', 'Сердце'),
('Dream', 'Сон'),
('Voice', 'Голос'),
('Door', 'Дверь'),
('Window', 'Окно'),
('Floor', 'Пол'),
('Roof', 'Крыша'),
('Sky', 'Небо'),
('Cloud', 'Облако'),
('Rain', 'Дождь'),
('Snow', 'Снег'),
('Wind', 'Ветер'),
('Fire', 'Огонь'),
('Ice', 'Лед'),
('Stone', 'Камень'),
('Beach', 'Пляж'),
('Ocean', 'Океан'),
('Mountain', 'Гора'),
('River', 'Река'),
('Lake', 'Озеро'),
('Sunlight', 'Свет солнца'),
('Shadow', 'Тень'),
('Plant', 'Растение'),
('Flower', 'Цветок'),
('Grass', 'Трава'),
('Fruit', 'Фрукт'),
('Vegetable', 'Овощ'),
('Meat', 'Мясо'),
('Fish', 'Рыба'),
('Bird', 'Птица'),
('Insect', 'Насекомое'),
('Animal', 'Животное'),
('Nature', 'Природа'),
('Health', 'Здоровье'),
('Medicine', 'Медицина'),
('School', 'Школа'),
('Teacher', 'Учитель'),
('Student', 'Ученик'),
('Class', 'Класс'),
('Lesson', 'Урок'),
('Homework', 'Домашнее задание'),
('Exam', 'Экзамен'),
('Bookstore', 'Магазин книг'),
('Library', 'Библиотека'),
('Art', 'Искусство'),
('Dance', 'Танец'),
('Sports', 'Спорт'),
('Exercise', 'Упражнение'),
('Gym', 'Тренажерный зал'),
('Travel', 'Путешествие'),
('Ticket', 'Билет'),
('Airport', 'Аэропорт'),
('Train', 'Поезд'),
('Bus', 'Автобус'),
('Bicycle', 'Велосипед'),
('Road', 'Дорога'),
('Map', 'Карта'),
('Direction', 'Направление'),
('Destination', 'Пункт назначения'),
('Journey', 'Путешествие'),
('Adventure', 'Приключение'),
('Culture', 'Культура'),
('Tradition', 'Традиция'),
('Festival', 'Праздник'),
('Celebration', 'Празднование'),
('Party', 'Вечеринка'),
('Friend', 'Друг'),
('Happiness', 'Счастье'),
('Sadness', 'Печаль'),
('Anger', 'Гнев'),
('Fear', 'Страх'),
('Surprise', 'Удивление'),
('Emotion', 'Эмоция');

--insert into users(name, number_user) values ('Ganja','528679394');

delete from users where userid=3;

delete from studied_users
-- вывод слов рандомных
SELECT word_eng,word_rus
FROM words w 
inner join studied_users su on w.wordid=su.wordid
inner join users u on su.userid=u.userid
where  u.number_user = 528679394 and w.word_eng != 'Cat'
ORDER BY RANDOM()
LIMIT 11;

--добавление нового слова пользователю
insert into studied_users (
SELECT u.userid, w.wordid FROM users u
CROSS JOIN Words w
WHERE u.number_user = 528679394
AND NOT EXISTS (SELECT 1 FROM studied_users su
WHERE su.userid = u.userid AND su.wordid = w.wordid)
ORDER BY RANDOM()
LIMIT 1);
