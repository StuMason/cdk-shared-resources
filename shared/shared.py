from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_route53 as route53,
    aws_route53_targets as targets
)
from constructs import Construct
from cdk_watchful import Watchful

class SharedResources(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.build_shared_services()

    def build_shared_services(self) -> None:
        self.vpc = ec2.Vpc(self, "Vpc", max_azs=2, 
            cidr="10.0.0.0/21"
        )
        
        self.target_group = elbv2.ApplicationTargetGroup(self, "default_target_group",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            vpc=self.vpc,
            target_type=elbv2.TargetType.IP
        )

        self.lb = elbv2.ApplicationLoadBalancer(self, "load_balancer",
            vpc=self.vpc,
            internet_facing=True
        )

        self.listener = self.lb.add_listener("listener",
            port=80,
            open=True,
            default_target_groups=[self.target_group]
        )

        self.cluster = ecs.Cluster(self, "ecs_cluster", vpc=self.vpc)

        wf = Watchful(self, "watchful",
            alarm_email="stu@stuartmason.co.uk"
        )

        wf.watch_scope(self)