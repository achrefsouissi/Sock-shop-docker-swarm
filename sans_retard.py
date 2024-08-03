import requests
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fonction pour mesurer le temps de réponse d'une URL
def measure_response_time(url, latency_coefficient):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    return (end_time - start_time) * 1000 * latency_coefficient  # Convertir en millisecondes avec un coefficient de latence

# URLs de chaque étape
urls = {
    "login": "http://192.168.56.100/index.html",
    "catalogue": "http://192.168.56.100/category.html",
    "panier": "http://192.168.56.100/basket.html",
    "paiement": "http://192.168.56.100/customer-orders.html",    
}

# Fonction pour calculer les temps de réseau et de traitement pour un lot de requêtes
def calculate_times(batch_size, num_iterations):
    total_network_time = 0
    total_processing_time = 0

    max_threads = 10
    latency_coefficient = batch_size / 10  # Coefficient de latence proportionnel à la taille du lot

    for _ in range(num_iterations):
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(measure_response_time, url, latency_coefficient) for url in urls.values() for _ in range(batch_size)]
            batch_network_time = sum(future.result() for future in as_completed(futures))

        # Calcul du temps de traitement
        batch_processing_time = (batch_network_time / 1000) + (0.5 * batch_size / 1000)  # Conversion en secondes

        total_network_time += batch_network_time
        total_processing_time += batch_processing_time

    # Calcul des temps moyens
    avg_network_time = (total_network_time / (num_iterations * len(urls) * batch_size)) / 1000  # en secondes
    avg_processing_time = (total_processing_time / num_iterations)  # en secondes

    return avg_network_time, avg_processing_time

# Simuler des lots de requêtes de 10 à 100
batch_sizes = range(10, 101, 10)
network_times = []
processing_times = []
response_times = []
num_iterations = 7  # Nombre d'itérations pour obtenir des mesures plus stables

for batch_size in batch_sizes:
    print(f"Calculating for batch size: {batch_size}")
    avg_network_time, avg_processing_time = calculate_times(batch_size, num_iterations)
    network_times.append(avg_network_time)
    processing_times.append(avg_processing_time)
    response_times.append(avg_network_time + avg_processing_time)
    print(f"Batch size: {batch_size}, Average network time: {avg_network_time:.4f} s, Average processing time: {avg_processing_time:.4f} s, Average response time: {avg_network_time + avg_processing_time:.4f} s")

# Tracer les courbes
plt.figure(figsize=(12, 6))

plt.plot(batch_sizes, network_times, marker='o', color='blue', linestyle='-', label='Temps de réseau sans introduction de retard')
plt.plot(batch_sizes, processing_times, marker='x', color='green', linestyle='--', label='Temps de traitement sans introduction de retard')
plt.plot(batch_sizes, response_times, marker='s', color='red', linestyle=':', label='Temps de réponse sans introduction de retard')

plt.xlabel('Nombre de requêtes')
plt.ylabel('Temps (s)')
plt.title('Temps de Réseau, Temps de Traitement et Temps de Réponse en Fonction du Nombre de Requêtes')
plt.legend()
plt.grid(True)
plt.tight_layout()  # Pour un espacement clair et concis
plt.show()

