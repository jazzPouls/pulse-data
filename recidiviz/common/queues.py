# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2019 Recidiviz, Inc.
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

"""Cloud Tasks queue helper functions."""

import datetime
import json
import uuid
from typing import List

from google.cloud import tasks_v2beta3
from google.cloud.tasks_v2beta3.types import Task

from recidiviz.utils import environment, metadata

_client = None
def client():
    global _client
    if not _client:
        _client = tasks_v2beta3.CloudTasksClient()
    return _client

@environment.test_only
def clear_client():
    global _client
    _client = None


def format_queue_path(queue_name):
    """Formats a queue name into its full Cloud Tasks queue path.

    Args:
        queue_name: `str` queue name.
    Returns:
        A Cloud Tasks queue path string.
    """
    full_queue_path = client().queue_path(
        metadata.project_id(),
        metadata.region(),
        queue_name)

    return full_queue_path


def format_task_path(queue_name: str, task_name: str):
    """Creates a task path out of the necessary parts.

    Task path is of the form:
        '/projects/{project}/locations/{location}'
        '/queues/{queue}/tasks/{task_name}'
    """
    return client().task_path(
        metadata.project_id(),
        metadata.region(),
        queue_name,
        task_name)


def format_scrape_task_path(queue_name: str, region_code: str, task_id: str):
    """Creates a scrape task path out of the necessary parts.

    Task path is of the form:
        '/projects/{project}/locations/{location}'
        '/queues/{queue}/tasks/{region_code}-{task_id}'
    """
    return format_task_path(queue_name, '{}-{}'.format(region_code, task_id))


def purge_scrape_tasks(*, region_code: str, queue_name: str):
    """Purge scrape tasks for a given region from its queue.

    Args:
        region_code: `str` region code.
        queue_name: `str` queue name.
    """
    for task in list_scrape_tasks(
            region_code=region_code, queue_name=queue_name):
        client().delete_task(task.name)


def list_scrape_tasks(*, region_code: str, queue_name: str) -> List[Task]:
    """List scrape tasks for the given region and queue"""
    region_task_prefix = format_scrape_task_path(queue_name, region_code, '')
    return [task for task in client().list_tasks(format_queue_path(queue_name))
            if task.name.startswith(region_task_prefix)]


def create_scrape_task(*, region_code, queue_name, url, body):
    """Create a scrape task in a queue.

    Args:
        region_code: `str` region code.
        queue_name: `str` queue name.
        url: `str` App Engine worker url.
        body: `dict` task body to be passed to worker.
    """
    task = Task(
        name=format_scrape_task_path(queue_name, region_code, uuid.uuid4()),
        app_engine_http_request={
            'relative_uri': url,
            'body': json.dumps(body).encode()
        }
    )

    client().create_task(format_queue_path(queue_name), task)

SCRAPER_PHASE_QUEUE = 'scraper-phase'

def enqueue_scraper_phase(*, region_code, url):
    """Add a task to trigger the next phase of a scrape.

    This triggers the phase at the given url for an individual region, passing
    the `region_code` as a url parameter. For example, this can trigger stopping
    a scraper or inferring release for a particular region.
    """
    task = Task(
        app_engine_http_request={
            'http_method': 'GET',
            'relative_uri': '{url}?region={region_code}'.format(
                url=url, region_code=region_code
            ),
        }
    )
    client().create_task(format_queue_path(SCRAPER_PHASE_QUEUE), task)


BIGQUERY_QUEUE = 'bigquery'

def create_bq_task(table_name: str, url: str):
    """Create a BigQuery table export path.

    Args:
        table_name: Cloud SQL table to export to BQ. Must be defined in
            recidiviz.calculator.bq.export_config.TABLES_TO_EXPORT.
        url: App Engine worker URL.
    """
    body = {'table_name': table_name}
    task_id = '{}-{}-{}'.format(
        table_name, str(datetime.date.today()), uuid.uuid4())
    task_name = format_task_path(BIGQUERY_QUEUE, task_id)
    task = Task(
        name=task_name,
        app_engine_http_request={
            'relative_uri': url,
            'body': json.dumps(body).encode()
        }
    )
    client().create_task(format_queue_path(BIGQUERY_QUEUE), task)
