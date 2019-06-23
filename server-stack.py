'''Module: Create a CloudFormation Stack'''
import troposphere.ec2 as ec2
from troposphere import Base64, FindInMap, GetAtt, Join
from troposphere import Parameter, Output, Ref, Template
from troposphere.cloudformation import Init, InitConfig, InitFiles, InitFile, Metadata
from troposphere.policies import CreationPolicy, ResourceSignal

def main():
    '''Function: Generates the Cloudformation template'''
    template = Template()
    template.set_description("Server Stack")

    keyname_param = template.add_parameter(
        Parameter(
            'KeyName',
            Description='An existing EC2 KeyPair.',
            ConstraintDescription='An existing EC2 KeyPair.',
            Type='AWS::EC2::KeyPair::KeyName',
        )
    )

    template.add_mapping('RegionMap', {'eu-north-1': {'ami': 'ami-a536bedb'}, 'ap-south-1': {'ami': 'ami-00b2a5e29f669c903'}, 'eu-west-3': {'ami': 'ami-0d8581d2794d7df68'}, 'eu-west-2': {'ami': 'ami-02369579484abae2e'}, 'eu-west-1': {'ami': 'ami-0c17a2bccea3e36f9'}, 'ap-northeast-2': {'ami': 'ami-05daa9d0230f30d79'}, 'ap-northeast-1': {'ami': 'ami-03a90fe15b63befea'}, 'sa-east-1': {'ami': 'ami-0c04bf4cfbf3e9dbe'}, 'ca-central-1': {'ami': 'ami-013d2a414e834a144'}, 'ap-southeast-1': {'ami': 'ami-07ed1f021e2eea7cb'}, 'ap-southeast-2': {'ami': 'ami-068e6346d66ed62c8'}, 'eu-central-1': {'ami': 'ami-00aa61be0e9a8f948'}, 'us-east-1': {'ami': 'ami-0dd925351e231e8c7'}, 'us-east-2': {'ami': 'ami-06cb7cbcc0e8e90e8'}, 'us-west-1': {'ami': 'ami-0d8e4e7b60cd5f225'}, 'us-west-2': {'ami': 'ami-06ad92f74f2c20787'}})

    ec2_security_group = template.add_resource(
        ec2.SecurityGroup(
            'EC2SecurityGroup',
            Tags=[{'Key':'Name', 'Value':Ref('AWS::StackName')},],
            GroupDescription='EC2 Security Group',
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    IpProtocol='tcp',
                    FromPort='22',
                    ToPort='22',
                    CidrIp='0.0.0.0/0',
                    Description='SSH'),
                ec2.SecurityGroupRule(
                    IpProtocol='tcp',
                    FromPort='80',
                    ToPort='80',
                    CidrIp='0.0.0.0/0',
                    Description='HTTP'),
                ec2.SecurityGroupRule(
                    IpProtocol='tcp',
                    FromPort='443',
                    ToPort='443',
                    CidrIp='0.0.0.0/0',
                    Description='HTTPS'),
            ],
        )
    )

    ec2_instance = template.add_resource(
        ec2.Instance(
            'Instance',
            Metadata=Metadata(
                Init({
                    "config": InitConfig(
                        files=InitFiles({
                            "/tmp/instance.txt": InitFile(
                                content=Ref('AWS::StackName'),
                                mode="000644",
                                owner="root",
                                group="root"
                            )
                        }),
                    )
                }),
            ),
            CreationPolicy=CreationPolicy(
                ResourceSignal=ResourceSignal(Timeout='PT15M')
            ),
            Tags=[{'Key':'Name', 'Value':Ref('AWS::StackName')},],
            ImageId=FindInMap('RegionMap', Ref('AWS::Region'), 'ami'),
            InstanceType='t3.micro',
            KeyName=Ref(keyname_param),
            SecurityGroups=[Ref(ec2_security_group)],
            UserData=Base64(
                Join(
                    '',
                    [
                        '#!/bin/bash -x\n',
                        'exec > /tmp/user-data.log 2>&1\n',
                        'unset UCF_FORCE_CONFFOLD\n',
                        'export UCF_FORCE_CONFFNEW=YES\n',
                        'ucf --purge /boot/grub/menu.lst\n',
                        'export DEBIAN_FRONTEND=noninteractive\n',
                        'apt-get update\n',
                        'apt-get -o Dpkg::Options::="--force-confnew" --force-yes -fuy upgrade\n',
           		'apt-get install -y python-pip\n',
			'pip install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz\n',
                        '# Signal Cloudformation when set up is complete\n',
                        '/usr/local/bin/cfn-signal -e $? --resource=Instance --region=', Ref('AWS::Region'), ' --stack=', Ref('AWS::StackName'), '\n',
                    ]
                )
            )
        )
    )

    template.add_resource(
        ec2.EIP(
            'ElasticIP',
            InstanceId=Ref(ec2_instance),
            Domain='vpc'
        )
    )

    template.add_output([
        Output(
            'InstanceDnsName',
            Description='PublicDnsName',
            Value=GetAtt(ec2_instance, 'PublicDnsName'),
        ),
    ])

    print(template.to_yaml())

if __name__ == '__main__':
    main()
