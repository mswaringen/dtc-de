terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = "./keys/my-creds.json"
  project     = "terraform-basics-449110"
  region      = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-basics-449110-terra-bucket"
  location      = "US"
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