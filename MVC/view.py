class Menus:
    @staticmethod
    def menu_principal():
        print("1-Créer la base de données EAN")
        print("2-créer la base de données de nos produits (ShippingBo)")
        print("3-Créer la base de données des produits issus de Prestashop")
        print("4-faire une requête BDD EAN")
        print("5-faire une requête sur nos produits (ShippingBo)")
        print("6-faire une requête sur la BDD Prestashop")
        print("7-création, remplissage et requête BDD Tri")
        print("8-quitter")
        choix = int(input("que souhaitez vous faire ?"))
        return choix

    @staticmethod
    def sous_menu_5():
        print("1-Consulter les produits 'A RECHERCHER'")
        print("2-Supprimer les A RECHERCHER dont le stock est à 0")
        print("3-Compter le nombre de produits dans la BDD")
        print("4-Copier les produits ayant du stock dans une table à part")
        print("5-Créer un CSV de la table produits_avec_stock")
        print("6-Afficher le nombre de produits dans la table et le nom des colonnes")
        print("7-Transfert des descriptions depuis prestashop")
        choix = int(input("que souhaitez vous faire ?"))
        return choix

    @staticmethod
    def sous_menu_6():
        print("1-compter le nombre d'articles")
        print("2-compter le nombre d'articles sans description")
        print("3-recherche EAN")
        print("4-supprimer les articles sans stock")
        print("5-Création du CSV des produits avec stock et sans description")
        print("6-Création du CSV des produits avec du stock")
        choix = int(input("Que voulez vous faire ?"))
        return choix

    @staticmethod
    def sous_menu_7():
        print("1-créer les bases de données")
        print("2-remplir manuellement les BDD")
        print("3-remplir avec un CSV")
        choix = int(input("Que voulez vous faire ?"))
        return choix


if __name__ == "__main__":
    print("Merci de commencer par lancer main.py")
