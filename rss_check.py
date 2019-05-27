import feedparser

aws_rss = {'EC2': 'https://status.aws.amazon.com/rss/ec2-us-east-1.rss',
           'API Gateway': 'https://status.aws.amazon.com/rss/apigateway-us-east-1.rss',
           'Cloudwatch': 'https://status.aws.amazon.com/rss/cloudwatch-us-east-1.rss',
           'Athena': 'https://status.aws.amazon.com/rss/athena-us-east-1.rss',
           'ECS': 'https://status.aws.amazon.com/rss/ecs-us-east-1.rss',
           'ELB': 'https://status.aws.amazon.com/rss/elb-us-east-1.rss',
           'Elasticache': 'https://status.aws.amazon.com/rss/elasticache-us-east-1.rss',
           'Guard Duty': 'https://status.aws.amazon.com/rss/guardduty-us-east-1.rss',
           'Route 53 dns': 'https://status.aws.amazon.com/rss/route53-us-east-1.rss',
           'Route 53 resolver': 'https://status.aws.amazon.com/rss/route53resolver-us-east-1.rss',
           'SES': 'https://status.aws.amazon.com/rss/ses-us-east-1.rss',
           'SNS': 'https://status.aws.amazon.com/rss/sns-us-east-1.rss',
           'SQS': 'https://status.aws.amazon.com/rss/sqs-us-east-1.rss',
           'S3': 'https://status.aws.amazon.com/rss/s3-us-standard.rss',
           'Autoscaling': 'https://status.aws.amazon.com/rss/autoscaling-us-east-1.rss',
           'Internet connection': 'https://status.aws.amazon.com/rss/internetconnectivity-us-east-1.rss',
           'Lambda': 'https://status.aws.amazon.com/rss/lambda-us-east-1.rss',
           'Secrets manager': 'https://status.aws.amazon.com/rss/secretsmanager-us-east-1.rss',
           }

for k, v in aws_rss.items():
    try:
        f = feedparser.parse(v)
        if '[RESOLVED]' not in f['entries'][0]['title']:
            print(f'{k} is bad')
        else:
            print(f'{k} is good')
    except IndexError:
        print(f'looks like {k} was never dead or ...')
    except Exception as e:
        print(f'{e}: {k} is noob')

