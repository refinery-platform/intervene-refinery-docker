# The rocker/shiny image is unversioned,
# and I never figured out the devtools install,
# so base on tidyverse instead.
FROM rocker/tidyverse:3.5.1

# Install shiny server (from https://hub.docker.com/r/rocker/shiny/~/dockerfile/)
# changes:
#   Formatting
#   -t unstable -> (remove)
#   libcairo2-dev/unstable -> libcairo2-dev
RUN apt-get update && \
    apt-get install -y \
        sudo \
        gdebi-core \
        pandoc \
        pandoc-citeproc \
        libcurl4-gnutls-dev \
        libcairo2-dev \
        libxt-dev && \
    S3=https://s3.amazonaws.com/rstudio-shiny-server-os-build/ubuntu-12.04/x86_64 && \
	wget --no-verbose $S3/VERSION -O version.txt && \
	VERSION=$(cat version.txt) && \
	wget --no-verbose $S3/shiny-server-$VERSION-amd64.deb -O ss-latest.deb && \
	gdebi -n ss-latest.deb && \
	rm -f version.txt ss-latest.deb && \
	R -e "install.packages(c('shiny', 'rmarkdown'), repos='https://cran.rstudio.com/')" && \
	cp -R /usr/local/lib/R/site-library/shiny/examples/* /srv/shiny-server/ && \
	rm -rf /var/lib/apt/lists/*

# django_docker_engine can not proxy websockets.
# http://rstudio.github.io/shiny-server/os/latest/#disabling-websockets-on-the-server
RUN echo 'disable_protocols websocket;' >> /etc/shiny-server/shiny-server.conf

# Requirements from https://github.com/asntech/intervene-shiny/blob/version-1.0/README.md
RUN R -e 'install.packages(c("shiny","shinydashboard", "devtools", "d3heatmap", "plotly", "gplots", "ggplot2", "gridExtra", "plyr", "UpSetR", "colourpicker", "corrplot", "BBmisc", "readr", "DT"));'
RUN R -e 'source("https://bioconductor.org/biocLite.R"); biocLite(c("RBGL","graph"));'
RUN R -e 'library(devtools);'

COPY . .

CMD ["R", "-e", "shiny::runApp('.', 80, host='0.0.0.0')"]