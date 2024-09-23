+------------------+
|      User        |
+------------------+
| - username       |
| - email          |
| - role           |
| - first_name     |
| - last_name      |
| - phone_number   |
| - date_of_birth  |
| - profile_picture |
| - bio            |
| - website        |
| - alternate_email |
| - linkedin       |
| - is_active      |
| + is_admin()     |
| + is_producer()  |
| + is_collector() |
| + is_consumer()  |
+------------------+
        ^
        |
        | 1
        | M
+------------------+
|      Group       |
+------------------+
| - name           |
| - photo          |
| + __str__()     |
+------------------+
        ^
        |
        | M
        | M
+------------------+
|     Message      |
+------------------+
| - content        |
| - timestamp      |
| + __str__()     |
+------------------+

+------------------+
|     Product      |
+------------------+
| - name           |
| - description    |
| - price          |
| - stock          |
| + __str__()     |
+------------------+
        ^
        |
        | 1
        | M
+------------------+
|     Order        |
+------------------+
| - order_number    |
| - order_date      |
| - status          |
| + __str__()      |
+------------------+
        |
        | M
        | 1
+------------------+
|     Need         |
+------------------+
| - description    |
| - quantity       |
| - status         |
| + __str__()     |
+------------------+

+------------------+
|      Notice      |
+------------------+
| - title          |
| - content        |
| - created_at     |
| + __str__()     |
+------------------+
