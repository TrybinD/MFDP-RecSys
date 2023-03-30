# MFDP-RecSys. Проект LifeStyle
Это репозиторий для проекта по курсу MFDP, трек RecSys 

Участник: Трубин Даниил Олегович

MVP: https://trybind-mfdp-recsys-main-z5amqv.streamlit.app/

1. [Данные и концепция](#data_and_concepts)
2. [Техническая реализация MVP](#tech_realisation)
3. [Краткий отчет по моделям](#models)

## <a name="data_and_concepts">1. Данные и концепция</a> 
### Концепция
Идея - разработка сайта (пока сайт (так быстрее), в светлом будущем и мобильное приложение, потому что это кажется более подходящей реализацией:)), который будет рекомендовать книги, фильмы, сериалы, а еще может быть еще статьи, например, на Хабре, подкасты, курсы и многое многое другое в зависимости от того, сколько свободного времени есть у пользователя. Можно построить рекомендательную систему для нового контента и для контента, добавленного в "Избранное".

С одной стороны это будет похоже на "Смотреть позже" на Ютубе, только для любого контента - книги, фильмы, сериалы, статьи, подкасты и тд и тп.
С другой стороны, это будет рекомендательная система для нового контента, на основе "Избранного".

*Какую "боль" закрывает*: У меня весь интересующий меня контент (книги, статьи, фильмы) разбросан по перепискам с самим собой, вкладкам в браузерах на телефоне и ПК и так далее. И, когда появляются 20-30 свободных минут, я могу их потратить на поиск и выбор того, что мне интересно прямо сейчас.
А иногда хочется чего-то нового, но похожего на то, что тебе нравится.

*Сценарий использования MVP*:
1) Пользователь заходит на сайт
2) Пользователь авторизуется (или регистрируется)
3) Пользователь попадает на начальную страницу рекомендаций нового контента, есть возможность добавить один из вариантов предложенного контента в избранное. Кроме этого есть фильтры, где он может указать время, которое у него есть и что-то еще (Например, предпочтения, или еще что-то). В светлом будущем можно будет попытаться предсказывать, сколько времени есть у пользователя на основе его предыдущих интеракций. Но это кажется большой новой фичей, которая должна встраиваться в уже работающий продукт (имеющий постоянных пользователей)
4) Можно переключиться на вкладку избранное и выбрать себе контент из избранного, так же по фильтрам
5) Можно переключиться на страницу с поиском и найти контент по ключевым словам. (Опционально, если получится, то можно добавлять кастомный контент, например ссылки на статью или pdf файлы с книгами и тд)

В идеале оба вида рекомендаций должны быть основаны на времен и настроении пользователя, предсказывать, хочет пользователь сейчас, например, образовательного контента или расслабляющего.

### Данные 
Так как идея в том, чтобы рекомендовать в зависимости от количества свободного времени, то нужно иметь, как возможность рекомендовать что-то длинное - фильм, что-то относительно короткое - сериалы, или что-то не сильно привязаное ко времени - книги (статьи)

Данные: 
Книги - Book-Crossing Dataset (http://www2.informatik.uni-freiburg.de/~cziegler/BX/) (Будут переведены на русский)

Фильмы и сериалы Kion - RecSys Course Competition (https://ods.ai/competitions/competition-recsys-21/data)

Статьи: Хабр

## 2. <a name="tech_realisation">Техническая реализация MVP (PoC)</a> 

На этапе MVP должен получиться **сайт**, с авторизацией, которая позволяет делать персонофицированные рекомендации и сохранять избранное.
Сценарий пользования сайтам указан выше.
MVP можно собрать на базе Streamlit, они даже предоставляют возможность деплоя сайта на их сервис, при условии, что сайт не будет потреблять много памяти.
Ссылка на шаблон сайта с минимальным функционалом указан выше.

Вообще, в условиях нехватки данных для нового сервиса с новыми клиентами, есть желание построить модель, где, возможно, используются контекстуальные многорукие бандиты + классический RecSys. Из бонусов, данная иситема сможет подстраиваться на каждого уникального пользователя. Но пока будем использовать для начала открытые датасеты о книгах, фильмах и сериалах (потом можно собрать датасет по статьям на Хабре и подкастам на основе интеракций на сайте). А потом можно разработать алгоритмы онлайн-дообучения собрать маленькую тестовую группу, на которой проверить насколько хорошо работают эти алгоритмы обучения или настроить имитационную модель и проверять обучение на ней. 

Дальше можно собирать информацию о паттернах поведения пользователя, распозновать эмоции и все это учитывать при рекомендации.
Добавить функции планирования и составления расписания. Но это уже для других пилотов и релизов)

### Метрики
В качестве основной метрики того, что сайт работает хорошо можно использовать MAP@k. Эта обратная величина к этой метрике * 20 логичным образом может трактоваться, как средняя позиция валидной рекомендации пользователю. И чем больше метрика, тем меньше обратная величина, что говорит, что валидная рекомендация ближе к началу списка.

## 3. <a name="models">Краткий отчет по моделям</a> 


