import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapR = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, anno1, anno2):
        self._grafo.clear()
        self._idMapR.clear()

        team = DAO.getAllNodes()
        for a in team:
            self._idMapR[a.constructorId] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        for a in team:
            a.risultati_per_anno = DAO.getRisultatiPerCostruttore(a.constructorId, anno1, anno2)

            #SE NEL DAO RESTITUISCO GIà UN DIZIONARIO
            #a.risultati = DAO.getRisultatiPerCostruttore( a.constructorId, anno1, anno2 )

            a.gare_totali = 0
            a.gare_completate = 0 #SFRUTTO LA DATACLASS
            #for year in a.risultati_per_anno:
            for year,pilota, position in a.risultati_per_anno:
                a.gare_totali +=1 #per la ricorsione
                if position is not None:
                    a.gare_completate += 1
            #OPPURE
            #CREO DIZIONARIO PK NEL DAO RESTITUISCO UNA LISTA DI TUPLE
           # dizionario = {}
           # for anno, pilota, posizione in risultati_per_anno:
                #if anno not in dizionario:
                   # dizionario[anno] = []
                #dizionario[anno].append((pilota, posizione))

        print("3 - Informazioni recuperate")

        for i in range(len(team)):
            a1 =team[i]

            for j in range(i + 1, len(team)):
                a2 = team[j]

                # Entrambi devono aver corso nel periodo
                if (len(a1.risultati_per_anno) > 0 and
                        len(a2.risultati_per_anno) > 0):

                    peso = a1.gare_completate + a2.gare_completate


                    self._grafo.add_edge(a1, a2, weight=peso)



    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getConnessaInfo(self):
        components = list(nx.connected_components(self._grafo))
        if len(components) == 0:
            return 0, set(), []
        largest = max(components, key=len)

        pesi = {}

        for nodo in largest:
            maxPeso = 0
            for vicino in self._grafo.neighbors(nodo):
                peso = self._grafo[nodo][vicino]["weight"]

                if peso > maxPeso:
                    maxPeso = peso

            pesi[nodo] = maxPeso
        ordered_nodes = sorted( largest, key=lambda n: pesi[n],   reverse=True  )
        details = [(n, pesi[n]) for n in ordered_nodes]
        #QUESTO METODO VA USATO QUANDO CHIEDE DI STAMPARE SULL BASE DEL PESO
        return len(components), largest, details

    def getConnessaInfo2(self):
        # lo trasformo in non orientato pk richiesto di ignorare
        #grafo_non_orientato = self._grafo.to_undirected()
        # components = list(nx.connected_components(grafo_non_orientato))
        components = list(nx.connected_components(self._grafo))

        # Se il grafo è vuoto
        if len(components) == 0:
            return 0, set(), []

        # components = list(nx.connected_components(self._grafo))  # TROVO LE COMP CONNESSE e ci faccio una lista
        largest = max(components, key=len)  # trova la + grande

        # b. Film con maggior numero di archi uscenti
        # film_max_out = max(self._grafo.nodes, key=lambda n: self._grafo.out_degree(n))
        # relativo numero archi usenti
        # max_out = self._grafo.out_degree(film_max_out)

        # ORDINO PER  NUMERO ATTORI!!
        ordered_nodes = sorted(largest, key=lambda n: n.gare_completate, reverse=True)  # ordine decrescente
        # ORDINO PER  GRADO!!
       # ordered_nodes = sorted(largest, key=lambda n: grafo_non_orientato.degree(n), reverse=True)  # ordine decrescente
        details = [(n, n.gare_completate) for n in ordered_nodes]

        return len(components), largest, details

    #QUESTO ULTIMO METODO STAMPA L'ORDINE CORRETTO MA NON DA IL NUMERO DI PESO GIUSTO

    def _indiceSfortuna(self, team):
        if team.gare_totali == 0:
            return 0

        return 1 - team.gare_completate / team.gare_totali

    def getGruppoTeamSfortunati(self, K,M):
        self._best_path = []
        self._best_score = -1

        components = list(nx.connected_components(self._grafo))
        if len(components) == 0:
            return None, 0

        # Individuo la componente connessa maggiore
        largest = max(components, key=len)
        candidati = []
        for team in largest:
            # Conto gli anni distinti in cui il team ha partecipato
            anni = set()

            for anno, pilota, position in team.risultati_per_anno:
                anni.add(anno)

            if len(anni) >= M:
                candidati.append(team)

        # Verifico che ci siano almeno K team validi
        if len(candidati) < K:
            return None, 0
        # Il percorso parziale  NONparte con il nodo selezionato
        parziale = []
        self._ricorsione(parziale, parziale, 0, K, 0)

        return self._best_path, self._best_score

    def _ricorsione(self, candidati, parziale, start, K, score):
        # Caso terminale: ho scelto K team
        if len(parziale) == K:
            if score > self._best_score:
                self._best_score = score
                self._best_path = list(parziale)
            return

        # Provo ad aggiungere un team
        for i in range(start, len(candidati)):
            team = candidati[i]

            indice = self._indiceSfortuna(team)
            parziale.append(team)

            self._ricorsione(candidati, parziale, i + 1, K, score + indice)

            # Tolgo il team e provo un'altra combinazione
            parziale.pop()



