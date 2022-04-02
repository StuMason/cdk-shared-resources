import aws_cdk as core
import aws_cdk.assertions as assertions

from ecs_fargate_shared_resources.ecs_fargate_shared_resources_stack import EcsFargateSharedResourcesStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ecs_fargate_shared_resources/ecs_fargate_shared_resources_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EcsFargateSharedResourcesStack(app, "ecs-fargate-shared-resources")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
