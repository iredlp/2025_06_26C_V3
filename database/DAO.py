from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    @staticmethod
    def getAllConstructors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from constructors"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct r.`year` as year 
                    from races r
                     order by r.year DESC """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """  select distinct c.*
                from constructors c
               
                """

        cursor.execute(query)

        for row in cursor:
            results.append(Team(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getRisultatiPerCostruttore(idC, anno1,anno2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """  
                   select ra.`year` ,r.driverId  as pilota, r.`position` as position
                    from constructors c, results r , races ra
                    where c.constructorId =r.constructorId and c.constructorId =%s
                    and ra.raceId =r.raceId 
                    and ra.`year` between %s and %s
                   
                                    """
        cursor.execute(query, (idC,anno1,anno2))

        for row in cursor:
            results.append((row["year"],row["pilota"], row["position"]))

        #se volessi già inserire i valori in un dizionario già qui nel DAO
       # for row in cursor:
           # anno = row["year"]
           # pilota = row["pilota"]
          #  posizione = row["posizione_gara"]
           # if anno not in risultati:
               # risultati[anno] = []
           # risultati[anno].append((pilota, posizione)

        cursor.close()
        conn.close()
        return results
