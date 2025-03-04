import json
import pandas as pd
from typing import List, Dict, Union
from datetime import datetime, date
from pathlib import Path
from PyPDF2 import PdfWriter, PdfReader
import os

class ExportService:
    @staticmethod
    def ensure_export_dir(export_type: str) -> str:
        """Crée et retourne le chemin du répertoire d'export."""
        base_dir = Path("exports")
        export_dir = base_dir / export_type
        export_dir.mkdir(parents=True, exist_ok=True)
        return str(export_dir)

    @staticmethod
    def generate_filename(base_name: str, extension: str) -> str:
        """Génère un nom de fichier unique avec timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.{extension}"

    @staticmethod
    def to_csv(data: List[Dict], filename: str = "github_activity") -> str:
        """Exporte les données au format CSV."""
        export_dir = ExportService.ensure_export_dir("csv")
        output_path = os.path.join(export_dir, ExportService.generate_filename(filename, "csv"))
        
        # Conversion des dates en format lisible
        formatted_data = []
        for item in data:
            formatted_item = item.copy()
            if "created_at" in formatted_item:
                formatted_item["created_at"] = formatted_item["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            formatted_data.append(formatted_item)
        
        df = pd.DataFrame(formatted_data)
        df.to_csv(output_path, index=False, encoding='utf-8')
        return output_path

    @staticmethod
    def to_json(data: List[Dict], filename: str = "github_activity") -> str:
        """Exporte les données au format JSON."""
        export_dir = ExportService.ensure_export_dir("json")
        output_path = os.path.join(export_dir, ExportService.generate_filename(filename, "json"))
        
        def datetime_handler(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            return str(obj)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, default=datetime_handler, indent=2, ensure_ascii=False)
        return output_path

    @staticmethod
    def to_pdf(data: Union[List[Dict], Dict], filename: str = "github_activity") -> str:
        """Exporte les données au format PDF."""
        export_dir = ExportService.ensure_export_dir("pdf")
        output_path = os.path.join(export_dir, ExportService.generate_filename(filename, "pdf"))
        
        # Création du contenu PDF
        df = pd.DataFrame(data if isinstance(data, list) else [data])
        
        # Utilisation de to_string pour un formatage plus contrôlé
        pdf_content = (
            f"Rapport d'activité GitHub\n"
            f"Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"{df.to_string()}\n"
        )
        
        # Création du PDF
        writer = PdfWriter()
        writer.add_page()
        page = writer.pages[0]
        page.extract_text = lambda: pdf_content
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return output_path 