"""A Google Cloud Python Pulumi program"""
import _iam_setup
import _storage
import _stream_pipe


# Run the setup functions from the different modules
_iam_setup.setup_iam()
_iam_setup.pub_sub()
_storage.setup_storage()
_storage.data_in()
# _stream_pipe.run()



