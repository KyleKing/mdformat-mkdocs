prerequisites needs a new title and the template needs real prerequisites 
### intro
We are looking forward to having you on our team. Please ensure you have prior experience with the HfLA website team before contributing to our repository.
### prerequisites 
- [x] join
    - [x] `added hyperlinks for ease` ops [Slack Channel](https://app.slack.com/client/T04502KQX/CGRATJCCF)
    - [x] `added hyperlinks for ease` [devops-security](https://github.com/hackforla/devops-security) repository

### Action Items
- [x] Add this issue to the Project Board under the Projects section (gear in right side panel). # add [CoP: DevOps: Project Board](https://github.com/orgs/hackforla/projects/73)
> - [x] Add this issue to the Project Board under the Projects section (gear in right side panel). as title [CoP: DevOps: Project Board](https://github.com/orgs/hackforla/projects/73)
- [x] Attend weekly team meeting, Wednesdays 6-8pm PST.
  - Note: There are no meetings on the 1st-7th of every month. # should be attention getting instead of a step
        <ins>***Note: There are no meetings on the 1st-7th of every month.***</ins>

### AWS 
- [x] use this [video guide](https://www.youtube.com/watch?si=78GhlDLV5zZu8qwh&v=CjKhQoYeR4Q&feature=youtu.be) for the following 
  - [x] Complete [Creating a personal AWS account](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#creating-a-personal-aws-account)
    - [x] `link was broken` [Login as root user & setup MFA](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#login-as-root-user--setup-mfa)
    - [x] `link led to creating iam user group not user` [Creating an IAM User](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#login-as-root-user--setup-mfa)

### AWS CLI
- [x] Read and follow the instructions in [Setting up IAM and AWS CLI](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#setting-up-iam-and-aws-cli) for:
    - [x] [Creating an IAM Group](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#create-an-iam-group)
    - [x] [Attaching IAM user to IAM Group](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#attach-iam-user-to-iam-group)
    - [x] [Providing `AdministratorAccess` policy to IAM group](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#attach-administratoraccess-policy-to-iam-group)
    - [x] Log in as the newly created user instead of continuing to log in as the root user (it is not recommended to login with root access).
    - [x] [Generating user access keys](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#generating-access-keys-for-aws-cli)

### AWS CLI quick quide
```bash
aws iam create-group --group-name AdminGroup
aws iam create-user --user-name drakeredwind01
aws iam create-login-profile --user-name drakeredwind01 --password ExamplePassword123!
aws iam add-user-to-group --group-name AdminGroup --user-name drakeredwind01
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AdministratorAccess --group-name AdminGroup
aws iam create-access-key --user-name drakeredwind01 > access_key.json
nano access_key.json
```


- [x] Complete the instructions in [AWS Documentation](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-install.html) and choose your operating system to install AWS CLI. 
- [x] Complete the instruction in [AWS Documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-short-term.html) to setup the AWS CLI.

### `old`backend state
- [x] Read follow the instructions in [Creating a backend state](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#creating-backend-state).
- [x] Create S3 bucket
  - [x] Region: us-west-2 (Oregon) 
  - [x] Name: `hfla-ops-terraform-state` 
  - [x] Enable versioning 
  - [x] Enable server-side encryption
- [x] Set up DynamoDB to store backend
  - [x] Create table `hfla_ops_terraform_table`
  - [x] Set partition key to `LockID` with a type of `String`
  - [x] Choose on-demand capacity

### Resources/Instructions
https://developer.hashicorp.com/terraform/language/settings/backends/s3


### `new`backend state
- [x] Read follow the instructions in [Creating a backend state](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#creating-backend-state).
- [x] Create S3 bucket
  - [x] `added for ease` search for `s3`
  - [x] AWS Region: US West (Oregon) us-west-2
  - [x] `?` Bucket type `General purpose` or `Directory - New`
  - [x] Bucket name `hfla-ops-terraform-state`
  - [x] Enable versioning 
  - [x] `?` Enable server-side encryption
    - [x] `?` Server-side encryption with Amazon S3 managed keys (SSE-S3)
    - [x] `?` Server-side encryption with AWS Key Management Service keys (SSE-KMS)
  - [x] `?` Bucket Key `default Enable` 
- [x] Set up DynamoDB to store backend
  - `added for ease` search for `DynamoDB`
  - `added for ease` Table details
    - [x] Create table `hfla_ops_terraform_table`
    - [x] Set partition key to `LockID` with a type of `String`
    - [x] Choose on-demand capacity
  - `added for ease` Table settings
    - [x] `added` Customize settings
  - `added for ease` Read/write capacity settings
    - [x] On-demand
  - `?` Deletion protection




### Terraform
- [x] Install Terraform locally by following the instructions of the installation guide mentioned in [Installing Terraform](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#installing-terraform)
    - (windows) **make sure terraform is in your path**
- [x] Install Terraform Docs locally by following the instructions of the installation guide mentioned in [Installing Terraform docs](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#installing-terraform-docs)
  #### WINDOWS
  - if you have windows you first need [scoop](https://scoop.sh/#/)
  - run scoop command
    - ```cmd
      scoop bucket add terraform-docs https://github.com/terraform-docs/scoop-bucket
      scoop install terraform-docs
      ```
    - if you don't have scoop run install it by running the following in powershell
      - ```powershell
        iex (new-object net.webclient).DownloadString('https://get.scoop.sh')
        ```
      - if you get following error in red letters run the bellow command `PowerShell requires an execution policy in [Unrestricted, RemoteSigned, ByPass] to run Scoop. For example, to set the execution policy to 'RemoteSigned' please run 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser'.`
        - ```powershell
          Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
          ```
- [x] Complete the instructions in [Clone the repository](https://github.com/hackforla/devops-security/blob/main/CONTRIBUTING.md#clone-the-repository)
- [x] Submit a [new request](https://github.com/hackforla/devops-security/issues/new?assignees=&labels=enhancement&projects=&template=request-aws-iam-resources.yml) to create new AWS user account and then self-assign this issue.
  - [x] `? {github handle} or {service account}. which service account? the one for aws?` Account Name: 
  - [x] Project(s) Name: https://github.com/hackforla/devops-security.git
  - [x] `? no instructions given. should i put in: in order to complete "Pre-work Checklist: DevOps-Security-Member: drakeredwind01 #36"` Reason for access:






- [x] Create a new branch from main by executing the command
    ```bash
    git checkout -b issue-number-add-new-iam-user
    ```
    - `added for ease` example
        ```bash
        git checkout -b 36-add-new-iam-user-drakeredwind01
        ```

- [x] Navigate to the `aws-user.tf` file and add your user information and follow the below template.

    ```bash
    module "iam_user_testiamuser" {
    source = "./modules/aws-users"

    user_name = "testiamuser"
    user_tags = {
      "Project"      = "devops-security"
      "Access Level" = "1"
    }
    user_groups = ["read-only-group"]
    }
    ```
- [x] In your code editor navigate to `terraform` directory. `cd terraform`
# [left off](https://github.com/hackforla/devops-security/issues/36)
- [x] Execute the command `terraform init` to initialize terraform in the directory. Address any failures that arise (if any).
    - if using pycharm go to `settings` then `plugins`  
    - [x] install `AWS Core`
    - [x] install `AWS Toolkit`
    - [x] restart pycharm
        - on the left side bar you will see `project`,`commit`,`pull request`,`structure`,`AWS Toolkit`
    - [x] click `AWS Toolkit`
    - [x] click `Add Another Connection`
    - [x] click `IAM Credentials`
    - [x] click `Continue`
    - [x] enter `profile name`,`access key`,`secret key` found in `access_key.json`
        - go to [cloudshell](https://us-west-2.console.aws.amazon.com/cloudshell) and type `nano access_key.json`
    - [x] click `Continue`
- [ ] Execute the command `terraform plan` this will output a plan replicating the same IAM resources as the devops security account. Address any failures that arise (if any).
- [ ] Then execute the command `terraform apply` this will create all of the resources that are currently managed by Devops Security. All of the resources created here incur zero cost except for the Dynamo DB installation, which should remain in the free tier.
      - [ ] ** If you have cost concerns, Run a Terraform Destroy to take down all of the resources you created (don't worry, you can recreate them just as quickly). **
- [ ] Once you have tested your changes, stage them in git with 
    - [ ] `git status` command.
    - [ ] then `git add path/to/file` (you can copy from above output for the file path).
- [ ] Commit the changes by executing `git commit -m "briefly describing the changes"`.
- [ ] Push the changes with `git push --set-upstream origin name-of-branch`


























# NOTES
my notes

python "D:\documents\ai\python\my-first-conda-project\_read to me args (with read time and csv stats) 1.py" "

commenter:drakeredwind01

suggest removing `needs-triage` `needs-sig` and adding `triage/accepted`, `sig-network`, and `sig-security`

## O3DE Network SIG - Issue Triage Guide
https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-triage+-label%3Asig%2Fnetwork++--label%3Asig%2Fbuild+--label%3Asig%2Fbuild+

1. Open issues with `needs-sig` label: https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-sig
   1. `OLD` 
   2. `NEW` 
2. Main O3DE repository: 
   1. `OLD` https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-triage+label%3Asig%2Fnetwork
   2. `NEW` https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-triage+-label%3Asig%2Fnetwork++--label%3Asig%2Fbuild+--label%3Asig%2Fbuild+
>     altered is:issue is:open label:needs-triage label:sig/network
>      to     is:issue is:open label:needs-triage -label:sig/network  -label:sig/build -label:sig/build  
3. Multiplayer Sample: https://github.com/o3de/o3de-multiplayersample/labels/needs-triage
   1. `OLD` 
   2. `NEW` 
4. NetSoak Test: https://github.com/o3de/o3de-netsoaktest/issues
   1. `OLD` 
   2. `NEW` 
5. [Multiplayer template](https://github.com/o3de/o3de-extras/tree/development/Templates/Multiplayer) issues in: 
   1. `OLD` issues in: https://github.com/o3de/o3de-extras/labels/sig%2Fnetwork
   2. `NEW` issues in: https://github.com/o3de/o3de-extras/issues?q=is%3Aopen+label%3Asig%2Fnetwork+++-label%3Asig%2Fnetwork+-label%3Asig%2Fcore+-label%3Asig%2Fbuild+-label%3Asig%2Fsimulation+-label%3Asig%2Frelease+-label%3Asig%2Fgraphics-audio+-label%3Asig%2Fplatform+
>     altered is:open label:sig/network  -label:sig/network
>      to      is:open label:sig/network   -label:sig/network -label:sig/core -label:sig/build -label:sig/simulation -label:sig/release -label:sig/graphics-audio -label:sig/platform  





## O3DE sig-security - Issue Triage Guide
https://github.com/o3de/sig-security/blob/main/TRIAGE_GUIDE.md

* O3DE issues to triage for SIG:
    * https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-triage+label%3Asig%2Fsecurity
    * https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Aneeds-triage+-label%3Asig%2Fsecurity+-label%3Asig%2Fbuild+-label%3Asig%2Fcontent+-label%3Asig%2Fcore+-label%3Asig%2Fdocs-community+-label%3Asig%2Fnetwork+-label%3Asig%2Fplatform+-label%3Asig%2Fgraphics-audio+-label%3Asig%2Frelease+-label%3Asig%2Fsimulation+-label%3Asig%2Ftesting+-label%3Asig%2Fui-ux+-label%3Asig%2FTAC%2FTSC+-label%3Asig%2Fmobile+
* O3DE known security issues: https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Akind%2Fsecurity
    * https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Akind%2Fsecurity
    * https://github.com/o3de/o3de/issues?q=is%3Aissue+is%3Aopen+label%3Akind%2Fsecurity+-label%3Atriage%2Faccepted+-kind%3Akind%2Fsecurity
* Dependabot alerts to check (link only accessible to SIG-Security maintainers): 
  <br>`broken` https://github.com/o3de/o3de/security/dependabot
    * For new alerts, create new GitHub issues against [O3DE](https://github.com/o3de/o3de) and tag with `kind\security` label for tracking.
    * **WARNING**: Since the O3DE _python/requirements.txt_ file includes hashes, Dependabot-generated PRs against this file should be **manually tested** against a clean `/python` folder (that is, no `/runtime` child dir) **prior to merging** in order to suss out any issues with hashing transitive dependencies.







