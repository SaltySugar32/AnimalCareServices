from utils import get_db_connection

con = get_db_connection()
def create_tables():
  con.executescript('''
  CREATE TABLE IF NOT EXISTS service (
    service_id INT IDENTITY(1,1) PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    duration INT
  );

  CREATE TABLE IF NOT EXISTS client (
    client_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(255) NOT NULL
  );

  CREATE TABLE IF NOT EXISTS master (
    master_id INT IDENTITY(1,1) PRIMARY KEY,
    master_name VARCHAR(255) NOT NULL,
    master_rating DECIMAL(3, 2)
  );

  CREATE TABLE IF NOT EXISTS master_service (
    master_service_id INT IDENTITY(1,1) PRIMARY KEY,
    service_id INT,
    master_id INT,
    work_day_start TIME,
    work_day_end TIME,
    FOREIGN KEY (service_id) REFERENCES service(service_id),
    FOREIGN KEY (master_id) REFERENCES master(master_id)
  );

  CREATE TABLE IF NOT EXISTS service_order (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    client_id INT,
    master_service_id INT,
    order_date DATE,
    FOREIGN KEY (client_id) REFERENCES client(client_id),
    FOREIGN KEY (master_service_id) REFERENCES master_service(master_service_id)
  );

  CREATE TABLE IF NOT EXISTS review (
    review_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT,
    review_title VARCHAR(255),
    review_description TEXT,
    review_score INT,
    FOREIGN KEY (order_id) REFERENCES service_order(order_id)
  );

  ''')

def drop_tables():
  con.executescript('''
  DROP table IF EXISTS service;
  DROP table IF EXISTS client;
  DROP table IF EXISTS master;
  DROP table IF EXISTS master_service;
  DROP table IF EXISTS service_order;
  DROP table IF EXISTS review;
  ''')

def gen_service():
  con.executescript('''
  INSERT INTO service(service_name, description, price, duration)
  VALUES 
    ('Прогулка', 'Прогулка домашнего животного в парке', 20, '01:00:00'),
    ('Кормление', 'Кормление домашнего животного', 10, '00:15:00'),
    ('Уход за шерстью', 'Расчесывание шерсти домашнего животного', 30, '01:00:00'),
    ('Удаление шерсти', 'Удаление шерсти из шерстяного покрытия домашнего животного', 50, '01:30:00'),
    ('Удаление блох и клещей', 'Удаление блох и клещей с тела домашнего животного', 15, '00:20:00');
  ''')

def gen_master():
  con.executescript('''
  INSERT INTO master(master_name)
  VALUES
  ('Иван Иванов'),
  ('Елена Петрова'),
  ('Алексей Сидоров'),
  ('Наталья Кузнецова'),
  ('Дмитрий Морозов');
  ''')

def gen_client():
  con.executescript('''
  INSERT INTO client(username)
  VALUES 
    ('user1'),
    ('admin'),
    ('anonym');
  ''')

def gen_master_service():
  con.executescript('''
  INSERT INTO master_service(service_id, master_id, work_day_start, work_day_end)
  VALUES
    (1, 1, '10:00:00', '16:00:00'),
    (2, 2, '09:00:00', '17:00:00'),
    (3, 3, '11:00:00', '19:00:00'),
    (4, 4, '10:00:00', '16:00:00'),
    (5, 5, '08:00:00', '14:00:00'),
    (1, 2, '13:00:00', '19:00:00'),
    (2, 3, '09:00:00', '16:00:00'),
    (3, 4, '10:00:00', '17:00:00'),
    (4, 5, '11:00:00', '18:00:00'),
    (5, 1, '08:00:00', '14:00:00');
  ''')

def gen_service_order():
  con.executescript('''
  INSERT INTO service_order(client_id, master_service_id, order_date)
  VALUES
    (1, 1, '2023-06-10 10:00:00'),
    (2, 5, '2023-06-11 13:30:00'),
    (3, 4, '2023-06-12 15:45:00'),
    (4, 3, '2023-06-13 09:15:00'),
    (5, 2, '2023-06-14 12:00:00'),
    (1, 3, '2023-06-15 14:30:00'),
    (2, 4, '2023-06-16 16:00:00'),
    (3, 5, '2023-06-17 11:45:00'),
    (4, 1, '2023-06-18 10:30:00'),
    (5, 2, '2023-06-19 13:15:00');
  ''')

def gen_review():
  con.executescript('''
  INSERT INTO review(order_id, review_title, review_description, review_score)
  VALUES
    (1, 'Отличный выгул', 'Мой пес получил отличный выгул. Спасибо!', 5),
    (2, 'Прекрасное обслуживание', 'Я очень довольна обслуживанием, мой кот был рад.', 4),
    (3, 'Отличная работа', 'Моя собака выглядит прекрасно после удаления шерсти. Спасибо!', 5),
    (4, 'Хорошее обслуживание', 'Мой кот был хорошо покормлен и ухожен.', 4),
    (5, 'Отличный мастер', 'Мастер был очень внимательным и заботился о моей собаке.', 5),
    (6, 'Хорошее обслуживание', 'Мой кот был хорошо покормлен и ухожен, но работа заняла больше времени, чем я ожидал.', 3),
    (7, 'Отличный выгул', 'Мой пес был очень доволен выгулом.', 5),
    (8, 'Прекрасная работа', 'Мой кот был очень доволен удалением шерсти. Спасибо!', 4),
    (9, 'Хорошее обслуживание', 'Мой пес был хорошо покормлен и ухожен.', 4),
    (10, 'Отличный мастер', 'Мастер был очень профессиональным и заботился о моей собаке.', 5);
  ''')
  

def populate():
  drop_tables()
  create_tables()
  gen_service()
  gen_client()
  gen_master()
  gen_master_service()
  gen_service_order()
  gen_review()

