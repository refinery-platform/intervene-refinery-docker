library(shiny)
library(rjson)

input_json = paste(readLines(Sys.getenv('INPUT_JSON_URL')), collapse = "")
input_data = fromJSON(input_json)
n <- 200

ui <- fluidPage(
    sidebarPanel(
        selectInput('xcol', 'X Variable', names(iris)),
        selectInput('ycol', 'Y Variable', names(iris),
            selected = names(iris)[[2]]),
        numericInput('clusters', 'Cluster count', 3,
            min = 1, max = 9)
    ),
    titlePanel("Hello World!"),
    mainPanel(
        paste("If this were for real, you would read from: ",
            input_data['file_relationships']
        ),
        plotOutput('plotIris')
    )
)

server <- function(input, output) {
    # From https://shiny.rstudio.com/gallery/kmeans-example.html
    # Simple example that exercises the network.

    selectedData <- reactive({
        iris[, c(input$xcol, input$ycol)]
    })

    clusters <- reactive({
        kmeans(selectedData(), input$clusters)
    })

    output$plotIris <- renderPlot({
        palette(c("#E41A1C", "#377EB8", "#4DAF4A", "#984EA3",
        "#FF7F00", "#FFFF33", "#A65628", "#F781BF", "#999999"))

        par(mar = c(5.1, 4.1, 0, 1))
        plot(selectedData(),
        col = clusters()$cluster,
        pch = 20, cex = 3)
        points(clusters()$centers, pch = 4, cex = 4, lwd = 4)
    })
}

shinyApp(ui = ui, server = server)
