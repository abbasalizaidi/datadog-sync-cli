# Unless explicitly stated otherwise all files in this repository are licensed
# under the 3-clause BSD style license (see LICENSE).
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019 Datadog, Inc.

import pytest

from tests.integration.helpers import BaseResourcesTestClass
from datadog_sync.models import Users


class TestUsersResources(BaseResourcesTestClass):
    resource_type = Users.resource_type
    field_to_update = "name"

    # FIXME: reintroduce after nested attribute update support
    @pytest.mark.skip(reason="nested attribute update is not currently supported in tests")
    def test_resource_update_sync(self):
        pass
