# intervene-refinery-docker
[![Build Status](https://travis-ci.org/refinery-platform/intervene-refinery-docker.svg?branch=master)](https://travis-ci.org/refinery-platform/intervene-refinery-docker)

Wrap the [Intervene shiny app](https://github.com/asntech/intervene-shiny) for Refinery

## Release process

Successful Github tags and PRs will prompt Travis to push the built image to Dockerhub. For a new version number:

```bash
$ git tag v0.0.x && git push origin --tags
```