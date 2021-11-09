## Getting started

General steps and shell commands are given.

0. [Install Git](https://git-scm.com/).

1. Clone this repository

`git clone https://github.com/schance995/cmsc421-group-project.git`

Note: this repository is private, please use a [GitHub access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) instead of your password to log in.

If typing your password every time is too annoying, consider setting up an [SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

2. Enter the directory

`cd cmsc421-group-project.git`

3. Create a new branch with your name (real name or GitHub username)

`git checkout -b <YOUR_NAME_HERE>`

## Development

1. Use the `main` branch for testing the app, and your personal branch for development

You can switch branches like so:

`git checkout <branch>`

2. Update your branch from main so that you have the latest changes

```
git pull
git merge main
```

3. Add files to track and commit

`git add <filenames>`

And update the ones already tracked:

`git add -u`

4. Commit changes

`git commit -m <message>`

You can also just type `git commit` and a text editor should pop up, where you can write your commit message. Please make it descriptive so you know what you worked on.

**Make sure you set your default editor to one you are comfortable with! For example Windows Git Bash sets the default editor to Vim which is not comfortable if you are not used to it.**

**Please commit changes regularly so you can roll back if needed!**

## Make a pull request

<https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>

1. Push your branch to the remote repository

`git push -u origin <branch>`

2. On the GitHub project page, click on the "Pull Requests" tab.

3. Click "New" and select "base: main <- compare: {your branch}"

4. Click "Create pull request"

5. Wait for us to review and merge the request to main branch!
