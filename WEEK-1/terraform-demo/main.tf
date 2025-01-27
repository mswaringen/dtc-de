terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = file(var.project_credentials)
  project     = var.project_name
  region      = var.project_region
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.project_location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo-dataset" {
  dataset_id                  = var.bq_dataset_name
  location                    = var.project_location
}