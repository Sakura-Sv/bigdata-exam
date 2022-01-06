from diagrams import Diagram, Cluster
from diagrams.alibabacloud.compute import ElasticSearch
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.network import ELB
from diagrams.elastic.elasticsearch import Kibana
from diagrams.gcp.network import DNS
from diagrams.generic.os import Ubuntu
from diagrams.k8s.compute import Pod
from diagrams.onprem.container import Docker
from diagrams.onprem.database import MongoDB, MySQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Github, Git
from diagrams.programming.framework import Spring, Flask
from diagrams.programming.language import Go, Python

with Diagram(name="Movie Recommend System", show=True):
    with Cluster("Backend"):
        dns = DNS("DNS")
        ingress = Nginx("Kubernates Ingress Gateway")
        dns >> ingress >> dns

        with Cluster("Python Application"):
            logs = Python("Logger")
            spider = Python("Spider")
            with Cluster("Flask Application"):
                auth = Flask("Flask Security")
                mvc = Flask("Flask router")
                services = [
                    Lambda("Movie Service"),
                    Lambda("User Service"),
                    Lambda("Search Service")
                ]
                dao = [
                    Python("PyMySQL")
                ]
                auth >> mvc >> auth
                mvc >> services
                mvc >> logs
                services >> dao[0]
        ingress >> auth >> ingress

        with Cluster("Data Persistence Layer"):
            mongo = MySQL("MySQL")
        dao >> mongo >> dao
        spider >> mongo >> spider

        with Cluster("Recommend Engine"):
            engine = EC2("Movie Recommend Engine")
        services[0] >> engine >> services[0]
        engine >> mongo >> engine

    with Cluster("DevOps"):
        git = Git("Git")
        github = Github("Github")
        action = Github("Github Actions")
        ubuntu = Ubuntu("Server")
        git >> github >> git
        with Cluster("Containerized"):
            docker = [
                Docker("MySQL"),
                Docker("App"),
            ]
            compose = Pod("Kubernates Pod")
            docker >> compose
    compose >> git
    github >> action >> ubuntu
    git >> action
