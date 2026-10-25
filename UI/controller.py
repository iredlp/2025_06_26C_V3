import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDAnno(self):
        try:
            anni = self._model.getAllYears()
            for y in anni:
                self._view._ddYear1.options.append(ft.dropdown.Option(y))
                self._view._ddYear2.options.append(ft.dropdown.Option(y))
                    #key=y.id,
                    #text=y.name))
            self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(ft.Text(f"Errore nel recupero degli anni: {ex}", color="red"))
            self._view.update_page()

    def handleBuildGraph(self, e):
        anno1 = self._view._ddYear1.value
        anno2 = self._view._ddYear2.value
       # categoria = self._view._ddcategory.value

        if not anno1:
            self._view.create_alert("Selezionare la prima data prima di creare il grafo.", color="red")
            return
        if not anno2:
            self._view.create_alert("Selezionare la seconda data prima di creare il grafo.", color="red")
            return
        #if not categoria:
         #   self._view.create_alert("Selezionare la CATEGORIA prima di creare il grafo.", color="red")
          #  return

        try:
            self._model.creaGrafo(anno1, anno2)
            self._view._txt_result.controls.append(ft.Text(f"Data selezionata: {anno1}", color="green"))
            self._view._txt_result.controls.append(ft.Text(f"Data selezionata: {anno2}\n", color="green"))
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)

            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
            #self.fillDDNodoStart(categoria)
            #self.fillDDNodoEnd(categoria)

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return
        self._view.update_page()


    def handlePrintDetails(self, e):
        numero, largest, details = self._model.getConnessaInfo()
        self._view._txt_result.controls.clear()

        self._view._txt_result.controls.append(
            ft.Text(f"Il grafo ha  {numero} componenti connesse\n", color="orange"))

        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa maggiore ha dimensione  {len(largest)}\n", color="green"))

        #for titolo in largest:
          #  self._view._txt_result.controls.append(ft.Text(f"{titolo} "))

        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa maggiore in ordine decrescente \n", color="green"))

        for titolo, numero_gare in details:
            self._view._txt_result.controls.append(ft.Text(f"{titolo}: {numero_gare} gare"))

        self._view.update_page()

    def handleCercaTeamSfortunati(self, e):
        self._view._txt_result.controls.clear()
        k = self._view._txtInSoglia.value
        # qui dovremmo fare i solti controlli sulla validità

        try:
            kInt = int(k)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red") )
            self._view.update_page()
            return
        if kInt <= 0:
            self._view.create_alert(
                "La soglia deve essere un intero positivo.", color="red")
            return

        m = self._view._txtInNumDiEdizioni.value
        # qui dovremmo fare i solti controlli sulla validità

        try:
            mInt = int(m)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red"))
            self._view.update_page()
            return
        if mInt <= 0:
            self._view.create_alert(
                "Il numero di edizioni deve essere un intero positivo.", color="red")
            return

        listTeam, bestScore = self._model.getGruppoTeamSfortunati( kInt, mInt)

        if listTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(
                f"Non ci sono abbastanza comoonenti connesse per trovare K team", color="red"))
            return

        self._view._txt_result.controls.append(ft.Text(
            f"Gruppo dei {kInt} team più sfortunati "
            f"(indice complessivo: {bestScore:.3f})", color="green"))
        # Stampo le informazioni di ogni regista
        for team in listTeam:
            indice = self._model._indiceSfortuna(team)
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{team.name}: indice di sfortuna = {indice:.3f}"
                )
            )

        self._view.update_page()


