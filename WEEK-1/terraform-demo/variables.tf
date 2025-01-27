variable "bq_dataset_name" {
    description = "value for the dataset name"
    default     = "terra_dataset"
}

variable "gcs_storage_class" {
    description = "storage class for GCS bucket"
    default     = "STANDARD"
}

variable "gcs_bucket_name" {
    description = "bucket name for GCS bucket"
    default     = "terraform-basics-449110-terra-bucket"
}

variable "project_location" {
    description = "location of the project"
    default     = "US"
}

variable "project_region" {
    description = "region for GCS bucket"
    default     = "us-central1"
}

variable "project_name" {
    description = "name of the project"
    default     = "terraform-basics-449110"
}

variable "project_credentials" {
    description = "path to the credentials file"
    default     = "./keys/my-creds.json"
}