#!/bin/bash
set -e   # Stopper à la première erreur
echo "=== Gametracker Pipeline ==="

echo "[1/4] Attente de la base de données..."
./scripts/wait-for-db.sh

echo "[2/4] Initialisation des tables..."
mysql --skip-ssl -h db -u root -proot game_db < scripts/init-db.sql

echo "[3/4] Exécution du pipeline ETL Python..."
python3 -m src.main

echo "[4/4] Génération du rapport..."
python3 -c "from src.report import generate_report; generate_report()"

echo "=== Pipeline terminé avec succès ==="