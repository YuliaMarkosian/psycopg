import psycopg2

with psycopg2.connect(database="client", user="postgres", password="10Ralefa") as conn:
    with conn.cursor() as cur:
        # cur.execute("""
        # DROP TABLE phonenumbers;
        # DROP TABLE clients
        # """)

        def create_db(cur):
            cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                name VARCHAR(20),
                lastname VARCHAR(30),
                email VARCHAR(254)
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phonenumbers(
                number VARCHAR(11) PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id)
            );
            """)
            conn.commit()
        pass

        def add_client(cur, name=None, surname=None, email=None, tel=None):
            cur.execute("""
            INSERT INTO clients(name, lastname, email)
            VALUES (%s, %s, %s)
            """, (name, surname, email))

            conn.commit()
        pass

        def add_phone (cur, client_id, tel):
            cur.execute("""
            INSERT INTO phonenumbers(number, client_id)
            VALUES (%s, %s)
            """, (tel, client_id))
        pass

        def change_client(cur, id, name=None, surname=None, email=None):
            cur.execute("""
            SELECT * from clients
            WHERE id = %s
            """, (id, ))
            info = cur.fetchone()
            if name is None:
                name = info[1]
            if surname is None:
                surname = info[2]
            if email is None:
                email = info[3]
            cur.execute("""
                UPDATE clients
                SET name = %s, lastname = %s, email =%s 
                where id = %s
                """, (name, surname, email, id))
        pass

        def delete_phone(cur, number):
            cur.execute("""
                DELETE FROM phonenumbers 
                WHERE number = %s
                """, (number, ))
        pass

        def delete_client(cur, id):
            cur.execute("""
            DELETE FROM phonenumbers
            WHERE client_id = %s
            """, (id, ))
            cur.execute("""
            DELETE FROM clients 
            WHERE id = %s
            """, (id,))
        pass

        def find_client(cur, name=None, surname=None, email=None, tel=None):
            if name is None:
                name = '%'
            else:
                name = '%' + name + '%'
            if surname is None:
                surname = '%'
            else:
                surname = '%' + surname + '%'
            if email is None:
                email = '%'
            else:
                email = '%' + email + '%'
            if tel is None:
                cur.execute("""
                    SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                    LEFT JOIN phonenumbers p ON c.id = p.client_id
                    WHERE c.name LIKE %s AND c.lastname LIKE %s
                    AND c.email LIKE %s
                    """, (name, surname, email))
            else:
                cur.execute("""
                    SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                    LEFT JOIN phonenumbers p ON c.id = p.client_id
                    WHERE c.name LIKE %s AND c.lastname LIKE %s
                    AND c.email LIKE %s AND p.number like %s
                    """, (name, surname, email, tel))
        pass

conn.close()