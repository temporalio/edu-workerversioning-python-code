import asyncio
import logging

from activities import LoanProcessingActivities
from shared import TASK_QUEUE_NAME
from temporalio.client import Client
from workflow import LoanProcessingWorkflow
from temporalio.common import WorkerDeploymentVersion, VersioningBehavior
from temporalio.worker import Worker, WorkerDeploymentConfig

async def main():
    logging.basicConfig(level=logging.INFO)

    client = await Client.connect("localhost:7233", namespace="default")

    activities = LoanProcessingActivities()

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[LoanProcessingWorkflow],
        activities=[activities.charge_customer, activities.send_thank_you_to_customer],
        deployment_config=WorkerDeploymentConfig(
            version=WorkerDeploymentVersion(
                deployment_name="worker_versioning_demo",
                # TODO Part A: Set a Build ID
                build_id=""),
            use_worker_versioning=True,
            # TODO Part A: Toggle versioning behavior to PINNED
            default_versioning_behavior=VersioningBehavior.UNSPECIFIED
        ),
    )
    logging.info("Starting the worker....")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
