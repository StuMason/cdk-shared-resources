#!/usr/bin/env python3
import os

import aws_cdk as cdk

from shared.shared import SharedResources
# from service.service import Service

env_EU = cdk.Environment(account="645571371616", region="eu-west-1")

app = cdk.App()
shared = SharedResources(app, "SharedResources", env=env_EU)
# service = Service(app, "Service", shared_resources=shared, env=env_EU)

app.synth()
