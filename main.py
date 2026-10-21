
import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"


def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    prezzoStr = 0

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti(
        "Deposito Strumenti Musicali",
        "Alessandro Visconti"
    )

    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(
        value=deposito.nome,
        size=38,
        weight=ft.FontWeight.BOLD
    )

    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(
        value=deposito.get_responsabile(),
        label="Responsabile"
    )

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(
        expand=True,
        spacing=5,
        padding=10,
        auto_scroll=True
    )

    # --- FUNZIONI PER MODIFICARE IL PREZZO ---

    def alza_prezzo(e):
        nonlocal prezzoStr

        prezzoStr = prezzoStr + 1
        targhetta_prezzo.value = f"{prezzoStr} €"
        page.update()

    def abbassa_prezzo(e):
        nonlocal prezzoStr

        if prezzoStr > 0:
            prezzoStr = prezzoStr - 1

        targhetta_prezzo.value = f"{prezzoStr} €"
        page.update()

    # --- FUNZIONE PER AGGIUNGERE UNO STRUMENTO ---

    def aggiungi_strumento(e):
        nonlocal prezzoStr

        try:
            anno = int(input_anno_strumento.value)
        except (ValueError, TypeError):
            alert.show_alert(
                "❌ L'anno di acquisto deve essere un numero intero."
            )
            return

        tipo = input_tipo_strumento.value
        marca = input_marca_strumento.value
        valore = prezzoStr

        strumento = deposito.aggiungi_strumento(
            tipo,
            marca,
            anno,
            valore
        )

        aggiorna_lista_strumenti()

        input_tipo_strumento.value = ""
        input_marca_strumento.value = ""
        input_anno_strumento.value = ""

        prezzoStr = 0
        targhetta_prezzo.value = f"{prezzoStr} €"

        alert.show_alert(
            f"✅ Strumento {strumento.codice} aggiunto con successo!"
        )

        page.update()

    # --- FUNZIONI APP ---

    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()

        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"

            lista_strumenti.controls.append(
                ft.Text(f"{stato} {strumento}")
            )

        page.update()

    # --- HANDLERS APP ---

    def cambia_tema(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if toggle_cambia_tema.value
            else ft.ThemeMode.LIGHT
        )

        toggle_cambia_tema.label = (
            "Tema scuro"
            if toggle_cambia_tema.value
            else "Tema chiaro"
        )

        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)

        txt_responsabile.value = (
            f"Responsabile: {deposito.get_responsabile()}"
        )

        page.update()

    # --- ELEMENTI PER L'INSERIMENTO DI UN NUOVO STRUMENTO ---

    txt_nuovo_strumento = ft.Text(
        "Aggiungi Nuovo Strumento",
        size=20
    )

    input_tipo_strumento = ft.TextField(label="Tipo")
    input_marca_strumento = ft.TextField(label="Marca")
    input_anno_strumento = ft.TextField(label="Anno di Acquisto")

    targhetta_prezzo = ft.Text(
        f"{prezzoStr} €",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    btn_alza_prezzo = ft.TextButton(
        content="^",
        width=30,
        height=30,
        on_click=alza_prezzo
    )

    btn_abbassa_prezzo = ft.TextButton(
        content="v",
        width=30,
        height=30,
        on_click=abbassa_prezzo
    )

    # --- EVENTI ---

    toggle_cambia_tema = ft.Switch(
        label="Tema scuro",
        value=True,
        on_change=cambia_tema
    )

    pulsante_conferma_responsabile = ft.Button(
        content="Conferma",
        on_click=conferma_responsabile
    )

    # Pulsante per aggiungere uno strumento
    btn_aggiungi_strumento = ft.Button(
        content="Aggiungi Strumento",
        on_click=aggiungi_strumento
    )

    # --- LAYOUT ---

    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),

        ft.Row(
            spacing=200,
            controls=[
                input_responsabile,
                pulsante_conferma_responsabile
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        # Sezione 3
        ft.Divider(),
        txt_nuovo_strumento,

        ft.Row(
            controls=[
                input_tipo_strumento,
                input_marca_strumento,
                input_anno_strumento,
                targhetta_prezzo,
                btn_alza_prezzo,
                btn_abbassa_prezzo
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        btn_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti
    )

    aggiorna_lista_strumenti()


ft.run(main)
