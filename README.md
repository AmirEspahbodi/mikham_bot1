# Mikham Bot Scraper Suite

A Python-based scraping and ingestion pipeline that collects business listings from **Google Maps** and **Neshan**, persists the results as Excel sheets, and then **imports** those listings into the Mikham platform. A lightweight **FastAPI** service exposes operational status and accepts new scrape requests by uploading structured Excel input.

The repository is organized as a small suite of cooperating services:

- **Scrapers** (`google/`, `neshan/`): Playwright-based browser automation that pulls listing data and writes it to Excel files.
- **Importer** (`importer/`): Browser automation that reads scraped Excel sheets and imports them into `https://mikham.me`.
- **API server** (`server/`): FastAPI service that provides a `/status` endpoint and accepts new scrape requests.

---

## Architecture & Data Flow

1. **Request Intake**
   - The FastAPI server reads an uploaded Excel sheet containing search parameters and enqueues search queries in Redis.
2. **Scrape Workers**
   - Google Maps and Neshan scraper processes dequeue search queries from Redis, open Playwright browser tabs, and scrape listing details.
   - Results are written to Excel files in `storage/not_imported_sheets/`.
3. **Importer**
   - The importer watches for not-yet-imported Excel sheets and automates form submission on Mikham.
   - Successfully processed sheets are moved to `storage/imported_sheets/`.

Redis is used as the **queue and state store**, while Excel files serve as the intermediate storage format between scraping and importing.

---

## Key Technologies

- **Python 3.12** (Poetry-managed dependencies)
- **Playwright** for headless browser automation
- **FastAPI** for the HTTP API
- **Redis** for queues and in-flight state
- **Pandas + OpenPyXL** for Excel read/write
- **Pydantic / pydantic-settings** for configuration and data validation

---

## Design Patterns & Structure

- **Singleton**: `RuntimeResource` (per scraper/importer) uses a Singleton metaclass to ensure a shared Playwright runtime within a process.
- **DAO (Data Access Object)**: Redis operations are isolated in `data/dao/redis.py` classes.
- **BO (Business Object)**: Domain-specific workflow objects live in `data/bo/` (e.g., scraping steps, importing steps).
- **DTO (Data Transfer Object)**: Pydantic `Listing` models define the structure of scraped listings (`data/dto/listing.py`).

This separation makes scraping, data access, and workflow logic independently testable and easier to evolve.

---

## Repository Layout

