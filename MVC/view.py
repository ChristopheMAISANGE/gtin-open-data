class Menus:
    @staticmethod
    def menu_principal():
        print("1-Créer la base de données EAN")
        print("2-Créer la base de données de nos produits (ShippingBo)")
        print("3-Créer la base de données des produits issus de Prestashop")
        print("4-Faire une requête BDD EAN")
        print("5-Faire une requête sur nos produits (ShippingBo)")
        print("6-Faire une requête sur la BDD Prestashop")
        print("7-Création, remplissage et requête BDD Tri")
        print("8-Gestion des produits 'A traiter'")
        print("10-Quitter")
        choix = int(input("Que souhaitez vous faire ?"))
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
        print("8- ?????")
        print("10-Retour au menu principal")
        choix = int(input("que souhaitez vous faire ?"))
        return choix

    @staticmethod
    def sous_menu_6():
        print("1-Compter le nombre d'articles")
        print("2-Compter le nombre d'articles sans description")
        print("3-Recherche EAN")
        print("4-Supprimer les articles sans stock")
        print("5-Création du CSV des produits avec stock et sans description")
        print("6-Création du CSV des produits avec du stock")
        print("10-Retour au menu principal")
        choix = int(input("Que voulez vous faire ?"))
        return choix

    @staticmethod
    def sous_menu_7():
        print("1-Créer les bases de données")
        print("2-Remplir manuellement les BDD")
        print("3-Remplir avec un CSV")
        print("10-Retour au menu principal")
        choix = int(input("Que voulez vous faire ?"))
        return choix

    @staticmethod
    def sous_menu_8():
        print("1-Créer la base de donner à partir du CSV")
        print("2-Compter le nombre de produits dans la BDD")
        print("3-Afficher et compter les produits qui ne contiennent pas EAN ou ean en userRef")
        print("4-Afficher et compter les produits qui contiennent EAN ou ean en userRef")
        print("5-Mise à jour des descriptions, Bullet points, catégories et photo2")
        print("6-Afficher et compter tous les ean de 13 chiffres uniquement")
        print("10-Retour au menu principal")
        choix = int(input("Que voulez vous faire ?"))
        return choix


if __name__ == "__main__":
    print("Merci de commencer par lancer main.py")
