from utils import get_db_connection
import random
import datetime

def create_tables(con=get_db_connection()):
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
    master_name VARCHAR(255) NOT NULL
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

def drop_tables(con=get_db_connection()):
  con.executescript('''
  DROP table IF EXISTS service;
  DROP table IF EXISTS client;
  DROP table IF EXISTS master;
  DROP table IF EXISTS master_service;
  DROP table IF EXISTS service_order;
  DROP table IF EXISTS review;
  ''')

def gen_service(con=get_db_connection()):
  con.executescript('''
  INSERT INTO service(service_name, description, price, duration)
  VALUES 
    ('Прогулка', 'Прогулка домашнего животного в парке', 20, '01:00:00'),
    ('Кормление', 'Кормление домашнего животного', 10, '00:15:00'),
    ('Уход за шерстью', 'Расчесывание шерсти домашнего животного', 30, '01:00:00'),
    ('Удаление шерсти', 'Удаление шерсти из шерстяного покрытия домашнего животного', 50, '01:30:00'),
    ('Удаление блох и клещей', 'Удаление блох и клещей с тела домашнего животного', 15, '00:20:00');
  ''')

def gen_master(con=get_db_connection(), master_num=10):
  
  m_first = ['Иван', 'Дмитрий', 'Егор', 'Даниил', 'Евгений', 'Василий', 'Артем']
  f_first = ['Елена','Наталья', 'Надежда', 'Татьяна', 'Анастасия', 'София', 'Маргарита']
  second = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Морозов', 'Смирнов', 'Попов', 'Соколов']
  values = ''
  
  for i in range(master_num):
    if(random.choice([0,1])):
      f = random.choice(m_first)
      s = random.choice(second)
      values += "('" + str(f) + " " + str(s)+ "'), "
    else:
      f = random.choice(f_first)
      s = random.choice(second)
      values += "('" + str(f) + " " + str(s)+ "а'), "
  values = values[:len(values)-2] + ';'

  con.executescript(f'''
  INSERT INTO master(master_name)
  VALUES {values}
  ''')

def gen_client(con=get_db_connection(), client_num=20):
  first = ['a', 'b', 'c', 'd', 'e', 'f', 'j', 'k', 'l']
  second = ['wayne', 'cool', 'ron', 'loo', 'maxwell', 'white', 'change', 'hawk']
  values = ""
  for i in range(client_num):
    f = random.choice(first)
    s = random.choice(second)
    t = random.randint(0,999)
    values += "('" + str(f) + "_" + str(s) + str(t) + "'), "
  values = values[:len(values)-2] + ';'

  con.executescript(f'''
  INSERT INTO client(username)
  VALUES {values}
  ''')

def gen_master_service(con=get_db_connection(), service_num=5, master_num=10):
  time_start = ['08:00:00', '09:00:00', '10:00:00', '11:00:00']
  time_end = ['16:00:00', '17:00:00', '18:00:00', '19:00:00']
  values = ''
  for i in range(master_num):
    for j in range(service_num):
      if(random.choice([0,1])):
        t_start = random.choice(time_start)
        t_end = random.choice(time_end)
        values += "(" + str(j+1) + ", " + str(i+1) + ", '" + str(t_start) + "', '" + str(t_end) + "'), "
  
  values = values[:len(values)-2] + ';'
  #return values
  con.executescript(f'''
  INSERT INTO master_service(service_id, master_id, work_day_start, work_day_end)
  VALUES {values}
  ''')

def gen_service_order(con=get_db_connection(), client_num = 20, service_order_num=50):
  cursor = con.cursor()
  cursor.execute('SELECT * FROM master_service')
  master_service_num = len(cursor.fetchall())
  values = ''
  
  for i in range(service_order_num):
    client = random.randint(1, client_num)
    master_service = random.randint(1, master_service_num)
    date = datetime.datetime(2023, 6, random.randint(10,30), random.randint(11, 15), random.choice([0,15,30,45]))
    values += '(' + str(client) + ', ' + str(master_service) + ", '" + str(date) + "'), "
  
  values = values[:len(values)-2] + ';'
  con.executescript(f'''
  INSERT INTO service_order(client_id, master_service_id, order_date)
  VALUES {values}
  ''')

def gen_review(con=get_db_connection(), review_num=20):
  cursor = con.cursor()
  cursor.execute('SELECT * FROM service_order')
  order_num = len(cursor.fetchall())
  values = ''

  for i in range(review_num):
    order = random.randint(1, order_num)
    score = random.choice([1,2,3,4,5])
    title = '' 
    desc = ''
    match score:
      case 1:
        title = random.choice(['Ужасно', 'Отвратительно', 'Ужасные мастера'])
        desc = random.choice(['Ужасный сервис', 'Ужасная работа', 'Не рекомендую', 'Держитесь дальше от этого'])
      case 2:
        title = random.choice(['Плохо', 'Очень плохо', 'Ужасная работа', "Ужасно"])
        desc = random.choice(['Плохие мастера', 'Плохо выполнена работа', 'Буду искать альтернативы', 'Не рекомендую'])
      case 3:
        title = random.choice(['Можно и лучше', 'Приемлемо', "Посредственная работа"])
        desc = random.choice(['Сервис оставляет желать лучшего', 'Ни о чем', 'Не совсем то, чего ожидал', 'Заказывать, только если нет других альтернатив'])
      case 4:
        title = random.choice(['Хорошо', 'Понравилось', 'Неплохо'])
        desc = random.choice(['Хорошая работа', 'Спасибо за сервис', 'Неплохо за свою цену'])
      case 5:
        title = random.choice(['Рекомендую', 'Прекрасно', 'Идеально'])
        desc = random.choice(['Великолепный сервис', 'Буду рекомендовать знакомым', 'Хорошая цена и сервис'])
    values += "(" + str(order) + ", '" + str(title) + "', '" + str(desc) + "', " + str(score) + "), "
  
  values = values[:len(values)-2] + ';'
  con.executescript(f'''
  INSERT INTO review(order_id, review_title, review_description, review_score)
  VALUES {values}
  ''')
  

def populate(client_num=20, service_num = 5, master_num=10, service_order_num=50, review_num=20):
  con=get_db_connection()
  drop_tables(con)
  create_tables(con)
  gen_service(con)
  gen_client(con, client_num)
  gen_master(con, master_num)
  gen_master_service(con, service_num, master_num)
  gen_service_order(con, client_num, service_order_num)
  gen_review(con, review_num)

