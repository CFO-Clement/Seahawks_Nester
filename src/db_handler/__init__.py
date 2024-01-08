# db_handler/__init__.py
"""
if __name__ == "__main__":
    db_name = "mydb"  # Remplacez par le nom de votre base de données MongoDB
    collection_name = "collectors"

    manager = CollectorManager(db_name, collection_name)

    # Récupérer les différents collectorName
    collector_names = manager.get_collector_names()
    print("Collector Names:", collector_names)

    # Récupérer les informations d'un collector spécifique
    collector_name_to_query = "unique_collector_name"  # Remplacez par le nom du collector que vous souhaitez interroger
    collector_info = manager.get_collector_info(collector_name_to_query)
    print("Collector Info:", collector_info)

    # Fermer la connexion MongoDB
    manager.client.close()
"""
from .db_handler import DBHandler