import os
import click
from github import Github
from git import Repo

''' A simple script to automate repo creation and initialization '''

click.clear()

# name of repo
rep = click.prompt(click.style("Enter name of ", fg='blue') 
+ click.style("repo", fg='green', bold=True) + click.style(" to be created", fg='blue'))

# system name
name = click.prompt(click.style("Enter ", fg='blue') + 
click.style("system username", fg='green', bold=True))

path = f"/home/{name}/{rep}"

# create local directory
try:  
    os.mkdir(path)
    os.chdir(path)
except OSError:  
    print ("\nCreation of the directory %s failed" % path)
else:  
    click.secho("\nSuccessfully created the directory %s " % path, fg='green')

# get GitHub username and password
username = click.prompt(click.style("\nEnter ", fg='blue') + click.style("GitHub username", fg='green', bold=True))
password = click.prompt(click.style("Enter ", fg='blue') + click.style("GitHub password", fg='green', bold=True), hide_input=True)

# get the user
g = Github(username, password)
user = g.get_user()

# create the repo
user.create_repo(f"{rep}")

# initialize git in local directory
repos = Repo.init(path).git
index = Repo.init(path).index

# create readme in local directory
f = open("README.md", "w+")
f.write(f"# {rep}")
f.close()

# add readme and commit
repos.add("README.md")
index.commit("initial commit")

# push changes
remote = f"https://github.com/{username}/{rep}.git"
os.system(f"git remote add origin {remote}")
os.system("git push -u origin master")