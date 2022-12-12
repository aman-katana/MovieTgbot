from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()

    # Метод, который передает запрос в БД
    def query(self, query, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


conn = Neo4jConnection(uri="bolt://localhost:7687", user="Aman", password="12345678")
# conn.query("CREATE OR REPLACE DATABASE neo4j")

# query_string = "MATCH (n) RETURN n"
# ans = conn.query(query_string, db='neo4j')
# print(ans)


async def add_user(user_id, user_name, user_date):
    # print(user_id, user_name, user_date)
    exists = conn.query(f"MATCH (user:USER) WHERE user.user_id = {user_id} RETURN user", db='neo4j')

    if len(list(exists)) == 0:
        q = "CREATE (user:USER {user_id: r_1, user_name: 'r_2', user_date: 'r_3'})".replace("r_1",
            str(user_id)).replace("r_2", str(user_name)).replace("r_3", str(user_date))
        conn.query(q, db='neo4j')
        # print("No user")
    else:
        # print("User exists")
        pass


async def add_movie(data):
    lst = []
    for i, v in dict(data).items():
        lst.append(f"{i}: '{v}'")
    lst.append('likes: 0')
    q = "CREATE (movie:MOVIE {" + f"{', '.join(lst)}" + "})"
    conn.query(q, db='neo4j')


async def get_movie_genre(genre, amount=1):
    ans = conn.query(f"""MATCH (movie:MOVIE) WHERE movie.ganre = '{genre}' 
                        RETURN ID(movie), movie 
                        ORDER BY movie.likes DESC
                        SKIP {(amount-1) * 10}
                        LIMIT 10""", db='neo4j')
    return ans


async def get_movie_search(text, amount=1):
    ans = conn.query(f"""MATCH (movie:MOVIE)
                        WHERE toLower(movie.name) contains '{text}' OR movie.date = '{text}' OR toLower(movie.ganre) contains '{text}' OR
                         toLower(movie.actors) contains '{text}' OR toLower(movie.producer) contains '{text}' OR 
                         toLower(movie.description) contains '{text}'
                        RETURN ID(movie), movie 
                        ORDER BY movie.likes DESC
                        SKIP {(amount - 1) * 10}
                        LIMIT 10""", db='neo4j')
    return ans


async def get_movie_pop():
    ans = conn.query(f"""MATCH (movie:MOVIE) RETURN ID(movie), movie ORDER BY movie.likes DESC LIMIT 10""")
    return ans


async def get_movie_liked(user_id):
    ans = conn.query(f"""MATCH (user:USER) -[like:LIKES]-> (movie:MOVIE)
                            WHERE user.user_id = {user_id}
                            RETURN ID(movie), movie""")
    return ans


async def get_movie_id(movie_id):
    ans = conn.query(f"MATCH (m:MOVIE) WHERE ID(m) = {movie_id} RETURN m", db='neo4j')
    return ans


async def user_like_movie(user_id, movie_id):
    yes = conn.query(f"""MATCH (user:USER) -[like:LIKES]-> (movie:MOVIE)
                            WHERE user.user_id = {user_id} AND ID(movie) = {movie_id}
                            RETURN like""")

    if len(list(yes)) > 0:
        pass
    else:
        conn.query(f"""MATCH (user:USER), (movie:MOVIE)
                    WHERE ID(movie) = {movie_id} AND user.user_id = {user_id}
                    CREATE (user) -[:LIKES]-> (movie)
                    SET movie.likes = (movie.likes + 1)""")


