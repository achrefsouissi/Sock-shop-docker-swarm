from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente entre les requêtes, ici entre 1 et 3 secondes

    @task
    def test_catalogue_produits(self):
        self.client.get("http://192.168.99.107/category.html")

    @task
    def test_panier_achat(self):
        self.client.get("http://192.168.99.107/basket.html")

    @task
    def test_paiement(self):
        self.client.get("http://192.168.99.107/customer-orders.html?")

    @task
    def test_login(self):
        self.client.get("http://192.168.99.107/index.html")

    @task
    def test_progression_livraison(self):
        self.client.get("http://192.168.99.107/customer-order.html?order=/orders/669264dacbff270007a22dcc")

    @task
    def test_chercher_produit_rouge(self):
        self.client.get("http://192.168.99.107/category.html?tags=red")

# Lancement de Locust en mode standalone
if __name__ == "__main__":
    import time
    from locust.main import main

    # Utilisation de time.sleep pour simuler le temps d'exécution de votre script avant le lancement de Locust
    time.sleep(10)  # Par exemple, attendez 10 secondes avant de lancer Locust

    # Appel à la fonction main de Locust pour démarrer le serveur Locust en mode standalone
    main(["--headless", "-f", __file__])

