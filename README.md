# TONI-Data-Processor-Web-App
This web application allows users to easily process cemetery data for the TONI indexing project.

It provides two main features:

PDF Extraction:
Upload a cemetery transcription PDF and extract structured data (Surname, Firstname, Record Type, Date, Location) into an Excel file. The app uses custom logic to identify surnames, first names, and burial dates, and allows the user to specify the location for the output.

Excel Deduplication:
Upload an Excel file and automatically remove exact duplicate rows, returning a cleaned Excel file for download.

Features
User-friendly web interface for file uploads
Supports both PDF and Excel file processing
Custom location input for PDF extraction
Automatic download of processed results in Excel format

Built with Flask and pandas, deployable on Vercel

How to Use
Select the file type (PDF or Excel).
For PDFs, enter the cemetery location.
Upload your file.
Download the processed Excel file.
