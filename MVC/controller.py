import sys
import pandas as pd
import sqlite3

from fonctions.fonctions import rechercher_article, rechercher_nos_articles, suppr_a_rechercher_0
from fonctions.fonctions import article_sans_stock_presta, article_stock_presta, article_ss_description_presta
from fonctions.fonctions import rechercher_article_presta, suppr_ss_stock_presta
from MVC.view import Menus


class Lancement:
    @staticmethod
    def depart():
        retour_menu = 0
        while retour_menu == 0:
            retour_menu = Menus.menu_principal()

            # Création BDD EAN
            if retour_menu == 1:
                # Lecture du fichier CSV avec les colonnes sélectionnées
                selected_columns = ["code", "brand", "name", "categories", "url"]
                df = pd.read_csv('open4goods-full-gtin-dataset.csv', usecols=selected_columns)

                # Connexion à la base de données SQLite
                conn = sqlite3.connect('open4goods.db')

                # Écriture des données dans la table de la base de données
                df.to_sql('produits', conn, if_exists='replace', index=False)

                cursor = conn.cursor()

                # Création de l'index sur la colonne "code"
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_code ON produits (code)')

                # Enregistrement des modifications et fermeture de la connexion
                conn.commit()
                # Fermeture de la connexion
                conn.close()

                # Retour au menu
                input("Tapez une touche pour continuer")
                Lancement.depart()

            # Création notre BDD (ShippingBo)
            if retour_menu == 2:
                # Lecture du fichier CSV avec les colonnes sélectionnées
                selected_columns = ["id", "userRef", "source", "sourceRef", "stock", "ean13", "title", "location",
                                    "weight", "clientRef", "pictureUrl", "hsCode", "supplier", "taxRate", "isPack",
                                    "height", "length", "width", "otherRef1", "otherRef2", "otherRef3", "otherRef4",
                                    "otherRef5", "otherRef6", "otherRef7", "otherRef8", "otherRef9", "otherRef10",
                                    "otherRef11", "otherRef12", "otherRef13", "otherRef14", "otherRef15",
                                    "cdiscountPrice", "spartooPartnaireRef"]

                df = pd.read_csv('productShippingBo.csv', sep=';', usecols=selected_columns,
                                 low_memory=False)

                # Connexion à la base de données SQLite
                conn = sqlite3.connect('notreBDD.db')

                # Écriture des données dans la table de la base de données
                df.to_sql('produits', conn, if_exists='replace', index=False)

                cursor = conn.cursor()

                # Création de l'index sur la colonne "code"
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_code ON produits (ean13)')

                # Enregistrement des modifications et fermeture de la connexion
                conn.commit()
                # Fermeture de la connexion
                conn.close()

                # Retour au menu
                input("Tapez une touche pour continuer")
                Lancement.depart()

            # Création BDD issue de Prestashop
            if retour_menu == 3:
                # Lecture du fichier CSV avec les colonnes sélectionnées
                selected_columns = ["actif", "référence", "ean13", "id_product", "id_product_attribute",
                                    "description FR", "description courte FR", "nom FR", "nom avec attributs FR",
                                    "produits du pack", "prix HT", "prix TTC", "tva", "quantité", "quantité physique",
                                    "catégorie par défaut FR", "catégorie par défaut (chemin complet) FR",
                                    "catégories FR", "catégories (chemin complet) FR", "fabricant",
                                    "images : urls_to_all_for_product FR"]
                df = pd.read_csv('2023_09_26 complet_presta.csv', sep=';', usecols=selected_columns,
                                 encoding='latin-1')

                # Connexion à la base de données SQLite
                conn = sqlite3.connect('BDD_Presta.db')

                # Écriture des données dans la table de la base de données
                df.to_sql('produits', conn, if_exists='replace', index=False)

                cursor = conn.cursor()

                # Création de l'index sur la colonne "code"
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_code ON produits (ean13)')

                # Enregistrement des modifications et fermeture de la connexion
                conn.commit()
                # Fermeture de la connexion
                conn.close()

                # Retour au menu
                input("Tapez une touche pour continuer")
                Lancement.depart()

            # Consultation BDD EAN
            if retour_menu == 4:
                # Demander à l'utilisateur de saisir un code
                code = input('Veuillez entrer le code de l\'article que vous recherchez : ')

                # Rechercher l'article
                article = rechercher_article(code)

                # Afficher les résultats
                if article:
                    print('Résultat de la recherche :')
                    print('Code :', article[0])
                    print('Marque :', article[1])
                    print('Nom :', article[2])
                    print('Catégories :', article[3])
                    print('URL :', article[4])
                else:
                    print('Aucun article trouvé avec ce code.')

                # Retour au menu
                input("tapez enter pour continuer")
                Lancement.depart()

            # Consultation notre BDD
            if retour_menu == 5:
                sous_menu = Menus.sous_menu_5()

                # Rechercher les article ayant pour titre A RECHERCHER
                if sous_menu == 1:
                    code = "A RECHERCHER"
                    stock = 0
                    article_total = rechercher_nos_articles(code, stock)
                    stock = 1
                    article_supp_0 = rechercher_nos_articles(code, stock)

                    # Afficher les résultats
                    if article_total:
                        print("Il y a ", len(article_total), "articles ayant pour titre 'A RECHERCHER' à afficher")
                        input('Résultat de la recherche :')
                        for a in article_total:
                            print(a[0], a[4])
                        input('taper enter')
                    if article_supp_0:
                        print(len(article_supp_0), "de ces articles ont un stock supérieur à 0")
                        input('Résultat de la recherche :')
                        for a in article_supp_0:
                            print(a[0], a[4])
                        input('taper enter')
                    else:
                        print('Aucun article trouvé avec ce code.')

                    # Retour au menu
                    input("Tapez une touche pour continuer")
                    Lancement.depart()

                # Supprimer les A RECHERCHER dont le stock est à 0
                if sous_menu == 2:
                    resultat = suppr_a_rechercher_0()
                    print(resultat)
                    input("tapez enter")

                    # Retour au menu
                    input("tapez enter pour continuer")
                    Lancement.depart()

                # Compter le nombre de produits dans la BDD
                if sous_menu == 3:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('notreBDD.db')

                    # Créer un curseur
                    cursor = conn.cursor()

                    # Exécuter une requête SQL pour compter le nombre de lignes dans la table "produits"
                    cursor.execute('SELECT COUNT(*) FROM produits')

                    # Récupérer le résultat
                    count = cursor.fetchone()[0]

                    # Fermer la connexion à la base de données
                    conn.close()

                    # Afficher le nombre de produits
                    print(f'Il y a {count} produits dans la base de données.')
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Créer une table avec les produits en stock
                if sous_menu == 4:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('notreBDD.db')
                    cursor = conn.cursor()

                    # Créer la table "produits_avec_stock" avec la même structure que "produits"
                    cursor.execute("PRAGMA table_info(produits)")
                    table_structure = ', '.join([f'{column[1]} {column[2]}' for column in cursor.fetchall()])
                    cursor.execute(f"CREATE TABLE produits_avec_stock ({table_structure})")

                    # Insérer les produits dont le stock est supérieur ou égal à 1 dans la nouvelle table
                    cursor.execute("INSERT INTO produits_avec_stock SELECT * FROM produits WHERE stock >= 1")

                    # Valider la transaction
                    conn.commit()

                    # Exécuter une requête SQL pour compter le nombre de lignes dans la table "produits"
                    cursor.execute('SELECT COUNT(*) FROM produits_avec_stock')

                    # Récupérer le résultat
                    count = cursor.fetchone()[0]

                    # Fermer la connexion à la base de données
                    conn.close()

                    # Afficher le nombre de produits
                    print(f'Il y a {count} produits dans la table "produits_avec_stock".')
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Exporter les produits avec stock en CSV
                if sous_menu == 5:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('notreBDD.db')

                    # Charger les données de la table "produits_avec_stock" dans un DataFrame Pandas
                    query = 'SELECT * FROM produits_avec_stock'
                    df = pd.read_sql_query(query, conn)

                    # Fermer la connexion à la base de données SQLite
                    conn.close()

                    # Exporter le DataFrame dans un fichier CSV avec le point-virgule comme séparateur
                    df.to_csv('CSV/produits_avec_stock.csv', sep=';', index=False)

                    print("Opération réussie")
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Afficher le nombre de produits dans la table et le nom des colonnes
                if sous_menu == 6:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('notreBDD.db')
                    cursor = conn.cursor()

                    # Exécuter la commande SQL PRAGMA pour obtenir les informations sur la table
                    cursor.execute('PRAGMA table_info(produits_avec_stock)')

                    # Récupérer les résultats et afficher les entêtes de colonnes
                    columns_info = cursor.fetchall()
                    column_names = [column[1] for column in columns_info]

                    cursor.execute('SELECT COUNT(*) FROM produits_avec_stock')

                    # Récupérer le résultat
                    count = cursor.fetchone()[0]

                    # Fermer la connexion à la base de données
                    conn.close()

                    # Afficher le nombre de produits
                    print(f'Il y a {count} produits dans la base de données.')
                    input("Tapez enter pour continuer")

                    # Afficher les entêtes de colonnes
                    print("Entêtes de colonnes de la table produits_avec_stock:")
                    print(column_names)
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Transfert des descriptions de prestashop vers BDD ShippingBo
                if sous_menu == 7:
                    # Établir une connexion à la base de données "BDD_Prest.db"
                    conn_prest = sqlite3.connect('BDD_Presta.db')
                    cursor_prest = conn_prest.cursor()

                    # Établir une connexion à la base de données "notreBDD.db"
                    conn_notre = sqlite3.connect('notreBDD.db')
                    cursor_notre = conn_notre.cursor()

                    # Interroger la base de données "BDD_Prest.db" pour obtenir les correspondances de codes EAN13
                    cursor_prest.execute('SELECT ean13, "description FR" FROM produits')
                    ean13_description_mapping = {row[0]: row[1] for row in cursor_prest.fetchall()}

                    # Mettre à jour la table "produits_avec_stock" avec les descriptions correspondantes
                    count = 0
                    for ean13, description in ean13_description_mapping.items():
                        count += 1
                        cursor_notre.execute('UPDATE produits_avec_stock SET description = ? WHERE ean13 = ?',
                                             (description, ean13))

                    # Valider la transaction et fermer les connexions aux bases de données
                    conn_notre.commit()
                    conn_notre.close()
                    conn_prest.close()

                    # Afficher le nombre de produits
                    print(f'Nous avons ajouté {count} descriptions dans la base de données.')
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                if sous_menu == 8:
                    # Établir une connexion à la base de données "BDD_Prest.db"
                    conn_prest = sqlite3.connect('BDD_Presta.db')
                    cursor_prest = conn_prest.cursor()

                    # Établir une connexion à la base de données "notreBDD.db"
                    conn_notre = sqlite3.connect('notreBDD.db')
                    cursor_notre = conn_notre.cursor()

                    # Extraire les codes EAN13 de la table "produits" dans "BDD_Prest.db"
                    cursor_prest.execute('SELECT référence FROM produits')
                    ean13_prest_list = [row[0] for row in cursor_prest.fetchall()]

                    # Extraire les codes EAN13 de la table "produits_avec_stock" dans "notreBDD.db"
                    cursor_notre.execute('SELECT userRef FROM produits_avec_stock')
                    ean13_notre_list = [row[0] for row in cursor_notre.fetchall()]

                    # Comparer les listes pour identifier les correspondances
                    correspondances = set(ean13_prest_list).intersection(ean13_notre_list)

                    # Afficher les correspondances
                    print("Codes EAN13 communs entre les deux bases de données :")
                    for ean13 in correspondances:
                        cursor_prest.execute('SELECT "description FR" FROM produits WHERE référence = ?', (ean13,))
                        result = cursor_prest.fetchone()
                        if result is not None:
                            description = result[0]
                        else:
                            description = "None"
                        cursor_notre.execute('UPDATE produits_avec_stock SET description = ? WHERE userRef = ?',
                                             (description, ean13))
                        print(ean13, description, "- OK")

                    print("Il y en a ", len(correspondances))

                    # Fermer les connexions aux bases de données
                    conn_prest.close()
                    conn_notre.close()

            # Consultation BDD Presta
            if retour_menu == 6:
                sous_menu = Menus.sous_menu_6()

                # Compter les articles sans stock, avec stock et total
                if sous_menu == 1:
                    articles_ss_stock = article_sans_stock_presta()
                    print("Il y a", str(len(articles_ss_stock)), "articles dont le stock est à 0 !")
                    input("tapez enter pour continuer")
                    articles_en_stock = article_stock_presta()
                    print("Il y a", str(len(articles_en_stock)), "articles avec du stock !")
                    input("tapez enter pour continuer")
                    nb_articles_total = len(articles_ss_stock) + len(articles_en_stock)
                    print("Il y a actuellement", str(nb_articles_total), "articles dans la BDD.")
                    input("tapez enter pour continuer")
                    Lancement.depart()

                # Articles sans description mais avec stock
                if sous_menu == 2:
                    articles_ss_description = article_ss_description_presta()
                    print("Il y a actuellement", str(len(articles_ss_description)),
                          "articles sans description mais avec du stock.")
                    input("tapez enter pour continuer")
                    Lancement.depart()

                # Recherche par ean dans BDD Prestashop
                if sous_menu == 3:
                    code = input('Veuillez entrer le code de l\'article que vous recherchez : ')

                    # Rechercher l'article
                    articles = rechercher_article_presta(code)

                    if articles:
                        for article in articles:
                            print(" ")
                            print("actif :", article[0])
                            print("référence :", article[1])
                            print("ean13 :", article[2])
                            print("id_product :", article[3])
                            print("id_product_attribute :", article[4])
                            print("description FR :", article[5])
                            print("description courte FR :", article[6])
                            print("nom FR :", article[7])
                            print("nom avec attributs FR :", article[8])
                            print("produits du pack :", article[9])
                            print("prix HT :", article[10])
                            print("prix TTC :", article[11])
                            print("tva :", article[12])
                            print("quantité :", article[13])
                            print("quantité physique :", article[14])
                            print("catégorie par défaut FR :", article[15])
                            print("catégorie par défaut (chemin complet) FR :", article[16])
                            print("catégories FR :", article[17])
                            print("catégories (chemin complet) FR :", article[18])
                            print("fabricant :", article[19])
                            print("images : urls_to_all_for_product FR :", article[20])
                            print(" ")
                            input("tapez enter pour continuer")
                    else:
                        print("Nous n'avons pas trouvé d'article avec ce code ean !")

                    input("tapez enter pour continuer")
                    Lancement.depart()

                # Supprimer les articles sans stock
                if sous_menu == 4:
                    suppression = suppr_ss_stock_presta()
                    print(suppression)
                    input("tapez enter pour continuer")
                    Lancement.depart()

                # Création du CSV des produits avec stocks et sans description
                if sous_menu == 5:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD_Presta.db')

                    # Charger les données de la table "produits_avec_stock" dans un DataFrame Pandas
                    query = 'SELECT * FROM produits WHERE "description FR" IS NULL AND quantité >= 1'
                    df = pd.read_sql_query(query, conn)

                    # Fermer la connexion à la base de données SQLite
                    conn.close()

                    # Exporter le DataFrame dans un fichier CSV avec le point-virgule comme séparateur
                    df.to_csv('CSV/produits_avec_stock_presta.csv', sep=';', index=False)

                    print("Opération réussie")
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                if sous_menu == 6:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD_Presta.db')

                    # Charger les données de la table "produits_avec_stock" dans un DataFrame Pandas
                    query = 'SELECT * FROM produits WHERE quantité >= 1'
                    df = pd.read_sql_query(query, conn)

                    # Fermer la connexion à la base de données SQLite
                    conn.close()

                    # Exporter le DataFrame dans un fichier CSV avec le point-virgule comme séparateur
                    df.to_csv('CSV/tous_produits_avec_stock_presta.csv', sep=';', index=False)

                    print("Opération réussie")
                    input("Tapez enter pour continuer")
                    Lancement.depart()

            # Création / remplissage et consultation de la BDD tri
            if retour_menu == 7:
                sous_menu = Menus.sous_menu_7()
                # Création
                if sous_menu == 1:
                    pass

                # Remplissage manuel
                if sous_menu == 2:
                    pass

                # Remplissage par CSV
                if sous_menu == 3:
                    pass

            # Quitter
            if retour_menu == 8:
                sys.exit("Merci et à bientôt !")


if __name__ == "__main__":
    print("Merci de commencer par lancer main.py")
