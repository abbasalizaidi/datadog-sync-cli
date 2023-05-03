# Unless explicitly stated otherwise all files in this repository are licensed
# under the 3-clause BSD style license (see LICENSE).
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019 Datadog, Inc.
from __future__ import annotations
import configobj
from sys import exit

from click import Choice, Option, option, File

from datadog_sync import constants
from typing import TYPE_CHECKING, Any, Callable, Dict, List

if TYPE_CHECKING:
    from click.core import Context


class CustomOptionClass(Option):
    def handle_parse_result(self, ctx: Context, opts: Dict[Any, Any], args: List[Any]) -> Any:
        try:
            return super(Option, self).handle_parse_result(ctx, opts, args)
        except Exception as e:
            if self.is_flag:
                print(f"Invalid value for Option '{self.human_readable_name}'. Valid values [True, False]")
            else:
                print(f"Invalid value for Option '{self.human_readable_name}': {str(e)}")
            exit(1)


_source_auth_options = [
    option(
        "--source-api-key",
        envvar=constants.DD_SOURCE_API_KEY,
        required=False,
        help="Datadog source organization API key.",
        cls=CustomOptionClass,
    ),
    option(
        "--source-app-key",
        envvar=constants.DD_SOURCE_APP_KEY,
        required=False,
        help="Datadog source organization APP key.",
        cls=CustomOptionClass,
    ),
    option(
        "--source-api-url",
        envvar=constants.DD_SOURCE_API_URL,
        required=False,
        default=constants.DEFAULT_API_URL,
        show_default=True,
        help="Datadog source organization API url.",
        cls=CustomOptionClass,
    ),
]

_destination_auth_options = [
    option(
        "--destination-api-key",
        envvar=constants.DD_DESTINATION_API_KEY,
        required=False,
        help="Datadog destination organization API key.",
        cls=CustomOptionClass,
    ),
    option(
        "--destination-app-key",
        envvar=constants.DD_DESTINATION_APP_KEY,
        required=False,
        help="Datadog destination organization APP key.",
        cls=CustomOptionClass,
    ),
    option(
        "--destination-api-url",
        envvar=constants.DD_DESTINATION_API_URL,
        required=False,
        default=constants.DEFAULT_API_URL,
        show_default=True,
        help="Datadog destination organization API url.",
        cls=CustomOptionClass,
    ),
]


def click_config_file_provider(ctx: Context, opts: CustomOptionClass, value: None) -> None:
    config = configobj.ConfigObj(value, unrepr=True)
    ctx.default_map = ctx.default_map or {}
    ctx.default_map.update(config)


_common_options = [
    option(
        "--http-client-retry-timeout",
        envvar=constants.DD_HTTP_CLIENT_RETRY_TIMEOUT,
        required=False,
        type=int,
        default=60,
        show_default=True,
        help="The HTTP request retry timeout period. Defaults to 60s",
        cls=CustomOptionClass,
    ),
    option(
        "--resources",
        envvar=constants.DD_RESOURCES,
        required=False,
        help="Optional comma separated list of resource to import. All supported resources are imported by default.",
        cls=CustomOptionClass,
    ),
    option(
        "--verbose",
        "-v",
        required=False,
        is_flag=True,
        help="Enable verbose logging.",
        cls=CustomOptionClass,
    ),
    option(
        "--max-workers",
        envvar=constants.MAX_WORKERS,
        required=False,
        type=int,
        help="Max number of workers when running operations in multi-threads.",
        cls=CustomOptionClass,
    ),
    option(
        "--filter-operator",
        envvar=constants.DD_FILTER_OPERATOR,
        required=False,
        default="OR",
        help="Filter operator when multiple filters are passed. Supports `AND` or `OR`.",
        cls=CustomOptionClass,
    ),
    option(
        "--filter",
        required=False,
        help="Filter resources.",
        multiple=True,
        envvar=constants.DD_FILTER,
        cls=CustomOptionClass,
    ),
    option(
        "--config",
        help="Read configuration from FILE.",
        type=File("rb"),
        callback=click_config_file_provider,
        cls=CustomOptionClass,
    ),
    option(
        "--validate",
        type=bool,
        envvar=constants.DD_VALIDATE,
        default=True,
        show_default=True,
        help="Enables validation of the provided API during client initialization. On import, only source api key is validated. On sync/diffs, only destination api key is validated.",
        cls=CustomOptionClass,
    ),
]


_non_import_common_options = [
    option(
        "--skip-failed-resource-connections",
        type=bool,
        default=True,
        show_default=True,
        help="Skip resource if resource connection fails.",
        cls=CustomOptionClass,
    ),
    option(
        "--cleanup",
        default="False",
        show_default=True,
        type=Choice(
            ["True", "False", "Force"],
            case_sensitive=False,
        ),
        help="Cleanup resources from destination org.",
        envvar=constants.DD_CLEANUP,
        cls=CustomOptionClass,
    ),
]


def source_auth_options(func: Callable) -> Callable:
    return _build_options_helper(func, _source_auth_options)


def destination_auth_options(func: Callable) -> Callable:
    return _build_options_helper(func, _destination_auth_options)


def common_options(func: Callable) -> Callable:
    return _build_options_helper(func, _common_options)


def non_import_common_options(func: Callable) -> Callable:
    return _build_options_helper(func, _non_import_common_options)


def _build_options_helper(func: Callable, options: List[Callable]) -> Callable:
    for _option in options:
        func = _option(func)
    return func
