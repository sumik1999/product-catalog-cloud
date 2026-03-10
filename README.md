Product Catalogue Application on Public Cloud
Student Name: Kiran Kumari
Course: Cloud Computing
Assignment: Public Cloud Application Deployment   Roll No:- 2025EET2480
1. Introduction
This project implements a Product Catalogue web application deployed on a public cloud environment. The system allows users to add and view products along with their associated images
2. Features Added and Their Usefulness
2.1 Add New Products and View Products. Additionally can even delete products
The application allows users to add new products to the catalogue by entering:
Product name
Product description
Product price
Product image
Usefulness
Enables users to dynamically add products
Demonstrates write operations to a cloud database
Shows integration with cloud storage for media
Allows easy browsing of the product catalogue
Demonstrates read operations from the database
2.2 Services used:-
Google Cloud SQL (database) : For database purpose
Google Cloud Storage (storage service) : For storing purpose
2.3 Handling of Bad-Inputs
The bad inputs cannot be sent into a product entry, they have been checked at the api endpoints
3. Architecture Decisions
Several design decisions were made to ensure scalability, modularity, and reliability.
3.1 Separation of Application and Storage Layers
The application has been written in flask (python) which is a lightweight web server that handles:
user interface : CSS added along with flask for frontend rendering
business logic : api endpoints routes built for add and list 
Storage responsibilities are separated into:
Cloud SQL database (Postgres) → structured product data, uses env configuration files that links externally to the service
Google Cloud Storage → product images, uses env files for linking. This logic has been separated into a gcs_utils.py file to keep it apart from api endpoints and make it re-usable.
Reason
Separating these layers improves scalability and performance while following best practices in cloud architecture.

3.2 Use of PostgreSQL Database
PostgreSQL was chosen as the database system for storing product metadata. This uses Google Cloud SQL services.
Stored data includes:
product id
product name
description
price
image URL
Reason
Reliable relational database
Structured schema support
Suitable for transactional data

3.3 Using Google Cloud Storage for Images
Images are stored in Google Cloud Storage buckets instead of the database.
Reason
Databases are inefficient for storing large binary objects
GCS offers scalable and reliable object storage
Easy public access via URLs

3.4 Hosting with Google Compute Engine
The Flask application is deployed on a Compute Engine Virtual Machine. Docker has been used further to containerize the web app.
Reason
Provides full control over environment
Easy deployment for Python web applications
Public IP enables external access
4. Architecture Diagram
Below is the architecture of the deployed system.
                Users (Web Browser)
                        ↓
                 HTTP Request
                        ↓
             Google Compute Engine VM
              (Flask Web Application running using docker)
                        ↓
         ----------------------------------------------
          ↓                                                    ↓
   PostgreSQL Database           Google Cloud Storage
   (Product Information)                 (Product Images)
5. Public URL
The deployed application can be accessed using the following public URL:
http://35.232.184.215:5000
The application code can be accessed using the following public URL:









