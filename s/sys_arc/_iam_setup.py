import pulumi
import pulumi_gcp as gcp
# from pulumi_gcp import pubsub

def setup_iam():
    # Create a service account
    service_account = gcp.serviceaccount.Account(
        'service-account',
        account_id='nimbusdb-service-account',
        display_name='NimbusDB Service Account'
    )

    # Assign roles to the service account
    roles = [
        'roles/storage.admin',           # Cloud Storage Admin
        'roles/bigquery.admin',          # BigQuery Admin
        'roles/pubsub.admin',            # Pub/Sub Admin
        'roles/dataflow.admin'           # Dataflow Admin
    ]

    for role in roles:
        gcp.projects.IAMMember(
            f'{role.replace("/", "_")}-binding',
            project=pulumi.Config('gcp').require('project'),
            role=role,
            member=service_account.email.apply(lambda email: f'serviceAccount:{email}')
        )

    # Export the service account email
    pulumi.export('service_account_email', service_account.email)

def pub_sub():
    project_id = "smart-charter-422809-k0"
    topic_name = "player-updates-1de6ac7"

    # Create a new subscription
    subscription = gcp.pubsub.Subscription(
        'player-updates-sub',
        project=project_id,
        topic=f'projects/{project_id}/topics/{topic_name}',
        # Optional arguments (refer to Pulumi documentation for details)
        ack_deadline_seconds=60, # Message acknowledgement deadline
        # retain_acked_messages=True, # Retain acknowledged messages
    )

    # This will create the subscription in your project
    pulumi.export('subscription_name', subscription.name)

