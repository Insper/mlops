# AWS CLI Configuration

The **AWS CLI** (*Command Line Interface*) is a tool that lets you manage AWS services from the command line. With it, you can run commands to create, modify, and delete AWS resources, making task automation and script integration easier.

### Installation

[**Click Here**](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install AWS CLI.

## Environment Setup

To follow the hands-on examples in this class, you need to configure your development environment. Here are the recommended steps:

1. **Activate Your AWS Account**: If you have not activated your account yet, check the notice sent by the instructors for more details.

2. **Install AWS CLI**: The AWS Command Line Interface (CLI) is one of the tools we will use to interact with AWS services.

3. **Configure Credentials**: We will configure access to your **AWS** account through **SSO** (a different setup from the first class).

!!! warning "Attention"
    Run the following command:

    !!! danger "Important"
        Set the region to `us-east-1`.
        We will centralize resources in a single region to keep better organization and control over what we create during the course.

    !!! warning "Browser login required"
        During this step, you will be prompted to sign in to your **AWS** account through your browser.

        Follow the on-screen instructions to complete the authentication process.

        If prompted, select the course account.

    !!! warning "Settings"
        - `SSO session name (Recommended):` you can use `mlops`
        - `SSO start URL:` use the login URL provided in the invitation email
        - `SSO region [None]`: use `us-east-1`
        - `SSO registration scopes [sso:account:access]:` just press ENTER
        - `CLI default client Region [None]:` use `us-east-2`
        - `CLI default output format [None]:` just press ENTER

    <div class="termy">

    ```bash
    $ aws configure sso --profile mlops
    $ aws sts get-caller-identity --profile mlops
    $ aws sso login --profile mlops
    ```

    </div>


!!! danger "Avoid confusion"
    Always verify that the `mlops` profile is active when running **AWS CLI** commands in this course.

    You can list all available profiles with:

    <div class="termy">

    ```bash
    $ aws configure list-profiles
    ```

    </div>

Now that your environment is configured, you are ready to start working with **AWS CLI** and explore **AWS** services.