INSERT INTO ranks (rank, base_xp) VALUES
    (1, 10),
    (2, 15),
    (3,25),
    (4,40),
    (5,60),
    (6,100),
    (7,150),
    (8,250),
    (9,400),
    (10,700);

INSERT INTO genres (name) VALUES
    ('青物'),
    ('フラットフィッシュ'),
    ('根魚'),
    ('イカ'),
    ('太刀魚'),
    ('シーバス'),
    ('小物');

INSERT INTO species (name, genre_id, rank, water_type, measure_type, standard_size, good_size, lunker_size, record_size) VALUES
    ('サバ', (SELECT id FROM genres WHERE name = '小物'),2,'salt','length',30,35,40,45),
    ('アジ', (SELECT id FROM genres WHERE name = '小物'),2,'salt','length',20,25,30,40),
    ('カサゴ', (SELECT id FROM genres WHERE name = '根魚'),3,'salt','length',15,20,25,30),
    ('ブリ', (SELECT id FROM genres WHERE name = '青物'),5,'salt','length',50,60,80,100),
    ('太刀魚', (SELECT id FROM genres WHERE name = '太刀魚'),5,'salt','finger',3,3.5,4,5),
    ('シーバス', (SELECT id FROM genres WHERE name = 'シーバス'),5,'salt','length',50,60,80,90),
    ('マゴチ', (SELECT id FROM genres WHERE name = 'フラットフィッシュ'),6,'salt','length',40,50,60,70),
    ('アオリイカ', (SELECT id FROM genres WHERE name = 'イカ'),6,'salt','weight',0.8,1,2,3),
    ('ヒラメ', (SELECT id FROM genres WHERE name = 'フラットフィッシュ'),7,'salt','length',40,50,70,80),
    ('ヒラマサ', (SELECT id FROM genres WHERE name = '青物'),9,'salt','length',60,70,90,110);

INSERT INTO methods (name, default_multiplier, fishing_area) VALUES
    ('サビキ',0.6,'both'),
    ('ちょい投げ',0.8,'shore'),
    ('穴釣り',0.8,'shore'),
    ('ウキ釣り',0.9,'shore'),
    ('泳がせ',1.0,'both'),
    ('投げ釣り',1.1,'shore'),
    ('テンヤ',1.2,'both'),
    ('ショアジギング',1.3,'shore'),
    ('ウキフカセ',1.4,'shore'),
    ('エギング',1.5,'both'),
    ('ルアー',1.6,'both');