class Menus:
    @staticmethod
    def menu_principal():
        print("1-Créer la base de données EAN")
        print("2-créer la base de données de nos produits (ShippingBo)")
        print("3-Créer la base de données des produits issus de Prestashop")
        print("4-faire une requête BDD EAN")
        print("5-faire une requête sur nos produits (ShippingBo)")
        print("6-création, remplissage et requête BDD Tri")
        print("7-quitter")
        choix = int(input("que souhaitez vous faire ?"))
        return choix

    @staticmethod
    def sous_menu_4():
        print("1-Consulter les produits 'A RECHERCHER'")
        print("2-Supprimer les A RECHERCHER dont le stock est à 0")
        choix = int(input("que souhaitez vous faire ?"))
        return choix

    @staticmethod
    def sous_menu_5():
        print("1-créer les bases de données")
        print("2-remplir manuellement les BDD")
        print("3-remplir avec un CSV")


if __name__ == "__main__":
    print("Merci de commencer par lancer main.py")
