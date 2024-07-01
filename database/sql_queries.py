CREATE_USER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS telegram_users
(
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER,
USERNAME CHAR(50),
FIRST_NAME CHAR(50),
LAST_NAME CHAR(50),
UNIQUE (TELEGRAM_ID)
)
"""

add_column_table_telegram_users = """
alter table telegram_users add column REFERENCE_LINK text
"""

create_table_reference_users = """
create table if not exists reference_users
(
id integer primary key,
owner_telegram_id integer,
reference_telegram_id integer,
unique (owner_telegram_id, reference_telegram_id)
)
"""

CREATE_PROFILE_TABLE = """
create table if not exists profile_users
(
id integer primary key,
telegram_id integer,
nickname char(50),
biography text,
age integer,
height integer,
weight integer,
gender char(50),
photo text,
unique (telegram_id)
)
"""

CREATE_BAN_USER_TABLE = """
create table if not exists ban_users
(
id integer primary key,
telegram_id integer,
ban_count integer,
unique (telegram_id)
)
"""

CREATE_LIKE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS like_profile
(
ID INTEGER PRIMARY KEY,
OWNER_TELEGRAM_ID INTEGER,
LIKER_TELEGRAM_ID INTEGER,
UNIQUE (OWNER_TELEGRAM_ID, LIKER_TELEGRAM_ID)
)
"""

CREATE_DISLIKE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS dislike_profile
(
ID INTEGER PRIMARY KEY,
OWNER_TELEGRAM_ID INTEGER,
DISLIKER_TELEGRAM_ID INTEGER,
UNIQUE (OWNER_TELEGRAM_ID, DISLIKER_TELEGRAM_ID)
)
"""

INSERT_USER_QUERY = """
INSERT OR IGNORE INTO telegram_users VALUES (?,?,?,?,?,?)
"""

FILTER_LEFT_JOIN_PROFILE_LIKE_QUERY = """
SELECT * FROM profile_users
LEFT JOIN like_profile ON profile_users.TELEGRAM_ID = like_profile.OWNER_TELEGRAM_ID
AND like_profile.LIKER_TELEGRAM_ID = ?
LEFT JOIN dislike_profile ON profile_users.TELEGRAM_ID = dislike_profile.OWNER_TELEGRAM_ID
AND dislike_profile.DISLIKER_TELEGRAM_ID = ?
WHERE like_profile.ID IS NULL
AND dislike_profile.ID IS NULL
AND profile_users.TELEGRAM_ID != ?

"""

INSERT_LIKE_QUERY = """
INSERT INTO like_profile VALUES (?,?,?)
"""

INSERT_DISLIKE_QUERY = """
INSERT INTO dislike_profile VALUES (?,?,?)
"""

INSERT_PROFILE_USERS = """
insert or ignore into profile_users values (?,?,?,?,?,?,?,?,?)
"""

INSERT_BAN_USER = """
insert into ban_users values (?,?,?)
"""

SELECT_BAN_USER = """
select * from ban_users where telegram_id = ?
"""

SELECT_PROFILE_USER = """
select * from profile_users where telegram_id = ?
"""

UPDATE_BAN_USER = """
update ban_users set ban_count = ban_count + 1 where telegram_id = ?
"""

DELETE_BAN_USER = """
delete from ban_users where telegram_id = ?
"""

select_reference_user = """
            SELECT REFERENCE_LINK
            FROM telegram_users
            WHERE telegram_id = ?
            """

select_referral_list = """
            SELECT reference_telegram_id
            FROM reference_users
            WHERE owner_telegram_id = ?
            """

select_join_telegram_users_telegram_id = f"""
            SELECT TELEGRAM_ID, FIRST_NAME
            FROM telegram_users
            WHERE TELEGRAM_ID IN 
            """

INSERT_REFERRAL_QUERY = """
            INSERT INTO reference_users VALUES (?,?,?)
            """

SELECT_USER_BY_LINK_QUERY = """
            SELECT * FROM telegram_users WHERE REFERENCE_LINK = ?
            """

UPDATE_USER_LINK_QUERY = """
            UPDATE telegram_users SET REFERENCE_LINK = ? WHERE TELEGRAM_ID = ?
            """

SELECT_USER_QUERY = """
            SELECT * FROM telegram_users WHERE TELEGRAM_ID = ?
            """

CREATE_TABLE_MUSIC = """
            create table if not exists music (
                id integer primary key,
                name_music text,
                user_name char(50),
                telegram_id integer,
                unique(id, telegram_id)
            )
"""

INSERT_USER_MUSIC = """
            insert into music values (?,?,?,?)
"""

CREATE_TABLE_AUDIO_REQUESTS = """
            CREATE TABLE IF NOT EXISTS audio_requests (
                user_id INTEGER PRIMARY KEY,
                requested INTEGER DEFAULT 0
            )
"""