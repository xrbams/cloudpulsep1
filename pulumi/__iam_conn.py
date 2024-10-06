import pulumi
from pulumi_gcp import serviceaccount, projects

def generate_IAM(): 
    service_account = serviceaccount.Account(
        "xrbams-service-account",
        account_id="my-service-account",
        display_name="My GCS Access Service Account"
    )

    # 3. Assign IAM roles to the Service Account (Grant Storage Object Viewer role)
    iam_binding = projects.IAMMember(
        "xrbams-account-storage-access",
        project=pulumi.Config().require("gcp:project"),
        role="roles/storage.objectViewer",
        member=service_account.email.apply(lambda email: f"serviceAccount:{email}")
    )

    # 4. Create a Key for the Service Account
    service_account_key = serviceaccount.Key(
        "xrbams-account-key",
        service_account_id=service_account.name
    )

    # 5. Save the service account key to a local file
    key_file_path = "service_account_key.json"
    pulumi.export("keyfile_path", key_file_path)

    # Save the keyfile to disk
    key_content = service_account_key.private_key.apply(lambda key: key)
    pulumi.Output.all(key_content).apply(
        lambda args: open(key_file_path, "w").write(args[0])
    )

    # 6. Export important information
    pulumi.export("service_account_email", service_account.email)
    pulumi.export("key_file_path", key_file_path)