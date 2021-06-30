# Store

#### Внутриигровой магазин

Во внутре игровом магазине все объекты продаются "лотами". Один лот может содержать по несколько (или ни одного) объектов персонаже, оружия, каждого вида аддона. Лоты подраздиляются на два вида:  `premium` - доступные за "донат" валюту, и обычные - доступные за внутриигровую валюту. Для разделения этих видов у каждого лота есть булевый параметор `premium` (`True` - для премиальных лотов, `False` для обычных). Параметор `price` указывает цену лота в неотрицательном целочисленном значении `unsighned integer`

##### Пример

Обычный лот стоимостью 3000 игройвой валюты

```json
"premium": false,
"price": 3000,
```

Премиум лот стоимостью 150 донат валюты

```json
"premium": true,
"price": 150,
```



#### Запросы для Store

##### Список лотов

http://cyberapi.l-b.uz/store/lots/

Метод: **GET**

Параметры:

*premium* - Отфильтровать по виду лота (0 - для обычных лотов, 1 - для премиальных). По умолчанию возвращает все лоты

*order* - Порядок лотов. Можно менять порядок по любому параметру (price, date_created, tech_name и т.д.)  и добавлять `-` в начале для сортировки в обратом порядке. Пример:  `-price` по убыванию цены, `-date_created` по убыванию даты

 *limit* - количество лотов в ответе за раз

*offset* - пропустить количество лотов для ответа

Ответ:

```json
{
    "count": 4,
    "next": "http://127.0.0.1:8000/store/lots/?limit=1&offset=1",
    "previous": null,
    "results": {
        "lots": [
            {
                "id": 4,
                "tech_name": "Carbon case",
                "premium": false,
                "price": 3000,
                "status": true,
                "date_created": "2020-10-20T16:04:27+05:00",
                "character": [
                    {
                        "id": 5,
                        "tech_name": "President",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-09-10T19:33:07.596969+05:00"
                    }
                ],
                "weapons": [
                    {
                        "id": 3,
                        "tech_name": "weapon_shotgun",
                        "default": false,
                        "hidden": false,
                        "date_created": "2020-04-24T00:47:34.360137+05:00",
                        "slot": 0,
                        "start": false
                    }
                ],
                "stock": [
                    {
                        "id": 3,
                        "tech_name": "shotgun_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-24T00:48:27.807122+05:00"
                    }
                ],
                "barrel": [
                    {
                        "id": 3,
                        "tech_name": "shotgun_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-24T00:48:47.726336+05:00"
                    }
                ],
                "muzzle": [
                    {
                        "id": 4,
                        "tech_name": "shotgun_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-24T00:48:58.218194+05:00"
                    }
                ],
                "mag": [
                    {
                        "id": 6,
                        "tech_name": "shotgun_large",
                        "default": false,
                        "hidden": false,
                        "date_created": "2020-04-24T00:49:28.945160+05:00"
                    }
                ],
                "scope": [
                    {
                        "id": 3,
                        "tech_name": "smg_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-19T01:41:00.780402+05:00"
                    }
                ],
                "grip": [
                    {
                        "id": 3,
                        "tech_name": "smg_vert",
                        "default": false,
                        "hidden": false,
                        "date_created": "2020-04-19T01:40:18.001510+05:00"
                    }
                ]
            }
        ]
    }
}
```

#### Список приобретённых лотов пользователя

http://cyberapi.l-b.uz/store/userlots/

Пользователь определяется по его токену авторизации

Метод: **GET**

Параметры:

*premium* - Отфильтровать по виду лота (0 - для обычных лотов, 1 - для премиальных). По умолчанию возвращает все лоты

*order* - Порядок лотов. Можно менять порядок по любому параметру (price, date_created, tech_name и т.д.)  и добавлять `-` в начале для сортировки в обратом порядке. Пример:  `-price` по убыванию цены, `-date_created` по убыванию даты

 *limit* - количество лотов в ответе за раз

*offset* - пропустить количество лотов для ответа

```json
{
    "count": 2,
    "next": "http://127.0.0.1:8000/store/userlots/?limit=1&offset=1",
    "previous": null,
    "results": {
        "lots": [
            {
                "id": 2,
                "tech_name": "Private collection",
                "premium": false,
                "price": 200,
                "status": true,
                "date_created": "2020-10-20T16:03:18+05:00",
                "character": [
                    {
                        "id": 3,
                        "tech_name": "CyborgRoman",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-19T01:41:36.848390+05:00"
                    }
                ],
                "weapons": [
                    {
                        "id": 3,
                        "tech_name": "weapon_shotgun",
                        "default": false,
                        "hidden": false,
                        "date_created": "2020-04-24T00:47:34.360137+05:00",
                        "slot": 0,
                        "start": false
                    },
                    {
                        "id": 2,
                        "tech_name": "weapon_smg",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-18T23:59:05.033252+05:00",
                        "slot": 0,
                        "start": true
                    }
                ],
                "stock": [
                    {
                        "id": 2,
                        "tech_name": "smg_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-19T01:42:30.121568+05:00"
                    }
                ],
                "barrel": [
                    {
                        "id": 2,
                        "tech_name": "smg_barrel",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-19T01:39:33.643984+05:00"
                    }
                ],
                "muzzle": [
                    {
                        "id": 4,
                        "tech_name": "shotgun_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-24T00:48:58.218194+05:00"
                    },
                    {
                        "id": 3,
                        "tech_name": "silencer",
                        "default": false,
                        "hidden": false,
                        "date_created": "2020-04-19T01:40:46.412250+05:00"
                    },
                    {
                        "id": 2,
                        "tech_name": "smg_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-19T01:36:33.249382+05:00"
                    }
                ],
                "mag": [
                    {
                        "id": 5,
                        "tech_name": "shotgun_normal",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-24T00:49:20.051209+05:00"
                    },
                    {
                        "id": 4,
                        "tech_name": "smg_quick",
                        "default": false,
                        "hidden": false,
                        "date_created": "2020-04-19T01:37:19.220474+05:00"
                    },
                    {
                        "id": 3,
                        "tech_name": "smg_large",
                        "default": false,
                        "hidden": false,
                        "date_created": "2020-04-19T01:37:08.648387+05:00"
                    },
                    {
                        "id": 2,
                        "tech_name": "smg_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-19T01:37:01.059546+05:00"
                    }
                ],
                "scope": [
                    {
                        "id": 4,
                        "tech_name": "shotgun_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-24T00:49:44.953043+05:00"
                    },
                    {
                        "id": 3,
                        "tech_name": "smg_base",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-19T01:41:00.780402+05:00"
                    }
                ],
                "grip": [
                    {
                        "id": 3,
                        "tech_name": "smg_vert",
                        "default": false,
                        "hidden": false,
                        "date_created": "2020-04-19T01:40:18.001510+05:00"
                    },
                    {
                        "id": 2,
                        "tech_name": "smg_grip",
                        "default": true,
                        "hidden": false,
                        "date_created": "2020-04-19T01:40:03.837560+05:00"
                    }
                ]
            }
        ]
    }
}
```

##### Поиск лота

http://cyberapi.l-b.uz/store/userlots/

Пользователь определяется по его токену авторизации

Метод: **GET**

Параметры:

*premium* - Отфильтровать по виду лота (0 - для обычных лотов, 1 - для премиальных). По умолчанию возвращает все лоты

*order* - Порядок лотов. Можно менять порядок по любому параметру (price, date_created, tech_name и т.д.)  и добавлять `-` в начале для сортировки в обратом порядке. Пример:  `-price` по убыванию цены, `-date_created` по убыванию даты

 *limit* - количество лотов в ответе за раз

*offset* - пропустить количество лотов для ответа

*query* - ключевое слово. Если не задана никакая фильтрация, то ищет в `tech_name` лота. Для поиска по персанажам, оружию или какому то аддону использовать параметры для фильтрации (все что ниже)

*character* - поиск по персонажам, чтобы включить нужно задать 1

*weapon* - поиск по оружию, чтобы включить нужно задать 1

*stock, barrel, muzzle, mag, grip, scope* - поиск по аддонам, чтобы включить нужно задать 1

Пример поиска лота в котором есть `stock` под названием `smg_base`:

http://cyberapi.l-b.uz/store/search?query=smg_base&stock=1

Ответ

```json
{
    "lots": [
        {
            "id": 2,
            "tech_name": "Private collection",
            "premium": false,
            "price": 200,
            "status": true,
            "date_created": "2020-10-20T16:03:18+05:00",
            "character": [
                {
                    "id": 3,
                    "tech_name": "CyborgRoman",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-19T01:41:36.848390+05:00"
                }
            ],
            "weapons": [
                {
                    "id": 3,
                    "tech_name": "weapon_shotgun",
                    "default": false,
                    "hidden": false,
                    "date_created": "2020-04-24T00:47:34.360137+05:00",
                    "slot": 0,
                    "start": false
                },
                {
                    "id": 2,
                    "tech_name": "weapon_smg",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-18T23:59:05.033252+05:00",
                    "slot": 0,
                    "start": true
                }
            ],
            "stock": [
                {
                    "id": 2,
                    "tech_name": "smg_base",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-19T01:42:30.121568+05:00"
                }
            ],
            "barrel": [
                {
                    "id": 2,
                    "tech_name": "smg_barrel",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-19T01:39:33.643984+05:00"
                }
            ],
            "muzzle": [
                {
                    "id": 4,
                    "tech_name": "shotgun_base",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-24T00:48:58.218194+05:00"
                },
                {
                    "id": 3,
                    "tech_name": "silencer",
                    "default": false,
                    "hidden": false,
                    "date_created": "2020-04-19T01:40:46.412250+05:00"
                },
                {
                    "id": 2,
                    "tech_name": "smg_base",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-19T01:36:33.249382+05:00"
                }
            ],
            "mag": [
                {
                    "id": 5,
                    "tech_name": "shotgun_normal",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-24T00:49:20.051209+05:00"
                },
                {
                    "id": 4,
                    "tech_name": "smg_quick",
                    "default": false,
                    "hidden": false,
                    "date_created": "2020-04-19T01:37:19.220474+05:00"
                },
                {
                    "id": 3,
                    "tech_name": "smg_large",
                    "default": false,
                    "hidden": false,
                    "date_created": "2020-04-19T01:37:08.648387+05:00"
                },
                {
                    "id": 2,
                    "tech_name": "smg_base",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-19T01:37:01.059546+05:00"
                }
            ],
            "scope": [
                {
                    "id": 4,
                    "tech_name": "shotgun_base",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-24T00:49:44.953043+05:00"
                },
                {
                    "id": 3,
                    "tech_name": "smg_base",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-19T01:41:00.780402+05:00"
                }
            ],
            "grip": [
                {
                    "id": 3,
                    "tech_name": "smg_vert",
                    "default": false,
                    "hidden": false,
                    "date_created": "2020-04-19T01:40:18.001510+05:00"
                },
                {
                    "id": 2,
                    "tech_name": "smg_grip",
                    "default": true,
                    "hidden": false,
                    "date_created": "2020-04-19T01:40:03.837560+05:00"
                }
            ]
        }
    ]
}
```

##### Покупка лота

http://cyberapi.l-b.uz/store/purchase/{lot id}/

Пользователь (покупатель) определяется по токену авторизации

Лот определяется по *lot id* отправленному в url

Метод: **POST**

Возможные ответы сервера:

```json
{
    "detail": "Lot has been successfully purchased"  // Успешно добавлен пользователю, деньги снят
}
```

```json
{
    "detail": "User already purchased this lot" // Уже был приобритён
}
```

```json
{
    "detail": "Insufficient funds" // Недостаточно средств для покупки
}
```

```json
{
    "detail": "Lot is unavailable to purchase" // Статус лота False, не доступен для покупки
}
```

Ответы можно не обрабатывать, на успешный ответ придёт HTTP 200 OK,  на все не успешные 400 BAD REQUEST