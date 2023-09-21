import sys
import pandas as pd
import sqlite3

from fonctions.fonctions import rechercher_article, rechercher_nos_articles, suppr_a_rechercher_0
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

            # Création notre BDD
            if retour_menu == 2:
                # Lecture du fichier CSV avec les colonnes sélectionnées
                selected_columns = ["id", "userRef", "source", "sourceRef", "stock", "ean13", "title", "location", "weight", "clientRef", "pictureUrl", "hsCode", "supplier", "taxRate", "isPack", "height", "length", "width", "otherRef1", "otherRef2", "otherRef3", "otherRef4", "otherRef5", "otherRef6", "otherRef7", "otherRef8", "otherRef9", "otherRef10", "otherRef11", "otherRef12", "otherRef13", "otherRef14", "otherRef15", "cdiscountPrice", "spartooPartnaireRef"]
                df = pd.read_csv('product_20230919071201_7204206.csv', sep=';', usecols=selected_columns)

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

            # Consultation BDD EAN
            if retour_menu == 3:
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
            if retour_menu == 4:
                sous_menu = Menus.sous_menu_4()
                if sous_menu == 1:
                    # Rechercher les article ayant pour titre A RECHERCHER
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
                if sous_menu == 2:
                    resultat = suppr_a_rechercher_0()
                    print(resultat)
                    input("tapez enter")

                    # Retour au menu
                    input("tapez enter pour continuer")
                    Lancement.depart()

            if retour_menu == 5:
                sys.exit("Merci et à bientôt !")


if __name__ == "__main__":
    print("Merci de commencer par lancer main.py")

