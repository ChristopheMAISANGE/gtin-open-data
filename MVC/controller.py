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
                conn = sqlite3.connect('BDD/open4goods.db')

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
                conn = sqlite3.connect('BDD/notreBDD.db')

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
                df = pd.read_csv('CSV/produits_presta.csv', sep=';', usecols=selected_columns,
                                 encoding='latin-1')

                # Connexion à la base de données SQLite
                conn = sqlite3.connect('BDD/BDD_Presta.db')

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
                    conn = sqlite3.connect('BDD/notreBDD.db')

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
                    conn = sqlite3.connect('BDD/notreBDD.db')
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
                    conn = sqlite3.connect('BDD/notreBDD.db')

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
                    conn = sqlite3.connect('BDD/notreBDD.db')
                    cursor = conn.cursor()

                    # Exécuter la commande SQL PRAGMA pour obtenir les informations sur la table
                    cursor.execute('PRAGMA table_info(produits_avec_stock)')

                    # Récupérer les résultats et afficher les en-têtes de colonnes
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

                    # Afficher les en-têtes de colonnes
                    print("En-têtes de colonnes de la table produits_avec_stock:")
                    print(column_names)
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Transfert des descriptions de prestashop vers BDD ShippingBo
                if sous_menu == 7:
                    # Établir une connexion à la base de données "BDD_Prest.db"
                    conn_prest = sqlite3.connect('BDD/BDD_Presta.db')
                    cursor_prest = conn_prest.cursor()

                    # Établir une connexion à la base de données "notreBDD.db"
                    conn_notre = sqlite3.connect('BDD/notreBDD.db')
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
                    conn_prest = sqlite3.connect('BDD/BDD_Presta.db')
                    cursor_prest = conn_prest.cursor()

                    # Établir une connexion à la base de données "notreBDD.db"
                    conn_notre = sqlite3.connect('BDD/notreBDD.db')
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

                # Retour au menu principal
                if sous_menu == 10:
                    print(" ")
                    Lancement.depart()

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
                    conn = sqlite3.connect('BDD/BDD_Presta.db')

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

                # Exporter les articles qui ont du stock dans un CSV
                if sous_menu == 6:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD/BDD_Presta.db')

                    # Charger les données de la table dans un DataFrame Pandas
                    query = 'SELECT * FROM produits WHERE quantité >= 1'
                    df = pd.read_sql_query(query, conn)

                    # Fermer la connexion à la base de données SQLite
                    conn.close()

                    # Exporter le DataFrame dans un fichier CSV avec le point-virgule comme séparateur
                    df.to_csv('CSV/tous_produits_avec_stock_presta.csv', sep=';', index=False)

                    print("Opération réussie")
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Retour au menu principal
                if sous_menu == 10:
                    print(" ")
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

                # Retour au menu principal
                if sous_menu == 10:
                    print(" ")
                    Lancement.depart()

            # Gestion des produits à traiter
            if retour_menu == 8:
                sous_menu = Menus.sous_menu_8()

                # Créer la base de donner à partir du CSV
                if sous_menu == 1:
                    # Lecture du fichier CSV avec les colonnes sélectionnées
                    selected_columns = ["ID_produit", "userRef", "stock", "ean13", "description", "bullet_points",
                                        "etat_produit", "Prix_vente_mini", "Prix_vente_conseil", "Categorie", "title",
                                        "weight", "Photo1", "Photo2", "Photo3", "Photo4", "Photo5", "Photo6",
                                        "supplier", "taxRate", "isPack", "height", "length", "width", "otherRef1",
                                        "Mode_transport", "Prix_achat", "Prix_transport", "otherRef5", "otherRef6",
                                        "otherRef7", "otherRef8", "otherRef9", "otherRef10", "otherRef11",
                                        "otherRef14"]

                    df = pd.read_csv('CSV/Articles_a_traiter.csv', sep=';', usecols=selected_columns,
                                     encoding='latin-1', low_memory=False)

                    # Connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD/articles_a_traiter.db')

                    # Écriture des données dans la table de la base de données
                    df.to_sql('produits', conn, if_exists='replace', index=False)

                    cursor = conn.cursor()

                    # Création de l'index sur la colonne "code"
                    cursor.execute('CREATE INDEX IF NOT EXISTS idx_code ON produits (userRef)')

                    # Enregistrement des modifications et fermeture de la connexion
                    conn.commit()
                    # Fermeture de la connexion
                    conn.close()

                    # Retour au menu
                    input("Tapez une touche pour continuer")
                    Lancement.depart()

                # Compter le nombre d'articles
                if sous_menu == 2:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD/articles_a_traiter.db')

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

                # Afficher et compter les produits qui ne contiennent pas EAN ou ean en userRef
                if sous_menu == 3:
                    # Établir une connexion à la base de données
                    conn = sqlite3.connect('BDD/articles_a_traiter.db')
                    cursor = conn.cursor()

                    cursor.execute('''
                        SELECT ID_produit, userRef, stock, ean13, title, Photo1, supplier, Mode_transport, Prix_achat
                        FROM produits
                        WHERE userRef NOT LIKE "%EAN%" AND userRef NOT LIKE "%ean%"
                    ''')

                    # Récupérer tous les résultats
                    resultats = cursor.fetchall()

                    # Afficher le nombre de produits trouvés
                    print(" ")
                    print("Nombre de produits sans 'EAN' ou 'ean' dans userRef :", len(resultats))
                    print(" ")
                    input("Tapez enter pour continuer")

                    # Afficher les produits sous la forme souhaitée
                    for row in resultats:
                        print("ID_produit:", row[0])
                        print("userRef:", row[1])
                        print("stock:", row[2])
                        print("ean13:", row[3])
                        print("title:", row[4])
                        print("Photo1:", row[5])
                        print("supplier:", row[6])
                        print("Mode_transport:", row[7])
                        print("Prix_achat:", row[8])
                        print(" ")

                    # Fermer la connexion à la base de données
                    conn.close()

                    # Retour au menu
                    input("Tapez une touche pour continuer")
                    Lancement.depart()

                # Afficher et compter les produits qui contiennent EAN ou ean en userRef
                if sous_menu == 4:
                    # Établir une connexion à la base de données
                    conn = sqlite3.connect('BDD/articles_a_traiter.db')
                    cursor = conn.cursor()

                    cursor.execute('''
                                    SELECT userRef, ean13
                                    FROM produits
                                    WHERE userRef LIKE "%EAN%" AND userRef LIKE "%ean%"
                                ''')

                    # Récupérer tous les résultats
                    resultats = cursor.fetchall()

                    # Afficher le nombre de produits trouvés
                    print(" ")
                    print("Nombre de produits avec 'EAN' ou 'ean' dans userRef :", len(resultats))
                    print(" ")
                    input("Tapez enter pour continuer")

                    # Afficher les produits sous la forme souhaitée
                    for row in resultats:
                        print("userRef:", row[0], "ean13:", row[1])

                    # Fermer la connexion à la base de données
                    conn.close()

                    # Retour au menu
                    input("Tapez une touche pour continuer")
                    Lancement.depart()

                # Mise à jour des descriptions, Bullet points, catégories et Photos
                if sous_menu == 5:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD/articles_a_traiter.db')

                    # Lire le fichier CSV dans un DataFrame
                    csv_file1 = 'CSV/import_sync_centric_1.csv'
                    csv_file2 = 'CSV/import_sync_centic_2.csv'
                    df_csv = pd.read_csv(csv_file1, sep=',', encoding='latin-1')
                    df_csv2 = pd.read_csv(csv_file2, sep=',', encoding='latin-1')

                    # Convertir la colonne 'ean13' en chaînes de caractères (str)
                    df_csv['ean'] = df_csv['ean'].astype(str)
                    df_csv2['ean'] = df_csv2['ean'].astype(str)

                    # Supprimer le ".0" de chaque valeur dans la colonne 'ean13'
                    df_csv['ean'] = df_csv['ean'].str.replace('.0', '')
                    df_csv2['ean'] = df_csv2['ean'].str.replace('.0', '')


                    # Initialiser un compteur pour le nombre de produits mis à jour
                    nombre_de_produits_mis_a_jour = 0

                    # Parcourir le DataFrame du 1er CSV et mettre à jour la base de données
                    for index, row in df_csv.iterrows():
                        ean13 = row['ean']
                        description_fr = row['description']
                        bullet_points_fr = row['features']
                        photo2_fr = row['additional_image_1']
                        photo3_fr = row['additional_image_2']
                        photo4_fr = row['additional_image_3']
                        photo5_fr = row['additional_image_4']
                        photo6_fr = row['additional_image_5']


                        # Vérifier si l'ean13 existe dans la base de données
                        cursor = conn.cursor()
                        cursor.execute('SELECT * FROM produits WHERE ean13 = ?', (ean13,))
                        existing_product = cursor.fetchone()

                        if existing_product:
                            # Mettre à jour les colonnes de la base de données
                            cursor.execute('''
                                UPDATE produits
                                SET description = ?, bullet_points = ?, Photo2 = ?, Photo3 = ?, Photo4 = ?, 
                                Photo5 = ?, Photo6 = ?
                                WHERE ean13 = ?
                            ''', (description_fr, bullet_points_fr, photo2_fr, photo3_fr, photo4_fr, photo5_fr,
                                  photo6_fr, ean13))

                            # Incrémenter le compteur
                            nombre_de_produits_mis_a_jour += 1

                    # Parcourir le DataFrame du 2nd CSV et mettre à jour la base de données
                    for index, row in df_csv2.iterrows():
                        ean13 = row['ean']
                        description_fr = row['description']
                        bullet_points_fr = row['features']
                        photo2_fr = row['additional_image_1']
                        photo3_fr = row['additional_image_2']
                        photo4_fr = row['additional_image_3']
                        photo5_fr = row['additional_image_4']
                        photo6_fr = row['additional_image_5']

                        # Vérifier si l'ean13 existe dans la base de données
                        cursor = conn.cursor()
                        cursor.execute('SELECT * FROM produits WHERE ean13 = ?', (ean13,))
                        existing_product = cursor.fetchone()

                        if existing_product:
                            # Mettre à jour les colonnes de la base de données
                            cursor.execute('''
                                UPDATE produits
                                SET description = ?, bullet_points = ?, Photo2 = ?, Photo3 = ?, Photo4 = ?, 
                                Photo5 = ?, Photo6 = ?
                                WHERE ean13 = ?
                                                    ''', (
                            description_fr, bullet_points_fr, photo2_fr, photo3_fr, photo4_fr, photo5_fr,
                            photo6_fr, ean13))

                            # Incrémenter le compteur
                            nombre_de_produits_mis_a_jour += 1

                    # Valider la transaction et fermer la connexion
                    conn.commit()
                    conn.close()

                    # Afficher le nombre de produits mis à jour
                    print("Nombre de produits mis à jour :", nombre_de_produits_mis_a_jour)
                    # Retour au menu
                    print(" ")
                    input("Tapez une touche pour continuer")
                    Lancement.depart()

                # Afficher et compter tous les ean de 13 chiffres uniquement
                if sous_menu == 6:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD/articles_a_traiter.db')

                    # Créer un curseur
                    cursor = conn.cursor()

                    # Exécuter la requête SQL pour rechercher les produits avec un ean13 de 13 chiffres
                    cursor.execute(
                        "SELECT ean13 FROM produits WHERE LENGTH(ean13) = 13 AND ean13 NOT LIKE '%[^0-9]%'")

                    # Récupérer les résultats de la requête
                    results = cursor.fetchall()

                    # Exécuter une requête SQL pour compter le nombre de lignes dans la table "produits"
                    cursor.execute('SELECT COUNT(*) FROM produits')

                    # Récupérer le résultat
                    count = cursor.fetchone()[0]

                    print(str(len(results)), "sur", count, "produits")
                    input("tapez enter pour continuer")

                    # Afficher les produits trouvés
                    for product in results:
                        print(product)

                    # Fermer la connexion à la base de données
                    conn.close()

                    # Créer un DataFrame pandas à partir des résultats
                    df = pd.DataFrame(results, columns=['ean13'])

                    # Exporter le DataFrame dans un fichier CSV
                    df.to_csv('CSV/ean13_valides.csv', index=False)

                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Exporter la BDD dans un CSV
                if sous_menu == 7:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD/articles_a_traiter.db')

                    # Charger les données de la table dans un DataFrame Pandas
                    query = 'SELECT * FROM produits'
                    df = pd.read_sql_query(query, conn)

                    # Fermer la connexion à la base de données SQLite
                    conn.close()

                    # Exporter le DataFrame dans un fichier CSV avec le point-virgule comme séparateur
                    df.to_csv('CSV/tous_produits_modifies.csv', sep=';', index=False)

                    print("Opération réussie")
                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Compter les articles sans description
                if sous_menu == 8:
                    # Établir une connexion à la base de données SQLite
                    conn = sqlite3.connect('BDD/articles_a_traiter.db')

                    # Créer un curseur
                    cursor = conn.cursor()

                    # Exécuter la requête SQL pour compter les produits sans description
                    cursor.execute("SELECT COUNT(*) FROM produits WHERE description IS NULL OR description = ''")

                    # Récupérer le résultat
                    count = cursor.fetchone()[0]

                    # Afficher le nombre de produits sans description
                    print("Nombre de produits sans description :", count)

                    # Fermer la connexion à la base de données
                    conn.close()

                    input("Tapez enter pour continuer")
                    Lancement.depart()

                # Retour au menu principal
                if sous_menu == 10:
                    print(" ")
                    Lancement.depart()

            # Quitter
            if retour_menu == 10:
                sys.exit("Merci et à bientôt !")


if __name__ == "__main__":
    print("Merci de commencer par lancer main.py")
