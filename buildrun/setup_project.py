#!/usr/bin/env python3
import argparse
import pathlib
import re

_files_to_replace = [
    ".gitlab-ci.yml",
    ".idea/misc.xml",
    ".idea/runConfigurations/_project_name.xml",
    ".idea/runConfigurations/pytest.xml",
    "README.md",
    "buildrun/docker/caddy/Caddyfile",
    "buildrun/docker/docker-compose/dev-env/docker-compose.yml",
    "buildrun/docker/docker-compose/dev-env/docker-compose.ldap.yml",
    "buildrun/docker/docker-compose/dev-env/Taskfile.yml",
    "buildrun/docker/docker-compose/test-env/docker-compose.yml",
    "buildrun/docker/project_name/Dockerfile",
    "buildrun/docker/project_name/dev.env",
    "buildrun/docker/docker-compose/dev-env/.env",
    "buildrun/docker/docker-compose/test-env/.env",
    "src/configurations/asgi.py",
    "src/configurations/settings.py",
    "src/configurations/partials_settings/base.py",
    "src/configurations/urls.py",
    "src/configurations/wsgi.py",
]


def snake_case_validation(arg_value):
    pat = re.compile(r"^[a-z][a-z0-9_]*$")
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("must be in snake_case")
    return arg_value


def main():
    parser = argparse.ArgumentParser(
        description="Initialise this template for a concrete project"
    )
    parser.add_argument(
        "project_name",
        type=snake_case_validation,
        help="Name of your project, in snake_case",
    )
    parser.add_argument(
        "projet_gitlab_image",
        type=str,
        help="Url of the Gitlab registry image for this project, e.g. gitlab.domain.ovh:4567/domain/dev/dommarket/dommarket",
    )
    parser.add_argument(
        "site_name", type=str, help="Name you want to give to your website"
    )
    args = vars(parser.parse_args())
    args["domain_name"] = args["project_name"].replace("_", "")

    for file_path in _files_to_replace:
        with open(file_path, "r") as file:
            filedata = file.read()
        for pattern in [
            "project_name",
            "projet_gitlab_image",
            "site_name",
            "domain_name",
        ]:
            filedata = filedata.replace(f"#{pattern}", args[pattern])
        with open(file_path, "w") as file:
            file.write(filedata)

    readme_lines = []
    with open("README.md", "r") as file:
        write = False
        for line in file:
            if write:
                readme_lines.append(line)
            elif line.startswith("# Prerequisites"):
                write = True
                readme_lines.append(line)

    with open("README.md", "w") as file:
        file.writelines(readme_lines)

    pathlib.Path(".idea/django-template.iml").rename(
        f".idea/{args['project_name']}.iml"
    )
    pathlib.Path("buildrun/docker/project_name").rename(
        f"buildrun/docker/{args['project_name']}"
    )
    pathlib.Path(".idea/runConfigurations/_project_name.xml").rename(
        f".idea/runConfigurations/{args['project_name']}.xml"
    )

    with open(".idea/modules.xml", "r") as file:
        filedata = file.read()
    filedata = filedata.replace("django-template", args["project_name"])
    with open(".idea/modules.xml", "w") as file:
        file.write(filedata)

    pathlib.Path("buildrun/setup_project.py").unlink()


if __name__ == "__main__":
    main()
