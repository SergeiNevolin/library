import geojson
import os
from db.db_manager import DBManager

class GeoReportService:
    def __init__(self, db_path):
        self.db_manager = DBManager(db_path)

    def generate_geojson_report(self):
        """Сформировать отчет о расположении читателей и выданных книгах в формате GeoJSON."""
        
        query = """
        SELECT 
            readers.name AS reader_name,
            readers.latitude AS latitude,
            readers.longitude AS longitude,
            books.title AS book_title
        FROM transactions
        JOIN readers ON transactions.reader_id = readers.id
        JOIN books ON transactions.book_id = books.id
        WHERE transactions.return_date IS NULL;
        """
        
        transactions_data = self.db_manager.fetch_all(query)
        
        if not transactions_data:
            print("Нет выданных книг.")
            return
    
        features = []
        
        for entry in transactions_data:
            reader_name, latitude, longitude, book_title = entry
            
            if latitude is None or longitude is None:
                continue

            feature = geojson.Feature(
                geometry=geojson.Point((longitude, latitude)),
                properties={
                    "reader_name": reader_name,
                    "book_title": book_title
                }
            )
            features.append(feature)
        
        feature_collection = geojson.FeatureCollection(features)
        
        reports_folder = "reports"
        
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)

        report_file = os.path.join(reports_folder, "readers_and_books.geojson")
        
        with open(report_file, "w") as f:
            geojson.dump(feature_collection, f)
        
        print(f"GeoJSON отчет сохранен в файл {report_file}.")
