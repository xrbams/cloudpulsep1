"""A Google Cloud Python Pulumi program"""
import _iam_setup
import _storage

# Run the setup functions from the different modules
_iam_setup.setup_iam()
_storage.setup_storage()


