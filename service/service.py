from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_route53 as route53,
    aws_elasticloadbalancingv2 as elbv2,
    aws_route53_targets as targets
)
from cdk_watchful import Watchful
from constructs import Construct

class Service(Stack):

    def __init__(self, scope: Construct, construct_id: str, shared_resources, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        app_name = "test-cdk"
        domain = "stuartmason.co.uk"

        task_definition = ecs.FargateTaskDefinition(self, f"{app_name}_task_def",
            cpu=256,
            memory_limit_mib=512
        )

        task_definition.add_container(f"{app_name}_web_container",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            port_mappings=[ecs.PortMapping(container_port=80)]
        )

        service = ecs.FargateService(self, f"{app_name}_service",
            cluster=shared_resources.cluster,
            task_definition=task_definition,
            desired_count=1,
            assign_public_ip=False,
        )

        target_group = shared_resources.listener.add_targets(f"{app_name}_app_target",
            port=80,
            targets=[service]
        )

        elbv2.ApplicationListenerRule(self, f"{app_name}_listener_rule",
            listener=shared_resources.listener,
            priority=123,
            conditions=[elbv2.ListenerCondition.host_headers([f"{app_name}.{domain}"])],
            target_groups=[target_group],
        )

        zone = route53.HostedZone.from_lookup(self, "zone",
            domain_name=domain
        )

        route53.ARecord(self, f"{app_name}_app_record_set",
            target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(shared_resources.lb)),
            zone=zone,
            record_name=f"{app_name}.{domain}"
        )

        wf = Watchful(self, "watchful",
            alarm_email="stu@stuartmason.co.uk"
        )

        wf.watch_scope(self)