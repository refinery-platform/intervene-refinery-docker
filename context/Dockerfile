FROM rocker/shiny:latest
# No other tags available :(

# django_docker_engine can not proxy websockets.
# http://rstudio.github.io/shiny-server/os/latest/#disabling-websockets-on-the-server
RUN echo 'disable_protocols websocket;' >> /etc/shiny-server/shiny-server.conf

RUN R -e 'install.packages("rjson")'

COPY . .

CMD ["R", "-e", "shiny::runApp('.', 80, host='0.0.0.0')"]