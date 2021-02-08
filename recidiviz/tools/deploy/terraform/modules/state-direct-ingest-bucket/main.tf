# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2021 Recidiviz, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================

# The state code associated with the buckets and service accounts (ex: "TN").
variable "state_code" {
  type = string
}

# the project id associated with the buckets and service accounts (ex: "recidiviz-123").
variable "project_id" {
  type = string
}

# The preferred region for the instance (ex: "us-east4").
variable "region" {
  type = string
}

# Whether or not the project is in production.
variable "is_production" {
  type = bool
}

locals {
  direct_ingest_formatted_str = "direct-ingest-state-us-%s"
}

resource "google_storage_bucket" "direct-ingest-bucket" {
  name     = "${var.project_id}-${format(local.direct_ingest_formatted_str, lower(var.state_code))}"
  location = var.region
}

resource "google_storage_bucket" "prod-only-testing-direct-ingest-bucket" {
  count    = var.is_production ? 1 : 0
  name     = "recidiviz-123-${format(local.direct_ingest_formatted_str, lower(var.state_code))}-testing"
  location = var.region
}

resource "google_service_account" "service-account" {
  account_id   = format(local.direct_ingest_formatted_str, lower(var.state_code))
  display_name = "A service account for ${var.state_code} Direct Ingest."
}

resource "google_storage_bucket_iam_member" "direct-ingest-buckets-member" {
  bucket = google_storage_bucket.direct-ingest-bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.service-account.email}"
}

resource "google_storage_bucket_iam_member" "prod-only-testing-direct-ingest-buckets-member" {
  count  = var.is_production ? 1 : 0
  bucket = google_storage_bucket.prod-only-testing-direct-ingest-bucket[count.index].name
  role = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.service-account.email}"
}