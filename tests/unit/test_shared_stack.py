import aws_cdk as core
import aws_cdk.assertions as assertions

from shared.shared import SharedResources

# example tests. To run these tests, uncomment this file along with the example
# resource in ecs_fargate_shared_resources/ecs_fargate_shared_resources_stack.py
def test_subnets_created():
    app = core.App()
    stack = SharedResources(app, "shared-resources")
    template = assertions.Template.from_stack(stack)

    # template.has_resource_properties("AWS::SQS::Queue", {
    #     "VisibilityTimeout": 300
    # })
    template.resource_count_is("AWS::EC2::Subnet", 4)
