from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_route53 as route53,
    aws_route53_targets as targets
)
from constructs import Construct

class SharedResources(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.build_shared_services()
        self.build_example_service()

    def build_shared_services(self) -> None:
        self.vpc = ec2.Vpc(self, "Vpc", max_azs=2, 
            cidr="10.0.0.0/21"
        )
        
        self.target_group = elbv2.ApplicationTargetGroup(self, "TargetGroup",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            vpc=self.vpc,
            target_type=elbv2.TargetType.IP
        )

        self.lb = elbv2.ApplicationLoadBalancer(self, "LB",
            vpc=self.vpc,
            internet_facing=True
        )

        self.listener = self.lb.add_listener("Listener",
            port=80,
            open=True,
            default_target_groups=[self.target_group]
        )

        self.cluster = ecs.Cluster(self, "EcsCluster", vpc=self.vpc)

    def build_example_service(self) -> None:
        task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
            cpu=256,
            memory_limit_mib=512
        )

        task_definition.add_container("WebContainer",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            port_mappings=[ecs.PortMapping(container_port=80)]
        )

        service = ecs.FargateService(self, "Service",
            cluster=self.cluster,
            task_definition=task_definition,
            desired_count=1,
            assign_public_ip=False,
        )

        target_group = self.listener.add_targets("app_target",
            port=80,
            targets=[service]
        )

        elbv2.ApplicationListenerRule(self, "my_app_listener_rule",
            listener=self.listener,
            priority=123,
            conditions=[elbv2.ListenerCondition.path_patterns(["/test"])],
            target_groups=[target_group],
        )

        zone = route53.HostedZone.from_lookup(self, "zone",
            domain_name="recode.zone"
        )

        route53.ARecord(self, "app_record_set",
            target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(self.lb)),
            zone=zone,
            record_name="test-cdk.recode.zone"
        )