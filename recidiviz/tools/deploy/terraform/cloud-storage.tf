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


locals {
  state_alpha_codes = ["US_ID", "US_MO", "US_ND", "US_PA", "US_TN", "US_MI"]
}

module "state_direct_ingest_buckets_and_accounts" {
  for_each         = toset(local.state_alpha_codes)
  source           = "./modules/state-direct-ingest-bucket"
  state_code       = each.key
  region           = contains(["US_ID", "US_MO", "US_ND", "US_PA"], each.key) ? "us-east1" : var.region
  is_production    = local.is_production
  project_id       = var.project_id
  state_admin_role = google_project_iam_custom_role.state-admin-role.name
}

module "justice-counts-data-bucket" {
  source      = "./modules/cloud-storage-bucket"
  project_id  = var.project_id
  name_suffix = "justice-counts-data"
}
