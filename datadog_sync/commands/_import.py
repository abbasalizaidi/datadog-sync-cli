import os
import time

from click import pass_context, command
from datadog_sync.constants import SOURCE_RESOURCES_DIR


@command("import", short_help="Import Datadog resources.")
@pass_context
def _import(ctx):
    """Import Datadog resources."""
    cfg = ctx.obj.get("config")
    start = time.time()

    os.makedirs(SOURCE_RESOURCES_DIR, exist_ok=True)

    for resource_type, resource in cfg.resources.items():
        if cfg.missing_deps and resource_type in cfg.missing_deps:
            continue
        cfg.logger.info("importing %s", resource_type)
        resource.import_resources()
        resource.write_resources_file("source", resource.source_resources)
        cfg.logger.info("finished importing %s", resource_type)


    cfg.logger.info(f"finished importing resources: {time.time() - start}s")

    if cfg.logger.exception_logged:
        exit(1)
