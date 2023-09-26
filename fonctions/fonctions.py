import sqlite3


def rechercher_article(code):
    conn = sqlite3.connect('open4goods.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour rechercher l'article par code
    cursor.execute('SELECT * FROM produits WHERE code = ?', (code,))
    article = cursor.fetchone()

    conn.close()
    return article


def rechercher_nos_articles(code, stock):
    conn = sqlite3.connect('notreBDD.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour rechercher l'article par code
    cursor.execute('SELECT * FROM produits WHERE title = ? AND stock >= ?', (code, stock,))
    article = cursor.fetchall()

    conn.close()
    return article


def suppr_a_rechercher_0():
    conn = sqlite3.connect('notreBDD.db')
    cursor = conn.cursor()

    # Executer la suppression
    sur = input("Êtes vous sûr de vouloir supprimer les entrées A RECHERCHER dont le stock est à 0 ?")
    if sur == "oui":
        try:
            code = "A RECHERCHER"
            cursor.execute('DELETE FROM produits WHERE title = ? and stock < 1', (code,))
            conn.commit()
            resultat = "Les produits A RECHERCHER dont le stock est à 0 ont été supprimés"
            cursor.close()
            conn.close()
        except sqlite3.Error as error:
            resultat = "Erreur lors du suppression dans la table :", error
    if sur == "non":
        resultat = "D'accord, nous n'avons rien supprimé"
    return resultat


if __name__ == "__main__":
    print("Merci de commencer par lancer main.py")
