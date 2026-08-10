# GitHub Automation Playbook

This profile is set up to stay alive without rewriting old academic projects.

## What is automated

- `Profile health`: checks README links, images, and badges every Monday.
- `Sync new repositories`: refreshes the profile radar every Monday and on manual runs.
- `Data Project Starter`: a public template repository for new data projects.

## How new repositories show up on the profile

Create a public repository with at least one data-oriented signal in the name, description, language, or topics:

- `data`
- `analytics`
- `analysis`
- `dados`
- `python`
- `sql`
- `machine-learning`
- `etl`
- `pipeline`
- `bi`
- `statistics`

The profile workflow will detect it and update the `Portfolio radar` block in the profile README.

## Recommended flow from any computer

1. Open `https://github.com/guivital1/data-project-starter`.
2. Click `Use this template`.
3. Create a new public repository with a clear data-oriented name and description.
4. Add data-oriented topics after the repository is created.
5. Push your analysis, notebooks, source code, and reports.
6. Run `Sync new repositories` manually in the profile repo, or wait for the weekly schedule.

## Fully automatic setup for future repos

GitHub Actions in the profile repository can update the profile repository using `GITHUB_TOKEN`.

To edit newly created repositories automatically, GitHub needs a fine-grained personal access token saved as a secret, for example `PROFILE_AUTOMATION_TOKEN`, with access only to selected repositories and only the minimum permissions needed.

That stronger version is intentionally not enabled by default. It is useful later, but the safer default is: create repos from `data-project-starter`, detect new repos, and update the profile radar.

## Old projects policy

Old delivered projects are preserved as history. Automations should not refactor, lint, rewrite, or chase failures in those repositories unless a future goal explicitly revives one of them.
