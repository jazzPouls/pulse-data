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

module "scheduler-queue" {
  source = "../serial-task-queue"

  queue_name                = "${local.direct_ingest_formatted_str}-scheduler"
  region                    = var.region
  max_dispatches_per_second = 100
}

module "process-job-queue" {
  source = "../serial-task-queue"

  queue_name                = "${local.direct_ingest_formatted_str}-process-job-queue"
  region                    = var.region
  max_dispatches_per_second = 100
}

module "bq-import-export-queue" {
  source = "../serial-task-queue"

  queue_name                = "${local.direct_ingest_formatted_str}-bq-import-export"
  region                    = var.region
  max_dispatches_per_second = 100
}
