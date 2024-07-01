import sqlite3
from database import sql_queries


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()

    def sql_create_tables(self):
        if self.connection:
            print("Database connected successfully")

        self.connection.execute(sql_queries.CREATE_USER_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_BAN_USER_TABLE)
        self.connection.execute(sql_queries.CREATE_PROFILE_TABLE)
        self.connection.execute(sql_queries.CREATE_LIKE_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_DISLIKE_TABLE_QUERY)
        self.connection.execute(sql_queries.create_table_reference_users)
        self.connection.execute(sql_queries.CREATE_TABLE_MUSIC)
        self.connection.execute(sql_queries.CREATE_TABLE_AUDIO_REQUESTS)

        try:
            self.connection.execute(sql_queries.add_column_table_telegram_users)
        except sqlite3.Error:
            pass

        self.connection.commit()

    def sql_insert_user(self, tg_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, tg_id, username, first_name, last_name, None)
        )
        self.connection.commit()

    def sql_insert_ban_user(self, tg_id):
        self.cursor.execute(
            sql_queries.INSERT_BAN_USER,
            (None, tg_id, 1)
        )
        self.connection.commit()

    def sql_select_ban_user(self, tg_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "count": row[2]
        }
        return self.cursor.execute(
            sql_queries.SELECT_BAN_USER,
            (tg_id,)
        ).fetchone()

    def sql_update_ban_user_count(self, tg_id):
        self.cursor.execute(
            sql_queries.UPDATE_BAN_USER,
            (tg_id,)
        )
        self.connection.commit()

    def sql_delete_user(self, tg_id):
        self.cursor.execute(
            sql_queries.DELETE_BAN_USER,
            (tg_id,)
        )
        self.connection.commit()

    def sql_insert_profile_user(self, tg_id, nickname, bio, age, height, weight, gender, photo):
        self.cursor.execute(
            sql_queries.INSERT_PROFILE_USERS,
            (None, tg_id, nickname, bio, age, height, weight, gender, photo)
        )
        self.connection.commit()

    def sql_select_profile_user(self, tg_id):
        self.cursor.execute(
            sql_queries.SELECT_PROFILE_USER,
            (tg_id,)
        )
        user_data = self.cursor.fetchone()

        if user_data:
            return {
                "id": user_data[0],
                "telegram_id": user_data[1],
                "nickname": user_data[2],
                "biography": user_data[3],
                "age": user_data[4],
                "height": user_data[5],
                "weight": user_data[6],
                "gender": user_data[7],
                "photo": user_data[8]
            }
        else:
            return None

    def sql_select_filter_profiles(self, tg_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "biography": row[3],
            "age": row[4],
            "height": row[5],
            "weight": row[6],
            "gender": row[7],
            "photo": row[8]
        }
        return self.cursor.execute(
            sql_queries.FILTER_LEFT_JOIN_PROFILE_LIKE_QUERY,
            (tg_id, tg_id, tg_id,)
        ).fetchall()

    def sql_insert_like(self, owner, liker):
        self.cursor.execute(
            sql_queries.INSERT_LIKE_QUERY,
            (None, owner, liker,)
        )
        self.connection.commit()

    def sql_insert_dislike(self, owner, disliker):
        self.cursor.execute(
            sql_queries.INSERT_DISLIKE_QUERY,
            (None, owner, disliker,)
        )
        self.connection.commit()

    def get_referral_link(self, user_id):
        self.cursor.execute(sql_queries.select_reference_user,
                            (user_id,)
                            )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_referral_list(self, user_id):
        self.cursor.execute(
            sql_queries.select_referral_list,
            (user_id,)
        )
        referred_users = self.cursor.fetchall()
        referred_users_ids = [user[0] for user in referred_users]
        if referred_users_ids:
            query = f"{sql_queries.select_join_telegram_users_telegram_id}({','.join('?' * len(referred_users_ids))})"

            self.cursor.execute(query, referred_users_ids)
            referred_users_data = self.cursor.fetchall()
            return referred_users_data
        else:
            return []

    def sql_insert_referral(self, owner, referral):
        self.cursor.execute(
            sql_queries.INSERT_REFERRAL_QUERY,
            (None, owner, referral,)
        )
        self.connection.commit()

    def sql_select_user_by_link(self, link):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "link": row[5],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_BY_LINK_QUERY,
            (link,)
        ).fetchone()

    def sql_update_user_link(self, link, tg_id):
        self.cursor.execute(
            sql_queries.UPDATE_USER_LINK_QUERY,
            (link, tg_id,)
        )
        self.connection.commit()

    def sql_select_user(self, tg_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "link": row[5],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_QUERY,
            (tg_id,)
        ).fetchone()

    def insert_table_music(self, music_name, user_name, tg_id):
        self.cursor.execute(
            sql_queries.INSERT_USER_MUSIC,
            (None, music_name, user_name, tg_id))
        self.connection.commit()

    def save_audio_request(self, user_id):
        self.cursor.execute('''
            INSERT INTO audio_requests (user_id, requested)
            VALUES (?, 1)
            ON CONFLICT(user_id) DO UPDATE SET requested = 1
        ''', (user_id,))
        self.connection.commit()

    def has_audio_request(self, user_id):
        self.cursor.execute('''
            SELECT requested FROM audio_requests WHERE user_id = ?
        ''', (user_id,))
        result = self.cursor.fetchone()
        return result and result[0] == 1

    def remove_audio_request(self, user_id):
        self.cursor.execute('''
            UPDATE audio_requests SET requested = 0 WHERE user_id = ?
        ''', (user_id,))
        self.connection.commit()