# Master thesis

In collaboration with M13H data science team and Labelium group, this thesis aims to develop a new tool.
This tool is transversal between all entities of Labelium group.

## Aim

Improve Amazon product referencing based only on the semantic part of the product information sheet. This improvement
provides advices to enrich the semantic and to understand product competitors (market study).

## Technologies

The SEO (Search Engine Organic) uses Word2Vec. Word2Vec is trained on thousands of Amazon product pages scrapped using 
Selenium. Finally, data preprocessing is done using libraries such as NLTK and libraries from stanford university 
(stematization).

This project is hosted on GCP and uses several services : GCS, Cloud Run, Cloud Function, Pub/Sub, BigQuery, Cloud 
Scheduler, Compute Engine.. A study takes around 30 minutes to process.

## Support 
This folder contains the thesis written by Olivier Randavel.
You will find the dashboard used to make the analyse and the thesis that describes the project.
This work has been grade 18/20
